# SocketTB v1.1.1 (https://github.com/PCigales/WinSocketTB)
# Copyright © 2023 PCigales
# This program is licensed under the GNU GPLv3 copyleft license (see https://www.gnu.org/licenses)

import socket
import ssl
import ctypes, ctypes.wintypes
import threading
import weakref
from collections import deque
import time
import datetime
import types
from functools import reduce
import urllib.parse
import email.utils
from io import BytesIO
import math
import base64
import hmac
import zlib
import gzip
import os
import hashlib
import struct
import textwrap
import subprocess

__all__ = ['ISocketGenerator', 'IDSocketGenerator', 'NestedSSLContext', 'HTTPMessage', 'HTTPStreamMessage', 'HTTPRequestConstructor', 'RSASelfSigned', 'UDPIServer', 'TCPIServer', 'RequestHandler', 'MultiUDPIServer', 'WebSocketDataStore', 'WebSocketRequestHandler', 'WebSocketIDServer', 'WebSocketIDClient', 'NTPClient', 'TOTPassword']

ws2 = ctypes.WinDLL('ws2_32', use_last_error=True)
iphlpapi = ctypes.WinDLL('iphlpapi', use_last_error=True)
wcrypt = ctypes.WinDLL('crypt32', use_last_error=True)
ncrypt = ctypes.WinDLL('ncrypt', use_last_error=True)
kernel32 = ctypes.WinDLL('kernel32',  use_last_error=True)
byref = ctypes.byref
INT = ctypes.c_int
UINT = ctypes.c_uint
LONG = ctypes.c_long
ULONG = ctypes.c_ulong
WORD = ctypes.wintypes.WORD
USHORT = ctypes.wintypes.USHORT
DWORD = ctypes.wintypes.DWORD
ULONG = ctypes.wintypes.ULONG
BOOL = ctypes.c_bool
PVOID = ctypes.c_void_p
SOCKET  = PVOID
WSAEVENT = PVOID
HANDLE = ctypes.wintypes.HANDLE
LPCWSTR = ctypes.wintypes.LPCWSTR
LPWSTR = ctypes.wintypes.LPWSTR
LPVOID = ctypes.wintypes.LPVOID
LPCVOID = ctypes.wintypes.LPCVOID
POINTER = ctypes.POINTER
STRUCTURE = ctypes.Structure

class WSANETWORKEVENTS(STRUCTURE):
  _fields_ = [('lNetworkEvents', LONG), ('iErrorCode', INT*10)]
class MIB_IPADDRROW(STRUCTURE):
  _fields_=[('dwAddr', DWORD), ('dwIndex', DWORD), ('dwMask', DWORD), ('dwBCastAddr', DWORD), ('dwReasmSize', DWORD), ('unused', USHORT), ('wType', USHORT)]
class MIB_IPADDRTABLE(STRUCTURE):
  _fields_ = [('dwNumEntries', DWORD), ('table', MIB_IPADDRROW*0)]
P_MIB_IPADDRTABLE = POINTER(MIB_IPADDRTABLE)

class CRYPT_KEY_PROV_INFO(STRUCTURE):
  _fields_ = [('pwszContainerName', LPWSTR), ('pwszProvName', LPWSTR), ('dwProvType', DWORD), ('dwFlags', DWORD), ('cProvParam', DWORD), ('rgProvParam', PVOID), ('dwKeySpec', DWORD)]
class CERT_EXTENSIONS(STRUCTURE):
  _fields_ = [('cExtension', DWORD), ('rgExtension', HANDLE)]
class SYSTEMTIME(STRUCTURE):
  _fields_ = [('wYear', WORD), ('wMonth', WORD), ('wDayOfWeek', WORD), ('wDay', WORD), ('wHour', WORD), ('WMinute', WORD), ('WSecond', WORD), ('WMilliseconds', WORD)]
P_SYSTEMTIME = POINTER(SYSTEMTIME)
class CRYPT_INTEGER_BLOB(STRUCTURE):
  _fields_ = [('cbData', DWORD), ('pbData', PVOID)]
class CERT_CONTEXT(STRUCTURE):
  _fields_ = [('dwCertEncodingType', DWORD), ('pbCertEncoded', PVOID), ('cbCertEncoded', DWORD), ('pCertInfo', PVOID), ('hCertStore', HANDLE)]
P_CERT_CONTEXT = POINTER(CERT_CONTEXT)


class ISocketMeta(type):

  def func_wrap(cls, mode, func, f):
    def w(self, *args, timeout='', **kwargs):
      return cls._func_wrap(self, mode, func, f, *args, timeout=timeout, **kwargs)
    w.__name__ = func.__name__
    w.__qualname__ = cls._func_wrap.__qualname__[:-10] + func.__name__
    return w

  def __init__(cls, *args, **kwargs):
    type.__init__(cls, *args, **kwargs)
    for name in ('recv', 'recvfrom', 'recv_into', 'recvfrom_into'):
      setattr(cls, name, cls.func_wrap('r', getattr(socket.socket, name), 2 if name[-4:] == 'into' else 1))
    for name in ('send', 'sendto'):
      setattr(cls, name, cls.func_wrap('w', getattr(socket.socket, name), float('inf')))
    def attribute_error(self, *args, **kwargs):
      raise NotImplementedError()
    for name in ('dup', 'makefile', 'connect_ex', 'ioctl', 'share'):
      setattr(cls, name, attribute_error)


class ISocket(socket.socket, metaclass=ISocketMeta):

  MODES = {'r': LONG(33), 'a': LONG(8), 'w': LONG(34), 'c': LONG(16)}

  def __init__(self, gen, family=-1, type=-1, proto=-1, fileno=None, timeout=''):
    socket.socket.__init__(self, family, type, proto, fileno)
    self.gen = gen
    self.sock_fileno = socket.socket.fileno(self)
    self.sock_timeout = gen.defaulttimeout if timeout == '' else timeout
    socket.socket.settimeout(self, 0)
    self.event = WSAEVENT(ws2.WSACreateEvent())
    self._mode = ''
    self._lock = threading.RLock()
    self.closed = False
    gen.isockets[self] = True

  def lock(self, timeout=''):
    if timeout == '':
      timeout = self.sock_timeout
    t = time.monotonic()
    a = self._lock.acquire(timeout=(timeout if timeout is not None else -1))
    if a:
      return (None if timeout is None else max(0, timeout + t - time.monotonic())), None
    else:
      raise InterruptedError() if self.closed else TimeoutError()

  def unlock(self, ul):
    self._lock.release()

  @property
  def mode(self):
    rt, ul = self.lock(None)
    try:
      return self._mode if not self.closed else None
    finally:
      self.unlock(ul)

  @mode.setter
  def mode(self, value):
    if self._mode == value or (self.closed and value is not None):
      return
    self._mode = value
    ws2.WSAEventSelect(SOCKET(self.sock_fileno), WSAEVENT(None), LONG(0))
    if value is not None:
      ws2.WSAResetEvent(self.event)
      ws2.WSAEventSelect(SOCKET(self.sock_fileno), self.event, self.MODES.get(value, LONG(0)))
    else:
      ws2.WSACloseEvent(self.event)
      self.gen.isockets[self] = False

  def unwrap(self, timeout=''):
    rt, ul = self.lock(timeout)
    try:
      self.mode = None
      self.closed = True
      sock = socket.socket(family=self.family, type=self.type, proto=self.proto, fileno=self.sock_fileno) if self.sock_fileno >= 0 else None
      self.detach()
    finally:
      self.unlock(ul)
    try:
      sock.settimeout(self.sock_timeout)
    except:
      pass
    return sock

  def shutdown(self, *args, timeout='', **kwargs):
    rt, ul = self.lock(timeout)
    try:
      if not self.closed:
        socket.socket.shutdown(self, *args, **kwargs)
      else:
        raise InterruptedError()
    finally:
      self.unlock(ul)

  def _close(self):
    self.closed = True
    ws2.WSASetEvent(self.event)
    rt, ul = self.lock(None)
    self.mode = None
    self.unlock(ul)
    self.sock_fileno = -1

  def close(self):
    self._close()
    socket.socket.close(self)

  def shutclose(self):
    self._close()
    try:
      socket.socket.shutdown(self, socket.SHUT_RDWR)
    except:
      pass
    try:
      socket.socket.close(self)
    except:
      pass

  def detach(self):
    self._close()
    return socket.socket.detach(self)

  def __enter__(self):
    return self

  def __exit__(self, et, ev, tb):
    self.shutclose()

  def __del__(self):
    self.shutclose()
    super().__del__()

  def gettimeout(self):
    return self.sock_timeout

  def settimeout(self, value):
    self.sock_timeout = value

  def getblocking(self):
    return self.sock_timeout != 0

  def setblocking(self, flag):
    self.sock_timeout = None if flag else 0

  @property
  def timeout(self):
    return self.sock_timeout

  def wait(self, timeout):
    if not self.mode or (timeout is not None and timeout < 0):
      return False
    if ws2.WSAWaitForMultipleEvents(ULONG(1), byref(self.event), BOOL(False), ULONG(int(timeout * 1000) if timeout is not None else -1), BOOL(False)) == 258 or not self.mode:
      return False
    else:
      ws2.WSAResetEvent(self.event)
      return True

  def _func_wrap(self, mode, func, f, *args, timeout='', **kwargs):
    rt, ul = self.lock(timeout)
    try:
      if self.closed:
        raise InterruptedError()
      self.mode = mode
      ws2.WSAResetEvent(self.event)
      try:
        r = func(self, *args, **kwargs)
        if len(args) > f and (args[f] & socket.MSG_PEEK):
          ws2.WSASetEvent(self.event)
        return r
      except BlockingIOError:
        if self.wait(rt):
          if len(args) > f and (args[f] & socket.MSG_PEEK):
            ws2.WSASetEvent(self.event)
          return func(self, *args, **kwargs)
      raise InterruptedError() if self.closed else TimeoutError()
    finally:
      self.unlock(ul)

  def _sendall(self, bytes, *args, timeout=None, **kwargs):
    t = time.monotonic()
    rt = timeout
    with memoryview(bytes) as m:
      l = len(m)
      s = 0
      while s < l:
        if timeout is not None and rt < 0:
          raise TimeoutError()
        s += self.send(m[s:], *args, timeout=rt, **kwargs)
        if timeout is not None:
          rt = timeout + t - time.monotonic()

  def sendall(self, bytes, *args, timeout='', **kwargs):
    rt, ul = self.lock(timeout)
    try:
      self._sendall(bytes, *args, timeout=rt, **kwargs)
    finally:
      self.unlock(ul)

  def accept(self, timeout=''):
    rt, ul = self.lock(timeout)
    try:
      if self.closed:
        raise InterruptedError()
      self.mode = 'a'
      ws2.WSAResetEvent(self.event)
      self.gettimeout = lambda : None
      a = None
      try:
        a = socket.socket.accept(self)
      except BlockingIOError:
        del self.gettimeout
        if self.wait(rt):
          self.gettimeout = lambda : None
          a = socket.socket.accept(self)
      finally:
        try:
          del self.gettimeout
        except:
          pass
      if a is not None:
        isock = self.gen.wrap(a[0])
        isock.settimeout(self.timeout)
        isock.mode = 'r'
        return (isock, a[1])
      raise InterruptedError() if self.closed else TimeoutError()
    finally:
      self.unlock(ul)

  def connect(self, *args, timeout='', **kwargs):
    rt, ul = self.lock(timeout)
    try:
      if self.closed:
        raise InterruptedError()
      self.mode = 'c'
      ws2.WSAResetEvent(self.event)
      try:
        socket.socket.connect(self, *args, **kwargs)
        return
      except BlockingIOError:
        if self.wait(rt):
          self.mode = 'w'
          if self.wait(0):
            return
          else:
            raise ConnectionRefusedError()
      raise InterruptedError() if self.closed else TimeoutError()
    finally:
      self.unlock(ul)

  @classmethod
  def _wait_for_events(cls, timeout, events, event_c=None):
    c = len(events) if event_c is None else (len(events) + 1)
    if c <= 64:
      if event_c is None:
        w = ws2.WSAWaitForMultipleEvents(ULONG(c), byref((WSAEVENT*c)(*events)), BOOL(False), timeout, BOOL(False))
      else:
        w = ws2.WSAWaitForMultipleEvents(ULONG(c), byref((WSAEVENT*c)(*events, event_c)), BOOL(False), timeout, BOOL(False))
    else:
      ev_c = WSAEVENT(ws2.WSACreateEvent()) if event_c is None else event_c
      t = threading.Thread(target=cls._wait_for_events, args=(timeout, events[63:], ev_c), daemon=True)
      t.start()
      w = ws2.WSAWaitForMultipleEvents(ULONG(64), byref((WSAEVENT*64)(*events[:63], ev_c)), BOOL(False), timeout, BOOL(False))
    if event_c is None:
      if c > 64:
        ws2.WSASetEvent(ev_c)
      return w
    elif w != 258:
      ws2.WSASetEvent(event_c)

  @classmethod
  def waitmult(cls, timeout, *isocks, event=None, reset_event=False):
    if not event in ('None', 'r', 'a', 'w', 'c'):
      return ()
    t = time.monotonic()
    rt = timeout
    locks = 0
    for isock in isocks:
      if (not isock._lock.acquire(timeout=-1)) if timeout is None else (rt < 0 or not isock._lock.acquire(timeout=rt)):
        for i in range(locks):
          isocks[i]._lock.release()
        return ()
      locks += 1
      if event is not None:
        isock.mode = event
      if timeout is not None:
        rt = timeout + t - time.monotonic()
    isocks_ = tuple(isock for isock in isocks if isock.mode)
    c = len(isocks_)
    if cls._wait_for_events(ULONG(int(rt * 1000) if timeout is not None else -1), tuple(isock.event for isock in isocks_)) == 258:
      r = ()
    else:
      r = tuple(isock for isock in isocks_ if (ws2.WSAWaitForMultipleEvents(ULONG(1), byref(isock.event), BOOL(False), ULONG(0), BOOL(False)) != 258 and isock.mode) and ((reset_event and ws2.WSAResetEvent(isock.event)) or True))
    for isock in isocks:
      isock._lock.release()
    return r


class ISocketGenerator:

  CLASS = ISocket

  def __init__(self):
    self.isockets = weakref.WeakKeyDictionary()
    self.lock = threading.Lock()
    self.closed = False
    self.defaulttimeout = socket.getdefaulttimeout()

  def wrap(self, sock):
    with self.lock:
      return self.CLASS(self, sock.family, sock.type, sock.proto, sock.detach(), sock.gettimeout()) if not self.closed else None

  def new(self, family=-1, type=-1, proto=-1):
    with self.lock:
      return self.CLASS(self, family, type, proto) if not self.closed else None

  def __call__(self, *args, **kwargs):
    return self.new(*args, **kwargs) if not args or not isinstance(args[0], socket.socket) else self.wrap(args[0])

  def socket(self, family=-1, type=-1, proto=-1):
    return self.new(family, type, proto)

  def close(self):
    with self.lock:
      self.closed = True
    fi = True
    for isock, activ in self.isockets.items():
      if fi:
        for isock_ in self.isockets:
          isock_.closed = True
        fi = False
      if activ:
        isock.shutclose()

  def __enter__(self):
    return self

  def __exit__(self, et, ev, tb):
    self.close()

  def getdefaulttimeout(self):
    return self.defaulttimeout

  def setdefaulttimeout(self, timeout):
    self.defaulttimeout = timeout

  def create_connection(self, address, timeout='', source_address=None):
    if timeout == '':
      timeout = socket.getdefaulttimeout()
    err = None
    t = time.monotonic()
    rt = timeout
    for res in socket.getaddrinfo(*address, 0, socket.SOCK_STREAM):
      if self.closed:
        return None
      if timeout is not None and rt < 0:
        raise TimeoutError()
      isock = None
      try:
        isock = self.new(*res[:3])
        if self.closed:
          return None
        if source_address:
          isock.bind(source_address)
        isock.connect(res[4], timeout=rt)
        return isock
      except Exception as _err:
        err = _err
        if isock is not None:
          isock.close()
      if timeout is not None:
        rt = timeout + t - time.monotonic()
    raise err if err is not None else socket.gaierror()

  def waitany(self, timeout, event):
    if not event in ('r', 'a', 'w', 'c') or self.closed:
      return ()
    return ISocket.waitmult(timeout, *(isock for isock, activ in self.isockets.items() if activ), event=event, reset_event=False)


class IDSocket(ISocket):

  MODES = {'u': LONG(59)}
  MODES_M = {'r': 33, 'a': 8, 'w': 34, 'c': 16}
  MODES_I = {'r': 0, 'a': 3, 'w': 1, 'c': 4}

  def __init__(self, gen, family=-1, type=-1, proto=-1, fileno=None, timeout=''):
    super().__init__(gen, family, type, proto, fileno, timeout)
    self._condition = threading.Condition(self._lock)
    self._queue_r = deque()
    self._queue_w = deque()
    self.events = {m: threading.Event() for m in ('r', 'a', 'w', 'c')}
    self.errors = {m: 0 for m in ('r', 'a', 'w', 'c')}
    self.wait_start()

  def lock(self, timeout='', mode='u'):
    th = threading.current_thread()
    if mode == 'r':
      pred = lambda : self._queue_r[0][0] == th
    elif mode == 'w':
      pred = lambda : self._queue_w[0][0] == th
    else:
      pred = lambda : self._queue_r[0][0] == th and self._queue_w[0][0] == th
    if timeout == '':
      timeout = self.sock_timeout
    t = time.monotonic()
    a_r = a_w = None
    with self._condition:
      if mode != 'w':
        a_r = [th]
        self._queue_r.append(a_r)
      if mode != 'r':
        a_w = [th]
        self._queue_w.append(a_w)
      a = pred()
      if not a:
        a = self._condition.wait_for(pred, timeout)
    if a:
      return (None if timeout is None else timeout + t - time.monotonic()), (a_r, a_w)
    else:
      raise InterruptedError() if self.closed else TimeoutError()

  def unlock(self, ul):
    a_r, a_w = ul
    with self._condition:
      if a_r is not None:
        a_r[0] = None
        while self._queue_r and self._queue_r[0][0] is None:
          self._queue_r.popleft()
      if a_w is not None:
        a_w[0] = None
        while self._queue_w and self._queue_w[0][0] is None:
          self._queue_w.popleft()
      self._condition.notify_all()

  @staticmethod
  def _wait(ref):
    self = ref()
    if not self:
      return
    e = self.event
    f = SOCKET(self.sock_fileno)
    lpNetworkEvents = WSANETWORKEVENTS()
    while not self.closed:
      del self
      ws2.WSAWaitForMultipleEvents(ULONG(1), byref(e), BOOL(False), ULONG(-1), BOOL(False))
      self = ref()
      if self:
        if not self.closed:
          if ws2.WSAEnumNetworkEvents(f, e, byref(lpNetworkEvents)):
            ws2.WSAResetEvent(e)
          else:
            for m in ('r', 'a', 'w', 'c'):
              if lpNetworkEvents.lNetworkEvents & self.MODES_M[m]:
                self.events[m].set()
                self.errors[m] = lpNetworkEvents.iErrorCode[self.MODES_I[m]]
                self.gen.events[m].set()
      else:
        return
    for m in ('r', 'a', 'w', 'c'):
      self.events[m].set()
      self.gen.events[m].set()
    del self

  def wait_start(self):
    self.mode = 'u'
    t = threading.Thread(target=self.__class__._wait, args=(weakref.getweakrefs(self)[0],), daemon=True)
    t.start()

  def _func_wrap(self, m, func, f, *args, timeout='', **kwargs):
    rt, ul = self.lock(timeout, m)
    try:
      self.events[m].clear()
      if self.closed:
        raise InterruptedError()
      t = None
      while True:
        try:
          r = func(self, *args, **kwargs)
          if len(args) > f and (args[f] & socket.MSG_PEEK):
            self.events[m].set()
          return r
        except BlockingIOError:
          if rt is not None:
            if t is None:
              rt0 = rt
              t = time.monotonic()
            else:
              rt = rt0 + t - time.monotonic()
          if self.events[m].wait(rt):
            if len(args) <= f or not (args[f] & socket.MSG_PEEK):
              self.events[m].clear()
            if self.closed:
              raise InterruptedError()
          else:
            break
      raise InterruptedError() if self.closed else TimeoutError()
    finally:
      self.unlock(ul)

  def sendall(self, bytes, *args, timeout='', **kwargs):
    rt, ul = self.lock(timeout, 'w')
    try:
      self._sendall(bytes, *args, timeout=rt, **kwargs)
    finally:
      self.unlock(ul)

  def accept(self, timeout=''):
    rt, ul = self.lock(timeout, 'a')
    try:
      self.events['a'].clear()
      if self.closed:
        raise InterruptedError()
      t = None
      a = None
      while True:
        self.gettimeout = lambda : None
        try:
          a = socket.socket.accept(self)
          break
        except BlockingIOError:
          if rt is not None:
            if t is None:
              rt0 = rt
              t = time.monotonic()
            else:
              rt = rt0 + t - time.monotonic()
          del self.gettimeout
          if self.events['a'].wait(rt):
            self.events['a'].clear()
            if self.closed:
              raise InterruptedError()
          else:
            break
        finally:
          try:
            del self.gettimeout
          except:
            pass
      if a is not None:
        isock = self.gen.wrap(a[0])
        isock.settimeout(self.timeout)
        return (isock, a[1])
      raise InterruptedError() if self.closed else TimeoutError()
    finally:
      self.unlock(ul)

  def connect(self, *args, timeout='', **kwargs):
    rt, ul =  self.lock(timeout, 'c')
    try:
      self.events['c'].clear()
      if self.closed:
        raise InterruptedError()
      try:
        socket.socket.connect(self, *args, **kwargs)
      except BlockingIOError:
        w = self.events['c'].wait(rt)
        self.events['c'].clear()
        if not w or self.closed:
          raise InterruptedError() if self.closed else TimeoutError()
        elif self.errors['c']:
          raise ConnectionRefusedError()
    finally:
      self.unlock(ul)

  @classmethod
  def waitmult(cls, *args, **kwargs):
    raise NotImplementedError()


class IDSocketGenerator(ISocketGenerator):

  CLASS = IDSocket

  def __init__(self):
    super().__init__()
    self.idsockets = self.isockets
    self.events = {m: threading.Event() for m in ('r', 'a', 'w', 'c')}

  def waitany(self, timeout, event):
    if not event in ('r', 'a', 'w', 'c') or self.closed:
      return ()
    self.events[event].clear()
    r = tuple(idsock for idsock in self.idsockets if not idsock.closed and idsock.events[event].is_set())
    if r:
      return r
    if self.events[event].wait(timeout) and not self.closed:
      self.events[event].clear()
      return tuple(idsock for idsock in self.idsockets if not idsock.closed and idsock.events[event].is_set())
    return ()


class NestedSSLContext(ssl.SSLContext):

  class SSLSocket(ssl.SSLSocket):

    _esocket = socket.socket()
    _esocket.detach()

    def __new__(cls, *args, **kwargs):
      if not hasattr(cls, 'sock'):
        raise TypeError('%s does not have a public constructor. Instances are returned by NestedSSLContext.wrap_socket().' % cls.__name__)
      cls_ = cls.__bases__[0]
      self = super(cls_, cls_).__new__(cls_, *args, **kwargs)
      self.socket = cls.sock
      cls.sock = None
      return self

    @classmethod
    def _create(cls, sock, *args, **kwargs):
      so = socket.socket(family=sock.family, type=sock.type, proto=sock.proto, fileno=sock.fileno())
      try:
        so.settimeout(sock.timeout)
      except:
        pass
      self = ssl.SSLSocket._create.__func__(type('BoundSSLSocket', (cls,), {'sock': sock}), so, *args, **kwargs)
      return self

    def detach(self):
      try:
        self.socket.detach()
      except:
        pass
      self._sslobj = None
      self.socket = self._esocket
      return super().detach()

    def unwrap(self):
      try:
        sock = super().unwrap()
        return sock
      finally:
        self.detach()

    def close(self):
      try:
        self.socket.close()
      except:
        pass
      self.detach()

    def shutdown(self, how):
      super().shutdown(how)
      try:
        self.socket.shutdown(how)
      except:
        pass

    def shutclose(self):
      try:
        if hasattr(self.socket, 'shutclose'):
          self.socket.shutclose()
        else:
          self.shutdown(socket.SHUT_RDWR)
          self.socket.close()
      except:
        pass
      self.detach()

    def settimeout(self, value):
      try:
        super().settimeout(value)
      except:
        pass
      try:
        self.socket.settimeout(value)
      except:
        pass

    def setblocking(self, flag):
      try:
        super().setblocking(flag)
      except:
        pass
      try:
        self.socket.setblocking(flag)
      except:
        pass

    def accept(self):
      sock, addr = self.socket.accept()
      sock = self.context.wrap_socket(sock, do_handshake_on_connect=self.do_handshake_on_connect, suppress_ragged_eofs=self.suppress_ragged_eofs, server_side=True)
      return sock, addr

    def connect(self, addr):
      if self.server_side:
        raise ValueError('can\'t connect in server-side mode')
      if self._connected or self._sslobj is not None:
        raise ValueError('attempt to connect already-connected SSLSocket!')
      self._sslobj = self.context._wrap_socket(self, False, self.server_hostname, owner=self, session=self._session)
      try:
        self.socket.connect(addr)
        self._connected = True
        if self.do_handshake_on_connect:
          self.do_handshake()
      except:
        self._sslobj = None
        raise

    def __del__(self):
      self.shutclose()
      super().__del__()

  sslsocket_class = SSLSocket
  ssl_read_ahead = 16384 + 2048

  class _SSLSocket():

    def __init__(self, context, ssl_sock, server_side, server_hostname):
      self.context = context
      self._sslsocket = weakref.ref(ssl_sock)
      self.inc = ssl.MemoryBIO()
      self.out = ssl.MemoryBIO()
      self.sslobj = context.wrap_bio(self.inc, self.out, server_side, server_hostname)

    @property
    def sslsocket(self):
      return self._sslsocket()

    def __getattr__(self, name):
      if name == 'is_isocket':
        self.is_isocket = isinstance(self.sslsocket.socket, ISocket)
        return self.is_isocket
      return self.sslobj._sslobj.__getattribute__(name)

    def __setattr__(self, name, value):
      if name in ('_sslsocket', 'is_isocket', 'inc', 'out', 'sslobj', 'context'):
        object.__setattr__(self, name, value)
      else:
        self.sslobj._sslobj.__setattr__(name, value)

    def _read_record(self, end_time, sto):
      bl = b''
      rt = None
      while len(bl) < 5:
        if end_time is not None:
          rt = end_time - time.monotonic()
          if rt < 0:
            raise TimeoutError(10060, 'timed out')
        if self.is_isocket:
          b_ = self.sslsocket.socket.recv(5 - len(bl), timeout=rt)
        else:
          if rt is not None and sto - rt > 0.005:
            sto = rt
            self.sslsocket.socket.settimeout(rt)
          b_ = self.sslsocket.socket.recv(5 - len(bl))
        if not b_:
          raise ConnectionResetError
        bl += b_
      l = int.from_bytes(bl[3:5], 'big')
      self.inc.write(bl)
      z = 0
      while l > 0:
        if end_time is not None:
          rt = max(end_time - time.monotonic(), z)
          if rt < 0:
            raise TimeoutError(10060, 'timed out')
          z = -1
        if self.is_isocket:
          b_ = self.sslsocket.socket.recv(l, timeout=rt)
        else:
          if rt is not None and sto - rt > 0.005:
            sto = rt
            self.sslsocket.socket.settimeout(rt)
          b_ = self.sslsocket.socket.recv(l)
        if not b_:
          raise ConnectionResetError
        l -= len(b_)
        self.inc.write(b_)
      return sto

    def interface(self, action, *args, **kwargs):
      rt = sto = timeout = self.sslsocket.gettimeout()
      end_time = None if timeout is None else timeout + time.monotonic()
      try:
        while True:
          try:
            res = action(*args, **kwargs)
          except (ssl.SSLWantReadError, ssl.SSLWantWriteError) as err:
            z = -1
            if self.out.pending:
              if end_time is not None:
                rt = end_time - time.monotonic()
                if rt < 0:
                  raise TimeoutError(10060, 'timed out')
                z = 0
              if self.is_isocket:
                self.sslsocket.socket.sendall(self.out.read(), timeout=rt)
              else:
                if rt is not None and sto - rt > 0.005:
                  sto = rt
                  self.sslsocket.socket.settimeout(rt)
                self.sslsocket.socket.sendall(self.out.read())
            elif err.errno == ssl.SSL_ERROR_WANT_WRITE:
              raise
            if err.errno == ssl.SSL_ERROR_WANT_READ:
              try:
                if self.context.ssl_read_ahead:
                  if end_time is not None:
                    rt = max(end_time - time.monotonic(), z)
                    if rt < 0:
                      raise TimeoutError(10060, 'timed out')
                  if self.is_isocket:
                    if not self.inc.write(self.sslsocket.socket.recv(self.context.ssl_read_ahead, timeout=rt)):
                      raise ConnectionResetError
                  else:
                    if rt is not None and sto - rt > 0.005:
                      sto = rt
                      self.sslsocket.socket.settimeout(rt)
                    if not self.inc.write(self.sslsocket.socket.recv(self.context.ssl_read_ahead)):
                      raise ConnectionResetError
                else:
                  sto = self._read_record(end_time, sto)
              except ConnectionResetError:
                if action == self.sslobj._sslobj.do_handshake:
                  raise ConnectionResetError(10054, 'An existing connection was forcibly closed by the remote host')
                else:
                  raise ssl.SSLEOFError(ssl.SSL_ERROR_EOF, 'EOF occurred in violation of protocol')
          else:
            if self.out.pending:
              if end_time is not None:
                rt = end_time - time.monotonic()
                if rt < 0:
                  raise TimeoutError(10060, 'timed out')
              if self.is_isocket:
                self.sslsocket.socket.sendall(self.out.read(), timeout=rt)
              else:
                if rt is not None and sto - rt > 0.005:
                  sto = rt
                  self.sslsocket.socket.settimeout(rt)
                self.sslsocket.socket.sendall(self.out.read())
            return res
      finally:
        if not self.is_isocket and timeout is not None:
          self.sslsocket.socket.settimeout(timeout)

    def do_handshake(self):
      return self.interface(self.sslobj._sslobj.do_handshake)

    def read(self, length=16384, buffer=None):
      return self.interface(self.sslobj._sslobj.read, length) if buffer is None else self.interface(self.sslobj._sslobj.read, length, buffer)

    def write(self, bytes):
      return self.interface(self.sslobj._sslobj.write, bytes)

    def shutdown(self):
      self.interface(self.sslobj._sslobj.shutdown)
      return self.sslsocket.socket

    def verify_client_post_handshake(self):
      return self.interface(self.sslobj._sslobj.verify_client_post_handshake)

  class _SSLDSocket(_SSLSocket):

    def __init__(self, context, ssl_sock, server_side, server_hostname):
      super().__init__(context, ssl_sock, server_side, server_hostname)
      self.rcondition = threading.Condition()
      self.rcounter = 0
      self.wlock = threading.Lock()

    def __setattr__(self, name, value):
      if name in ('_sslsocket', 'is_isocket', 'inc', 'out', 'sslobj', 'context', 'wlock', 'rcondition', 'rcounter'):
        object.__setattr__(self, name, value)
      else:
        self.sslobj._sslobj.__setattr__(name, value)

    def interface(self, action, *args, **kwargs):
      rt = sto = timeout = self.sslsocket.gettimeout()
      end_time = None if timeout is None else timeout + time.monotonic()
      try:
        while True:
          with self.rcondition:
            rc = 2 * (self.rcounter // 2)
          try:
            res = action(*args, **kwargs)
          except (ssl.SSLWantReadError, ssl.SSLWantWriteError) as err:
            z = -1
            if self.out.pending:
              if end_time is not None:
                rt = end_time - time.monotonic()
                if rt < 0 or not self.wlock.acquire(timeout=rt):
                  raise TimeoutError(10060, 'timed out')
              else:
                self.wlock.acquire()
              try:
                if end_time is not None:
                  rt = end_time - time.monotonic()
                  if rt < 0:
                    raise TimeoutError(10060, 'timed out')
                  z = 0
                b = self.out.read()
                if b:
                  if self.is_isocket:
                    self.sslsocket.socket.sendall(b, timeout=rt)
                  else:
                    if rt is not None and sto - rt > 0.005:
                      sto = rt
                      self.sslsocket.socket.settimeout(rt)
                    self.sslsocket.socket.sendall(b)
              finally:
                self.wlock.release()
            elif err.errno == ssl.SSL_ERROR_WANT_WRITE:
              raise
            if err.errno == ssl.SSL_ERROR_WANT_READ:
              with self.rcondition:
                if self.rcounter == rc:
                  self.rcounter += 1
                elif self.rcounter > rc + 1:
                  continue
                else:
                  if end_time is not None:
                    rt = max(end_time - time.monotonic(), z)
                    if rt < 0:
                      raise TimeoutError(10060, 'timed out')
                  self.rcondition.wait(rt)
                  continue
              try:
                if self.context.ssl_read_ahead:
                  if end_time is not None:
                    rt = max(end_time - time.monotonic(), z)
                    if rt < 0:
                      raise TimeoutError(10060, 'timed out')
                  if self.is_isocket:
                    if not self.inc.write(self.sslsocket.socket.recv(self.context.ssl_read_ahead, timeout=rt)):
                      raise ConnectionResetError
                  else:
                    if rt is not None and sto - rt > 0.005:
                      sto = rt
                      self.sslsocket.socket.settimeout(rt)
                    if not self.inc.write(self.sslsocket.socket.recv(self.context.ssl_read_ahead)):
                      raise ConnectionResetError
                else:
                  sto = self._read_record(end_time, sto)
              except ConnectionResetError:
                if action == self.sslobj._sslobj.do_handshake:
                  raise ConnectionResetError(10054, 'An existing connection was forcibly closed by the remote host')
                else:
                  raise ssl.SSLEOFError(ssl.SSL_ERROR_EOF, 'EOF occurred in violation of protocol')
              finally:
                with self.rcondition:
                  self.rcounter += 1
                  self.rcondition.notify_all()
          else:
            if self.out.pending:
              if end_time is not None:
                rt = end_time - time.monotonic()
                if rt < 0 or not self.wlock.acquire(timeout=rt):
                  raise TimeoutError(10060, 'timed out')
              else:
                self.wlock.acquire()
              try:
                if end_time is not None:
                  rt = end_time - time.monotonic()
                  if rt < 0:
                    raise TimeoutError(10060, 'timed out')
                b = self.out.read()
                if b:
                  if self.is_isocket:
                    self.sslsocket.socket.sendall(b, timeout=rt)
                  else:
                    if rt is not None and sto - rt > 0.005:
                      sto = rt
                      self.sslsocket.socket.settimeout(rt)
                    self.sslsocket.socket.sendall(b)
              finally:
                self.wlock.release()
            return res
      finally:
        if not self.is_isocket and timeout is not None:
          self.sslsocket.socket.settimeout(timeout)

  def __init__(self, *args, duplex=False, **kwargs):
    self.DefaultSSLContext = ssl.SSLContext(*args, **kwargs)
    ssl.SSLContext.__init__(*args, **kwargs)
    self.duplex = duplex

  def wrap_callable(self, name):
    def new_callable(*args, **kwargs):
      object.__getattribute__(self.DefaultSSLContext, name)(*args, **kwargs)
      return object.__getattribute__(self, name)(*args, **kwargs)
    return new_callable

  def __getattribute__(self, name):
    if not name in NestedSSLContext.__dict__ and type(object.__getattribute__(self, name)) in (types.BuiltinMethodType, types.MethodType):
      return self.wrap_callable(name)
    else:
      return object.__getattribute__(self, name)

  def __setattr__(self, name, value):
    object.__setattr__(self, name, value)
    if name != 'DefaultSSLContext':
      self.DefaultSSLContext.__setattr__(name, value)

  def wrap_socket(self, sock, *args, **kwargs):
    return ssl.SSLContext.wrap_socket(self.DefaultSSLContext if sock.__class__ == socket.socket and not self.duplex else self, sock, *args, **kwargs)

  def _wrap_socket(self, ssl_sock, server_side, server_hostname, *args, **kwargs):
    return (NestedSSLContext._SSLDSocket if self.duplex else NestedSSLContext._SSLSocket)(self, ssl_sock, server_side, server_hostname)

  def wrap_bio(self, *args, **kwargs):
    return self.DefaultSSLContext.wrap_bio(*args, **kwargs)


class HTTPExplodedMessage:

  __slots__ = ('method', 'path', 'version', 'code', 'message', 'headers', 'body', 'expect_close')

  def __init__(self):
    self.method = self.path = self.version = self.code = self.message = self.body = self.expect_close = None
    self.headers = {}

  def __bool__(self):
    return self.method is not None or self.code is not None

  def clear(self):
    self.__init__()
    return self

  def header(self, name, default=None):
    return self.headers.get(name.title(), default)

  def in_header(self, name, value):
    h = self.header(name)
    return False if h is None else (value.lower() in map(str.strip, h.lower().split(',')))

  def cookies(self, domain, path):
    hck = self.header('Set-Cookie')
    domain = domain.lower()
    dom_ip = all(c in '.:[]0123456789' for c in domain)
    path = path.rstrip('/') if (path != '/' and path[:1] == '/') else '/'
    ck = {}
    if hck is not None:
      hck = map(str.strip, hck.split('\n'))
      for co in hck:
        c = map(str.strip, co.split(';'))
        try:
          cn, cv = next(c).split('=', 1)
          if not cn:
            continue
          cd = cp = None
          for ca in c:
            try:
              can, cav = ca.split('=', 1)
            except:
              continue
            if cd is None and can.lower() == 'domain' and cav:
              cav = cav.lstrip('.').lower()
              if (domain != cav) if dom_ip else (not domain[-len(cav) - 1 :] in (cav, '.' + cav)):
                raise
              cd = (cav, True)
            if cp is None and can.lower() == 'path':
              if not path[: len(cav) + (1 if cav[-1:] != '/' else 0)] in (cav, cav + '/'):
                raise
              cp = cav
          if cd is None:
            cd = (domain, False)
          if cp is None:
            cp = ''
          ck[(cd, cp, cn)] = cv
        except:
          pass
    return ck

  def __repr__(self):
    if self:
      try:
        return '\r\n'.join(('<HTTPExplodedMessage at %#x>\r\n----------' % id(self), (' '.join(filter(None, (self.method, self.path, self.version, self.code, self.message)))), *('%s: %s' % (k, l) for k, v in self.headers.items() for l in v.split('\n')), ('----------\r\nStreaming body: ' + ('open' if next(c for c in self.body.__closure__ if type(c.cell_contents).__name__ == 'generator').cell_contents.gi_frame else 'closed')) if type(self.body).__name__ == 'function' else '----------\r\nLength of body: %s byte(s)' % len(self.body or ''), '----------\r\nClose expected: %s' % self.expect_close))
      except:
        return '<HTTPExplodedMessage at %#x>\r\n<corrupted object>' % id(self)
    else:
      return '<HTTPExplodedMessage at %#x>\r\n<no message>' % id(self)


class HTTPMessage:

  @staticmethod
  def _read_headers(msg, http_message):
    if not msg:
      return False
    a = None
    for msg_line in msg.replace('\r\n', '\n').split('\n')[:-2]:
      if a is None:
        try:
          a, b, c = msg_line.strip().split(None, 2)
        except:
          try:
            a, b, c = *msg_line.strip().split(None, 2), ''
          except:
            return False
      else:
        try:
          header_name, header_value = msg_line.split(':', 1)
        except:
          return False
        header_name = header_name.strip().title()
        if header_name:
          header_value = header_value.strip()
          if not header_name in ('Content-Length', 'Location', 'Host') and http_message.headers.get(header_name):
            if header_value:
              http_message.headers[header_name] += ('\n' if header_name in ('Set-Cookie', 'Www-Authenticate', 'Proxy-Authenticate') else ', ') + header_value
          else:
            http_message.headers[header_name] = header_value
        else:
          return False
    if a is None:
      return False
    if a[:4].upper() == 'HTTP':
      http_message.version = a.upper()
      http_message.code = b
      http_message.message = c
    else:
      http_message.method = a.upper()
      http_message.path = b
      http_message.version = c.upper()
    http_message.expect_close = http_message.in_header('Connection', 'close') or (http_message.version.upper() != 'HTTP/1.1' and not http_message.in_header('Connection', 'keep-alive'))
    return True

  @staticmethod
  def _read_trailers(msg, http_message):
    if not msg:
      return False
    for msg_line in msg.replace('\r\n', '\n').split('\n')[:-2]:
      try:
        header_name, header_value = msg_line.split(':', 1)
      except:
        return False
      header_name = header_name.strip().title()
      if header_name:
        if header_name in ('Transfer-Encoding', 'Content-Length', 'Host', 'Content-Encoding', 'Location'):
          continue
        header_value = header_value.strip()
        if http_message.headers.get(header_name):
          if header_value:
            http_message.headers[header_name] += ('\n' if header_name in ('Set-Cookie', 'Www-Authenticate', 'Proxy-Authenticate') else ', ') + header_value
        else:
          http_message.headers[header_name] = header_value
      else:
        return False
    return True

  @staticmethod
  def _read(message, max_data, end_time):
    try:
      if end_time is not None:
        rem_time = end_time - time.monotonic()
        if rem_time <= 0:
          return None
        if abs(message.gettimeout() - rem_time) > 0.005:
          message.settimeout(rem_time)
      return message.recv(min(max_data, 1048576))
    except:
      return None

  @staticmethod
  def _write(message, msg, end_time):
    try:
      if end_time is not None:
        rem_time = end_time - time.monotonic()
        if rem_time <= 0:
          return None
        if abs(message.gettimeout() - rem_time) > 0.005:
          message.settimeout(rem_time)
      message.sendall(msg)
      return len(msg)
    except:
      return None

  def __new__(cls, message=None, body=True, decompress=True, decode='utf-8', max_length=1048576, max_hlength=1048576, max_time=None, exceeded=None):
    http_message = HTTPExplodedMessage()
    if isinstance(exceeded, list):
      exceeded[:] = [False]
    else:
      exceeded = None
    if message is None:
      return http_message
    if max_time is False:
      max_time = None
    end_time = None if max_time is None else time.monotonic() + max_time
    iss = isinstance(message, socket.socket)
    max_hlength = min(max_length, max_hlength)
    rem_length = max_hlength
    if not iss:
      msg = message[0]
    else:
      msg = b''
      try:
        message.settimeout(max_time)
      except:
        return http_message
    while True:
      msg = msg.lstrip(b'\r\n')
      if msg and msg[0] < 0x20:
        return http_message
      body_pos = msg.find(b'\r\n\r\n')
      if body_pos >= 0:
        body_pos += 4
        break
      body_pos = msg.find(b'\n\n')
      if body_pos >= 0:
        body_pos += 2
        break
      if not iss or rem_length <= 0:
        return http_message
      try:
        bloc = cls._read(message, rem_length, end_time)
        if not bloc:
          return http_message
      except:
        return http_message
      rem_length -= len(bloc)
      msg = msg + bloc
    if not cls._read_headers(msg[:body_pos].decode('ISO-8859-1'), http_message):
      return http_message.clear()
    if not iss:
      http_message.expect_close = True
    if http_message.code in ('100', '101', '204', '304'):
      http_message.body = b''
      return http_message
    if not body:
      http_message.body = msg[body_pos:]
      return http_message
    rem_length += max_length - max_hlength
    chunked = http_message.in_header('Transfer-Encoding', 'chunked')
    if chunked:
      body_len = -1
    else:
      body_len = http_message.header('Content-Length')
      if body_len is None:
        if not iss or (http_message.code in ('200', '206') and http_message.expect_close):
          body_len = -1
        else:
          body_len = 0
      else:
        try:
          body_len = max(0, int(body_len))
        except:
          return http_message.clear()
    if decompress and body_len != 0:
      hce = [e for h in (http_message.header('Content-Encoding', ''), http_message.header('Transfer-Encoding', '')) for e in map(str.strip, h.lower().split(',')) if not e in ('chunked', '', 'identity')]
      for ce in hce:
        if not ce in ('deflate', 'gzip'):
          if http_message.method is not None and iss:
            try:
              cls._write(message, ('HTTP/1.1 415 Unsupported media type\r\nContent-Length: 0\r\nDate: %s\r\nCache-Control: no-cache, no-store, must-revalidate\r\n\r\n' % email.utils.formatdate(time.time(), usegmt=True)).encode('ISO-8859-1'), (time.monotonic() + 3) if end_time is None else min(time.monotonic() + 3, end_time))
            except:
              pass
          return http_message.clear()
    else:
      hce = []
    if http_message.in_header('Expect', '100-continue') and iss:
      if body_pos + body_len - len(msg) <= rem_length:
        try:
          if cls._write(message, 'HTTP/1.1 100 Continue\r\n\r\n'.encode('ISO-8859-1'), end_time) is None:
            return http_message.clear()
        except:
          return http_message.clear()
      else:
        try:
          cls._write(message, ('HTTP/1.1 413 Payload too large\r\nContent-Length: 0\r\nDate: %s\r\nCache-Control: no-cache, no-store, must-revalidate\r\n\r\n' % email.utils.formatdate(time.time(), usegmt=True)).encode('ISO-8859-1'), (time.monotonic() + 3) if end_time is None else min(time.monotonic() + 3, end_time))
        except:
          pass
        if exceeded is not None:
          exceeded[0] = True
        return http_message.clear()
    if not chunked:
      if body_len < 0:
        if not iss:
          http_message.body = msg[body_pos:]
        else:
          bbuf = BytesIO()
          rem_length -= bbuf.write(msg[body_pos:])
          while rem_length > 0:
            try:
              bw = bbuf.write(cls._read(message, rem_length, end_time))
              if not bw:
                break
              rem_length -= bw
            except:
              return http_message.clear()
          if rem_length <= 0:
            if exceeded is not None:
              exceeded[0] = True
            return http_message.clear()
          http_message.body = bbuf.getvalue()
      elif len(msg) < body_pos + body_len:
        if not iss:
          return http_message.clear()
        if body_pos + body_len - len(msg) > rem_length:
          if exceeded is not None:
            exceeded[0] = True
          return http_message.clear()
        bbuf = BytesIO()
        body_len -= bbuf.write(msg[body_pos:])
        while body_len:
          try:
            bw = bbuf.write(cls._read(message, body_len, end_time))
            if not bw:
              return http_message.clear()
            body_len -= bw
          except:
            return http_message.clear()
        http_message.body = bbuf.getvalue()
      else:
        http_message.body = msg[body_pos:body_pos+body_len]
    else:
      bbuf = BytesIO()
      buff = msg[body_pos:]
      while True:
        chunk_pos = -1
        rem_slength = max_hlength - len(buff)
        while chunk_pos < 0:
          buff = buff.lstrip(b'\r\n')
          chunk_pos = buff.find(b'\r\n')
          if chunk_pos >= 0:
            chunk_pos += 2
            break
          chunk_pos = buff.find(b'\n')
          if chunk_pos >= 0:
            chunk_pos += 1
            break
          if not iss or rem_slength <= 0:
            return http_message.clear()
          if rem_length <= 0:
            if exceeded is not None:
              exceeded[0] = True
            return http_message.clear()
          try:
            bloc = cls._read(message, min(rem_length, rem_slength), end_time)
            if not bloc:
              return http_message.clear()
          except:
            return http_message.clear()
          rem_length -= len(bloc)
          rem_slength -= len(bloc)
          buff = buff + bloc
        try:
          chunk_len = int(buff[:chunk_pos].split(b';', 1)[0].rstrip(b'\r\n'), 16)
          if not chunk_len:
            break
        except:
          return http_message.clear()
        if chunk_pos + chunk_len - len(buff) > rem_length:
          if exceeded is not None:
            exceeded[0] = True
          return http_message.clear()
        if len(buff) < chunk_pos + chunk_len:
          if not iss:
            return http_message.clear()
          chunk_len -= bbuf.write(buff[chunk_pos:])
          while chunk_len:
            try:
              bw = bbuf.write(cls._read(message, chunk_len, end_time))
              if not bw:
                return http_message.clear()
              chunk_len -= bw
            except:
              return http_message.clear()
            rem_length -= bw
          buff = b''
        else:
          bbuf.write(buff[chunk_pos:chunk_pos+chunk_len])
          buff = buff[chunk_pos+chunk_len:]
      http_message.body = bbuf.getvalue()
      rem_length = min(rem_length, max_hlength - body_pos - len(buff) + chunk_pos)
      while not (b'\r\n\r\n' in buff or b'\n\n' in buff):
        if not iss:
          return http_message.clear()
        if rem_length <= 0:
          if exceeded is not None:
            exceeded[0] = True
          return http_message.clear()
        try:
          bloc = cls._read(message, rem_length, end_time)
          if not bloc:
            return http_message.clear()
        except:
          return http_message.clear()
        rem_length -= len(bloc)
        buff = buff + bloc
      if len(buff) - chunk_pos > 2:
        cls._read_trailers(buff[chunk_pos:].decode('ISO-8859-1'), http_message)
    if http_message.body:
      try:
        if hce:
          for ce in hce[::-1]:
            if ce == 'deflate':
              try:
                http_message.body = zlib.decompress(http_message.body)
              except:
                http_message.body = zlib.decompress(http_message.body, wbits=-15)
            elif ce == 'gzip':
              http_message.body = gzip.decompress(http_message.body)
            else:
              raise
        if decode:
          http_message.body = http_message.body.decode(decode)
      except:
        if http_message.method is not None and iss:
          try:
            cls._write(message, ('HTTP/1.1 415 Unsupported media type\r\nContent-Length: 0\r\nDate: %s\r\nCache-Control: no-cache, no-store, must-revalidate\r\n\r\n' % email.utils.formatdate(time.time(), usegmt=True)).encode('ISO-8859-1'), (time.monotonic() + 3) if end_time is None else min(time.monotonic() + 3, end_time))
          except:
            pass
        return http_message.clear()
    return http_message


class HTTPStreamMessage(HTTPMessage):

  def __new__(cls, message=None, decompress=True, max_hlength=1048576, max_time=None):
    http_message = HTTPExplodedMessage()
    if message is None:
      return http_message
    if max_time is False:
      max_time = None
    end_time = None if max_time is None else time.monotonic() + max_time
    iss = isinstance(message, socket.socket)
    rem_length = max_hlength
    if not iss:
      msg = message[0]
    else:
      msg = b''
      try:
        message.settimeout(max_time)
      except:
        return http_message
    while True:
      msg = msg.lstrip(b'\r\n')
      body_pos = msg.find(b'\r\n\r\n')
      if body_pos >= 0:
        body_pos += 4
        break
      body_pos = msg.find(b'\n\n')
      if body_pos >= 0:
        body_pos += 2
        break
      if not iss or rem_length <= 0:
        return http_message
      try:
        bloc = cls._read(message, rem_length, end_time)
        if not bloc:
          return http_message
      except:
        return http_message
      rem_length -= len(bloc)
      msg = msg + bloc
    if not cls._read_headers(msg[:body_pos].decode('ISO-8859-1'), http_message):
      return http_message.clear()
    if not iss:
      http_message.expect_close = True
    if http_message.code in ('100', '101', '204', '304'):
      chunked = False
      body_len = 0
    else:
      chunked = http_message.in_header('Transfer-Encoding', 'chunked')
      if chunked:
        body_len = -1
      else:
        body_len = http_message.header('Content-Length')
        if body_len is None:
          if not iss or (http_message.code in ('200', '206') and http_message.expect_close):
            body_len = -1
          else:
            body_len = 0
        else:
          try:
            body_len = max(0, int(body_len))
          except:
            return http_message.clear()
    if decompress and body_len != 0:
      hce = [e for h in (http_message.header('Content-Encoding', ''), http_message.header('Transfer-Encoding', '')) for e in map(str.strip, h.lower().split(',')) if not e in ('chunked', '', 'identity')]
      for ce in hce:
        if not ce in ('deflate', 'gzip'):
          if http_message.method is not None and iss:
            try:
              cls._write(message, ('HTTP/1.1 415 Unsupported media type\r\nContent-Length: 0\r\nDate: %s\r\nCache-Control: no-cache, no-store, must-revalidate\r\n\r\n' % email.utils.formatdate(time.time(), usegmt=True)).encode('ISO-8859-1'), (time.monotonic() + 3) if end_time is None else min(time.monotonic() + 3, end_time))
            except:
              pass
          return http_message.clear()
      hce.reverse()
    else:
      hce = []
    rce = range(len(hce))
    if http_message.in_header('Expect', '100-continue') and iss:
      try:
        if cls._write(message, 'HTTP/1.1 100 Continue\r\n\r\n'.encode('ISO-8859-1'), end_time) is None:
          return http_message.clear()
      except:
        return http_message.clear()
    bbuf = ssl.MemoryBIO()
    def _body():
      def error(value=None):
        e = GeneratorExit()
        e.value = value or None
        raise e
      def decompress(data, i):
        if data:
          dec = hce[i]
          if isinstance(dec, str):
            if dec == 'deflate':
              if data[0] & 0x0e == 0x08:
                dec = hce[i] = zlib.decompressobj(wbits=15)
              else:
                dec = hce[i] = zlib.decompressobj(wbits=-15)
            elif dec == 'gzip':
                dec = hce[i] = zlib.decompressobj(wbits=31)
            else:
              raise
          return dec.decompress(data)
        else:
          return b''
      def bbuf_write(data):
        try:
          bbuf.write(reduce(decompress, rce, data))
        except:
          if http_message.method is not None and iss:
            try:
              cls._write(message, ('HTTP/1.1 415 Unsupported media type\r\nContent-Length: 0\r\nDate: %s\r\nCache-Control: no-cache, no-store, must-revalidate\r\n\r\n' % email.utils.formatdate(time.time(), usegmt=True)).encode('ISO-8859-1'), (time.monotonic() + 3) if end_time is None else min(time.monotonic() + 3, end_time))
            except:
              pass
          raise
        else:
          return len(data)
      nonlocal body_len
      nonlocal end_time
      if body_len != 0:
        length, max_time = yield None
        end_time = None if max_time is None else time.monotonic() + max_time
      else:
        return b''
      if not chunked:
        if body_len < 0:
          try:
            bbuf_write(msg[body_pos:])
          except:
            error()
          if iss:
            while True:
              while bbuf.pending > length:
                length, max_time = yield bbuf.read(length)
                end_time = None if max_time is None else time.monotonic() + max_time
              try:
                if max_time is not False:
                  message.settimeout(max_time)
                  max_time = False
                bw = bbuf_write(cls._read(message, 1048576, end_time))
                if not bw:
                  break
              except:
                if bbuf.pending == length:
                  length, max_time = yield bbuf.read(length)
                error(bbuf.read())
        elif len(msg) < body_pos + body_len:
          try:
            body_len -= bbuf_write(msg[body_pos:])
          except:
            error()
          if not iss:
            while bbuf.pending >= length:
              length, max_time = yield bbuf.read(length)
            error(bbuf.read())
          while body_len:
            while bbuf.pending >= length:
              length, max_time = yield bbuf.read(length)
              end_time = None if max_time is None else time.monotonic() + max_time
            try:
              if max_time is not False:
                message.settimeout(max_time)
                max_time = False
              bw = bbuf_write(cls._read(message, min(body_len, 1048576), end_time))
              if not bw:
                raise
              body_len -= bw
            except:
              error(bbuf.read())
        else:
          try:
            bbuf_write(msg[body_pos:body_pos+body_len])
          except:
            error()
        while bbuf.pending > length:
          length, max_time = yield bbuf.read(length)
          end_time = None if max_time is None else time.monotonic() + max_time
      else:
        buff = msg[body_pos:]
        while True:
          chunk_pos = -1
          rem_slength = max_hlength - len(buff)
          while chunk_pos < 0:
            buff = buff.lstrip(b'\r\n')
            chunk_pos = buff.find(b'\r\n')
            if chunk_pos >= 0:
              chunk_pos += 2
              break
            chunk_pos = buff.find(b'\n')
            if chunk_pos >= 0:
              chunk_pos += 1
              break
            if not iss or rem_slength <= 0:
              if bbuf.pending == length:
                length, max_time = yield bbuf.read(length)
              error(bbuf.read())
            try:
              if max_time is not False:
                message.settimeout(max_time)
                max_time = False
              bloc = cls._read(message, min(rem_slength, 1048576), end_time)
              if not bloc:
                raise
            except:
              if bbuf.pending == length:
                length, max_time = yield bbuf.read(length)
              error(bbuf.read())
            rem_slength -= len(bloc)
            buff = buff + bloc
          try:
            chunk_len = int(buff[:chunk_pos].split(b';', 1)[0].rstrip(b'\r\n'), 16)
            if not chunk_len:
              break
          except:
            if bbuf.pending == length:
              length, max_time = yield bbuf.read(length)
            error(bbuf.read())
          if len(buff) < chunk_pos + chunk_len:
            try:
              chunk_len -= bbuf_write(buff[chunk_pos:])
            except:
              error(bbuf.read())
            if not iss:
              while bbuf.pending >= length:
                length, max_time = yield bbuf.read(length)
              error(bbuf.read())
            while chunk_len:
              while bbuf.pending >= length:
                length, max_time = yield bbuf.read(length)
                end_time = None if max_time is None else time.monotonic() + max_time
              try:
                if max_time is not False:
                  message.settimeout(max_time)
                  max_time = False
                bw = bbuf_write(cls._read(message, min(chunk_len, 1048576), end_time))
                if not bw:
                  raise
                chunk_len -= bw
              except:
                error(bbuf.read())
            buff = b''
          else:
            try:
              bbuf_write(buff[chunk_pos:chunk_pos+chunk_len])
            except:
              error(bbuf.read())
            buff = buff[chunk_pos+chunk_len:]
          while bbuf.pending > length:
            length, max_time = yield bbuf.read(length)
            end_time = None if max_time is None else time.monotonic() + max_time
        while bbuf.pending > length:
          length, max_time = yield bbuf.read(length)
          end_time = None if max_time is None else time.monotonic() + max_time
        while not (b'\r\n\r\n' in buff or b'\n\n' in buff):
          if not iss:
            if bbuf.pending == length:
              length, max_time = yield bbuf.read(length)
            error(bbuf.read())
          try:
            if max_time is not False:
              message.settimeout(max_time)
              max_time = False
            bloc = cls._read(message, 1048576, end_time)
            if not bloc:
              raise
          except:
            if bbuf.pending == length:
              length, max_time = yield bbuf.read(length)
            error(bbuf.read())
          buff = buff + bloc
        if len(buff) - chunk_pos > 2:
          cls._read_trailers(buff[chunk_pos:].decode('ISO-8859-1'), http_message)
      if bbuf.pending:
        for dec in hce:
          if isinstance(dec, str):
            error(bbuf.read())
          elif not dec.eof:
            error(bbuf.read())
      return bbuf.read()
    bg = _body()
    def body(length=float('inf'), max_time=None, return_pending_on_error=False, *, callback=None):
      if math.isnan(body.__defaults__[0]):
        return None
      if max_time is False:
        max_time = None
      if not length:
        if body.__defaults__[0] == 0 and callback is not None:
          callback()
        return b''
      elif length > 0:
        try:
          return bg.send((length, max_time))
        except StopIteration as e:
          if callback is not None:
            callback()
          return e.value or b''
        except GeneratorExit as e:
          body.__defaults__ = (float('nan'), None, False)
          if callback is not None:
            callback()
          return e.value if return_pending_on_error else None
      elif length == float('-inf'):
        bg.close()
        if callback is not None:
          callback()
        return b''
      else:
        bg.close()
        body.__defaults__ = (float('nan'), None, False)
        if callback is not None:
          callback()
        return None
    http_message.body = body
    try:
      bg.send(None)
    except StopIteration:
      body.__defaults__ = (0, None, False)
    return http_message


class HTTPBaseRequest:

  RequestPattern = \
    '%s %s HTTP/1.1\r\n' \
    'Host: %s\r\n%s' \
    '\r\n'

  def __init_subclass__(cls, context_class=ssl.SSLContext, socket_source=socket):
    cls.SSLContext = context_class(ssl.PROTOCOL_TLS_CLIENT)
    cls.SSLContext.check_hostname = False
    cls.SSLContext.verify_mode = ssl.CERT_NONE
    cls.ConnectionGenerator = socket_source.create_connection

  @classmethod
  def connect(cls, url, url_p, headers, timeout, max_hlength, end_time, pconnection, ip):
    raise TypeError('the class HTTPBaseRequest is not intended to be instantiated directly')

  @staticmethod
  def _netloc_split(loc, def_port=''):
    n, s, p = loc.rpartition(':')
    return (n, p or def_port) if (s == ':' and ']' not in p) else (loc, def_port)

  @staticmethod
  def _rem_time(timeout, end_time):
    if end_time is not None:
      rem_time = end_time - time.monotonic()
      if timeout is not None:
        rem_time = min(timeout, rem_time)
    elif timeout is not None:
      rem_time = timeout
    else:
      rem_time = None
    if rem_time is not None and rem_time <= 0:
      raise TimeoutError()
    return rem_time

  def __new__(cls, url, method=None, headers=None, data=None, timeout=30, max_length=16777216, max_hlength=1048576, max_time=None, decompress=True, pconnection=None, retry=None, max_redir=5, unsecuring_redir=False, ip='', basic_auth=None, process_cookies=None):
    if url is None:
      return HTTPMessage()
    if method is None:
      method = 'GET' if data is None else 'POST'
    redir = 0
    exceeded = [False]
    try:
      url_p = urllib.parse.urlsplit(url, allow_fragments=False)
      if headers is None:
        headers = {}
      hitems = headers.items()
      if pconnection is None:
        pconnection = [None, {}, []]
        hccl = True
      else:
        l = len(pconnection)
        pconnection[0:3] = [pconnection[0] if l >= 1 else None, pconnection[1] if l >= 2 else {}, []]
        hccl = 'close' in (e.strip() for k, v in hitems if k.lower() == 'connection' for e in v.lower().split(','))
      if data:
        hexp = '100-continue' in (e.strip() for k, v in hitems if k.lower() == 'expect' for e in v.lower().split(','))
      else:
        hexp = False
      headers = {k: v for k, v in hitems if not k.lower() in ('host', 'content-length', 'connection', 'expect')}
      if hexp:
        headers['Expect'] = '100-continue'
      if not 'accept-encoding' in (k.lower() for k, v in hitems):
        headers['Accept-Encoding'] = 'identity, deflate, gzip' if decompress else 'identity'
      if data is not None:
        if not 'chunked' in (e.strip() for k, v in hitems if k.lower() == 'transfer-encoding' for e in v.lower().split(',')):
          headers['Content-Length'] = str(len(data))
      headers['Connection'] = 'close' if hccl else 'keep-alive'
      hauth = headers.get('Authorization')
    except:
      return HTTPMessage()
    if retry is None:
      retry = pconnection[0] is not None
    retried = not retry
    end_time = time.monotonic() + max_time if max_time is not None else None
    if process_cookies is None:
      process_cookies = basic_auth is not None
    cook = pconnection[1]
    auth = False
    while True:
      try:
        pconnection[2].append(url)
        ck = {}
        if process_cookies:
          domain = cls._netloc_split(url_p.netloc)[0].lower()
          dom_ip = all(c in '.:[]0123456789' for c in domain)
          path = url_p.path.split('#', 1)[0]
          path = path.rstrip('/') if (path != '/' and path[:1] == '/') else '/'
          for k, v in cook.items():
            if ((domain[-len(k[0][0]) - 1 :] in (k[0][0], '.' + k[0][0])) if (k[0][1] and not dom_ip) else (domain == k[0][0])) and path[: len(k[1]) + (1 if k[1][-1:] != '/' else 0)] in (k[1], k[1] + '/'):
              if (not k[2] in ck) or (len(k[0][0]) > len(ck[k[2]][1]) or (len(k[0][0]) == len(ck[k[2]][1]) and len(k[1]) >= len(ck[k[2]][2]))):
                ck[k[2]] = (v, k[0][0], k[1])
        path = cls.connect(url, url_p, headers, timeout, max_hlength if max_length < 0 else min(max_length, max_hlength), end_time, pconnection, ip)
        try:
          code = '100'
          rem_time = cls._rem_time(None, end_time)
          pconnection[0].settimeout(rem_time)
          msg = cls.RequestPattern % (method, path, url_p.netloc, ''.join(k + ': ' + v + '\r\n' for k, v in (headers if not ck else {**headers, 'Cookie': '; '.join(k + '=' + v[0] for k, v in ck.items())}).items()))
          if hexp and data:
            pconnection[0].sendall(msg.encode('iso-8859-1'))
            rem_time = cls._rem_time(3 if timeout is None else min(3, timeout), end_time)
            if max_length < 0:
              resp = HTTPStreamMessage(pconnection[0], decompress=Fals, max_hlength=max_hlength, max_time=rem_time)
            else:
              resp = HTTPMessage(pconnection[0], body=(method.upper() != 'HEAD'), decompress=False, decode=None, max_length=max_length, max_hlength=max_hlength, max_time=rem_time)
            code = resp.code
            if code is None:
              code = '100'
            if code == '100':
              rem_time = cls._rem_time(None, end_time)
              pconnection[0].settimeout(rem_time)
              pconnection[0].sendall(data)
          else:
            pconnection[0].sendall(msg.encode('iso-8859-1') + (data or b''))
          rem_time = cls._rem_time(None, end_time)
        except TimeoutError:
          raise
        except:
          if retried:
            raise
          retried = True
          try:
            pconnection[0].close()
          except:
            pass
          pconnection[0] = None
          pconnection[2].pop()
          continue
        while code == '100':
          rem_time = cls._rem_time(None, end_time)
          if max_length < 0:
            resp = HTTPStreamMessage(pconnection[0], decompress=decompress, max_hlength=max_hlength, max_time=rem_time)
          else:
            resp = HTTPMessage(pconnection[0], body=(method.upper() != 'HEAD'), decompress=decompress,decode=None, max_length=max_length, max_hlength=max_hlength, max_time=rem_time, exceeded=exceeded)
          code = resp.code
          if code == '100':
            redir += 1
            if redir > max_redir:
              raise
        if code is None:
          rem_time = cls._rem_time(None, end_time)
          if retried or exceeded == [True]:
            raise
          retried = True
          try:
            pconnection[0].close()
          except:
            pass
          pconnection[0] = None
          pconnection[2].pop()
          continue
        retried = not retry
        if process_cookies and resp.header('Set-Cookie') is not None:
          cook.update(resp.cookies(cls._netloc_split(url_p.netloc)[0], url_p.path.split('#', 1)[0]))
        if code == '401':
          if not auth and basic_auth is not None and any((l or 'basic')[:5].lower() == 'basic' for l in resp.header('WWW-Authenticate').split('\n')):
            auth = True
            headers['Authorization'] = 'Basic ' + base64.b64encode(basic_auth.encode('utf-8')).decode('utf-8')
            if headers['Connection'] == 'close' or resp.expect_close:
              pconnection[0] = None
          else:
            auth = False
            break
        elif code[:2] == '30' and code != '304':
          auth = False
          if resp.header('location'):
            url = urllib.parse.urljoin(url, resp.header('location'))
            urlo_p = url_p
            url_p = urllib.parse.urlsplit(url, allow_fragments=False)
            if headers['Connection'] == 'close' or resp.expect_close or (urlo_p.scheme.lower() != url_p.scheme.lower() or urlo_p.netloc != url_p.netloc):
              if not unsecuring_redir and urlo_p.scheme.lower() == 'https' and url_p.scheme.lower() != 'https':
                raise
              try:
                pconnection[0].close()
              except:
                pass
              pconnection[0] = None
              headers['Connection'] = 'close'
            redir += 1
            if redir > max_redir:
              break
            if code == '303':
              if method.upper() != 'HEAD':
                method = 'GET'
              data = None
              for k in list(headers.keys()):
                if k.lower() in ('transfer-encoding', 'content-length', 'content-type'):
                  del headers[k]
          else:
            raise
        else:
          auth = False
          break
      except:
        auth = False
        try:
          pconnection[0].close()
        except:
          pass
        pconnection[0] = None
        return HTTPMessage()
      finally:
        if not auth and 'Authorization' in headers:
          if hauth is not None:
            headers['Authorization'] = hauth
          else:
            del headers['Authorization']
    if max_length < 0:
      def callback():
        resp.body.__kwdefaults__['callback'] = None
        if headers['Connection'] == 'close' or resp.expect_close or math.isnan(resp.body.__defaults__[0]):
          try:
            pconnection[0].close()
          except:
            pass
          pconnection[0] = None
      resp.body.__kwdefaults__['callback'] = callback
      if method.upper() == 'HEAD':
        resp.body(float('-inf'))
      else:
        resp.body(0)
    else:
      if headers['Connection'] == 'close' or resp.expect_close:
        try:
          pconnection[0].close()
        except:
          pass
        pconnection[0] = None
    return resp


def HTTPRequestConstructor(socket_source=socket, proxy=None):
  if not proxy or not proxy.get('ip', None):
    class HTTPRequest(HTTPBaseRequest, context_class=NestedSSLContext if socket_source != socket else ssl.SSLContext, socket_source=socket_source):
      @classmethod
      def connect(cls, url, url_p, headers, timeout, max_hlength, end_time, pconnection, ip):
        if pconnection[0] is None:
          rem_time = cls._rem_time(timeout, end_time)
          if url_p.scheme.lower() == 'http':
            pconnection[0] = cls.ConnectionGenerator((url_p.hostname, url_p.port if url_p.port is not None else 80), timeout=rem_time, source_address=(ip, 0))
          elif url_p.scheme.lower() == 'https':
            pconnection[0] = cls.ConnectionGenerator((url_p.hostname, url_p.port if url_p.port is not None else 443), timeout=rem_time, source_address=(ip, 0))
            rem_time = cls._rem_time(timeout, end_time)
            pconnection[0].settimeout(rem_time)
            pconnection[0] = cls.SSLContext.wrap_socket(pconnection[0], server_side=False, server_hostname=cls._netloc_split(url_p.netloc)[0])
          else:
            raise
        if pconnection[0] is None:
          raise
        return (url_p.path + ('?' + url_p.query if url_p.query else '')).replace(' ', '%20') or '/'
  else:
    class HTTPRequest(HTTPBaseRequest, context_class=NestedSSLContext if socket_source != socket or proxy.get('secure', None) else ssl.SSLContext, socket_source=socket_source):
      PROXY = (proxy['ip'], proxy['port'])
      PROXY_AUTH = ('Basic ' + base64.b64encode(proxy['auth'].encode('utf-8')).decode('utf-8')) if proxy.get('auth', None) else ''
      PROXY_SECURE = bool(proxy.get('secure', None))
      PROXY_TUNNEL = bool(proxy.get('tunnel', None))
      @classmethod
      def connect(cls, url, url_p, headers, timeout, max_hlength, end_time, pconnection, ip):
        if pconnection[0] is None:
          rem_time = cls._rem_time(timeout, end_time)
          psock = cls.ConnectionGenerator(cls.PROXY, timeout=rem_time, source_address=(ip, 0))
          if cls.PROXY_SECURE:
            rem_time = cls._rem_time(timeout, end_time)
            psock.settimeout(rem_time)
            psock = cls.SSLContext.wrap_socket(psock, server_side=False, server_hostname=cls.PROXY[0])
          if url_p.scheme.lower() == 'http':
            if cls.PROXY_TUNNEL:
              rem_time = cls._rem_time(timeout, end_time)
              psock.settimeout(rem_time)
              psock.sendall(('CONNECT %s:%s HTTP/1.1\r\nHost: %s:%s\r\n%s\r\n' % (*(cls._netloc_split(url_p.netloc, '80') * 2), ('Proxy-Authorization: %s\r\n' % cls.PROXY_AUTH) if cls.PROXY_AUTH else '')).encode('iso-8859-1'))
              rem_time = cls._rem_time(timeout, end_time)
              if not HTTPMessage(psock, body=False, decompress=False, decode=None, max_hlength=max_hlength, max_time=rem_time).code in ('200', '204'):
                raise
            pconnection[0] = psock
          elif url_p.scheme.lower() == 'https':
            rem_time = cls._rem_time(timeout, end_time)
            psock.settimeout(rem_time)
            psock.sendall(('CONNECT %s:%s HTTP/1.1\r\nHost: %s:%s\r\n%s\r\n' % (*(cls._netloc_split(url_p.netloc, '443') * 2), ('Proxy-Authorization: %s\r\n' % cls.PROXY_AUTH) if cls.PROXY_AUTH else '')).encode('iso-8859-1'))
            rem_time = cls._rem_time(timeout, end_time)
            if not HTTPMessage(psock, body=False, decompress=False, decode=None, max_hlength=max_hlength, max_time=rem_time).code in ('200', '204'):
              raise
            rem_time = cls._rem_time(timeout, end_time)
            psock.settimeout(rem_time)
            pconnection[0] = cls.SSLContext.wrap_socket(psock, server_side=False, server_hostname=cls._netloc_split(url_p.netloc)[0])
          else:
            raise
        if pconnection[0] is None:
          raise
        if url_p.scheme.lower() == 'http' and not cls.PROXY_TUNNEL:
          if cls.PROXY_AUTH:
            headers['Proxy-Authorization'] = cls.PROXY_AUTH
          else:
            headers.pop('Proxy-Authorization', None)
        return ((url_p.path + ('?' + url_p.query if url_p.query else '')) if url_p.scheme.lower() != 'http' or cls.PROXY_TUNNEL else url).replace(' ', '%20') or '/'
  return HTTPRequest


class RSASelfSigned:

  def __init__(self, name, years):
    self.name = name
    self.years = years
    self.ready = threading.Event()

  def generate(self):
    pcbEncoded = DWORD(0)
    wcrypt.CertStrToNameW(DWORD(1), LPCWSTR('CN=' + self.name), DWORD(2), None, None, byref(pcbEncoded), None)
    pSubjectIssuerBlob = CRYPT_INTEGER_BLOB()
    pSubjectIssuerBlob.cbData = DWORD(pcbEncoded.value)
    pSubjectIssuerBlob.pbData = ctypes.cast(ctypes.create_string_buffer(pcbEncoded.value), PVOID)
    wcrypt.CertStrToNameW(DWORD(1), LPCWSTR('CN=' + self.name), DWORD(2), None, PVOID(pSubjectIssuerBlob.pbData), byref(pcbEncoded), None)
    phProvider = HANDLE(0)
    ncrypt.NCryptOpenStorageProvider(byref(phProvider), LPCWSTR('Microsoft Software Key Storage Provider'), DWORD(0))
    phKey = HANDLE(0)
    ncrypt.NCryptCreatePersistedKey(phProvider, byref(phKey), LPCWSTR('RSA'), None, DWORD(1), DWORD(0))
    ncrypt.NCryptSetProperty(phKey, LPCWSTR('Export Policy'), byref(ULONG(3)), 4, ULONG(0x80000000))
    ncrypt.NCryptSetProperty(phKey, LPCWSTR('Length'), byref(DWORD(2048)), 4, ULONG(0x80000000))
    ncrypt.NCryptFinalizeKey(phKey, DWORD(0x40))
    pKeyProvInfo = CRYPT_KEY_PROV_INFO()
    pKeyProvInfo.pwszContainerName = LPWSTR('CN=' + self.name)
    pKeyProvInfo.pwszProvName = LPWSTR('Microsoft Software Key Storage Provider')
    pKeyProvInfo.dwProvType = DWORD(0x01)
    pKeyProvInfo.dwFlags = DWORD(0x40)
    pKeyProvInfo.cProvParam = DWORD(0)
    pKeyProvInfo.rgProvParam = PVOID(0)
    pKeyProvInfo.dwKeySpec = DWORD(1)
    pSignatureAlgorithm = None
    pStartTime = P_SYSTEMTIME(SYSTEMTIME())
    kernel32.GetSystemTime(pStartTime)
    pEndTime = P_SYSTEMTIME(SYSTEMTIME())
    ctypes.memmove(pEndTime, pStartTime, ctypes.sizeof(SYSTEMTIME))
    pEndTime.contents.wYear += self.years
    if pEndTime.contents.wMonth == 2 and pEndTime.contents.wDay == 29:
      pEndTime.contents.wDay = 28
    pExtensions = CERT_EXTENSIONS()
    pExtensions.cExtension = 0
    pExtensions.rgExtension = PVOID(0)
    wcrypt.CertCreateSelfSignCertificate.restype = P_CERT_CONTEXT
    pCertContext = wcrypt.CertCreateSelfSignCertificate(phKey, pSubjectIssuerBlob, DWORD(0), pKeyProvInfo, pSignatureAlgorithm, pStartTime, pEndTime, pExtensions)
    self.cert = ctypes.string_at(pCertContext.contents.pbCertEncoded, pCertContext.contents.cbCertEncoded)
    pcbResult = DWORD(0)
    ncrypt.NCryptExportKey(phKey, None, LPCWSTR('PKCS8_PRIVATEKEY'), None, None, 0, byref(pcbResult), DWORD(0x40))
    pbOutput = ctypes.create_string_buffer(pcbResult.value)
    ncrypt.NCryptExportKey(phKey, None, LPCWSTR('PKCS8_PRIVATEKEY'), None, pbOutput, pcbResult, byref(pcbResult), DWORD(0x40))
    self.key = bytes(pbOutput)
    ncrypt.NCryptFreeObject(phProvider)
    ncrypt.NCryptDeleteKey(phKey, DWORD(0x40))
    wcrypt.CertFreeCertificateContext(pCertContext)

  def get_PEM(self):
    return ('-----BEGIN CERTIFICATE-----\r\n' + '\r\n'.join(textwrap.wrap(base64.b64encode(self.cert).decode('utf-8'), 64)) + '\r\n-----END CERTIFICATE-----\r\n', '-----BEGIN PRIVATE KEY-----\r\n' + '\r\n'.join(textwrap.wrap(base64.b64encode(self.key).decode('utf-8'), 64)) + '\r\n-----END PRIVATE KEY-----\r\n')

  def _pipe_PEM(self, certname, keyname, number=1):
    pipe_c = HANDLE(kernel32.CreateNamedPipeW(LPCWSTR('\\\\.\\pipe\\' + certname + ('.pem' if certname[:4].lower() != '.pem' else '')), DWORD(0x00000002), DWORD(0), DWORD(1), DWORD(0x100000), DWORD(0x100000), DWORD(0), HANDLE(0)))
    pipe_k = HANDLE(kernel32.CreateNamedPipeW(LPCWSTR('\\\\.\\pipe\\' + keyname + ('.pem' if keyname[:4].lower() != '.pem' else '')), DWORD(0x00000002), DWORD(0), DWORD(1), DWORD(0x100000), DWORD(0x100000), DWORD(0), HANDLE(0)))
    self.ready.set()
    pem = tuple(t.encode('utf-8') for t in self.get_PEM())
    n = DWORD(0)
    for i in range(number):
      for (p, v) in zip((pipe_c, pipe_k), pem):
        kernel32.ConnectNamedPipe(p, LPVOID(0))
        kernel32.WriteFile(p, ctypes.cast(v, LPCVOID), DWORD(len(v)), byref(n), LPVOID(0))
        kernel32.FlushFileBuffers(p)
        kernel32.DisconnectNamedPipe(p)
    kernel32.CloseHandle(pipe_c)
    kernel32.CloseHandle(pipe_k)

  def pipe_PEM(self, certname, keyname, number=1):
    pipe_thread = threading.Thread(target=self._pipe_PEM, args=(certname, keyname), kwargs={'number': number}, daemon=True)
    pipe_thread.start()
    self.ready.wait()

  def __enter__(self):
    self.generate()
    return self

  def __exit__(self, type, value, traceback):
    pass


class BaseIServer:

  def __new__(cls, *args, **kwargs):
    if cls is BaseIServer:
      raise TypeError('the class BaseIServer is not intended to be instantiated directly')
    return object.__new__(cls)

  def __init__(self, server_address, request_handler_class, allow_reuse_address=False, dual_stack=True, threaded=False, daemon_thread=False, isocket_gen_class=None):
    self.server_address = server_address
    self.request_handler_class = request_handler_class
    self.allow_reuse_address = allow_reuse_address
    self.dual_stack = dual_stack
    self.threaded = threaded
    self.daemon_thread = daemon_thread
    self.lock = threading.RLock()
    self.closed = None
    self.isocketgen = (isocket_gen_class or ISocketGenerator)()
    self.thread = None
    self.threads = set()
    self._server_initiate()

  def _server_close(self):
    self.isocketgen.close()

  def _process_request(self, request, client_address):
    try:
      self._handle_request(request, client_address)
    except:
      pass
    try:
      self._close_request(request)
    except:
      pass
    if self.threaded:
      with self.lock:
        self.threads.remove(threading.current_thread())

  def serve(self):
    with self.lock:
      if self.closed is not None:
        return
      self.thread = threading.current_thread()
      self.closed = False
    while not self.closed:
      try:
        request, client_address = self._get_request()
        if self.closed:
          break
        if self.threaded:
          th = threading.Thread(target=self._process_request, args=(request, client_address), daemon=self.daemon_thread)
          self.threads.add(th)
          th.start()
        else:
          self._process_request(request, client_address)
      except:
        pass

  def start(self):
    th = threading.Thread(target=self.serve)
    th.start()

  def _wait_threads(self, threads, timeout=None):
    rt = timeout
    if timeout is not None:
      t = time.monotonic()
    while True:
      if timeout is not None:
        rt = timeout + t - time.monotonic()
        if rt <= 0:
          return False
      with self.lock:
        for th in threads:
          break
        else:
          return True
      th.join(rt)

  def shutdown(self, block_on_close=True):
    with self.lock:
      if self.closed:
        return
      self.closed = True
    self._server_close()
    self.thread.join()
    self.thread = None
    if block_on_close and self.threaded:
      self._wait_threads(self.threads)

  def stop(self, block_on_close=True):
    self.shutdown()


class UDPIServer(BaseIServer):

  def __init__(self, server_address, request_handler_class, allow_reuse_address=False, multicast_membership=None, dual_stack=True, max_packet_size=65507, threaded=False, daemon_thread=False, isocket_gen_class=None):
    self.max_packet_size = max_packet_size
    self.multicast_membership = multicast_membership
    super().__init__(server_address, request_handler_class, allow_reuse_address, dual_stack, threaded, daemon_thread, isocket_gen_class)

  def _server_initiate(self):
    self.isocket = self.isocketgen(type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
    if self.allow_reuse_address or self.multicast_membership:
      self.isocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if self.dual_stack:
      self.isocket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
    self.isocket.bind(self.server_address)
    self.server_address = self.isocket.getsockname()
    if self.multicast_membership:
      self.isocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, struct.pack('4s4s', socket.inet_aton(self.multicast_membership), socket.inet_aton(self.server_address[0])))

  def _get_request(self):
    return self.isocket.recvfrom(self.max_packet_size)

  def _handle_request(self, request, client_address):
    self.request_handler_class((request, self.isocket), client_address, self)

  def _close_request(self, request):
    pass


class TCPIServer(BaseIServer):

  def __init__(self, server_address, request_handler_class, allow_reuse_address=False, dual_stack=True, request_queue_size=10, threaded=False, daemon_thread=False, isocket_gen_class=None, nssl_context=None):
    self.request_queue_size = request_queue_size
    self.nssl_context = nssl_context
    if self.nssl_context is True:
      cid = base64.b32encode(os.urandom(10)).decode('utf-8')
      self.nssl_context = NestedSSLContext(ssl.PROTOCOL_TLS_SERVER)
      with RSASelfSigned('TCPIServer' + cid, 1) as cert:
        cert.pipe_PEM('cert' + cid, 'key' + cid, 2)
        self.nssl_context.load_cert_chain(r'\\.\pipe\cert%s.pem' % cid, r'\\.\pipe\key%s.pem' % cid)
    super().__init__(server_address, request_handler_class, allow_reuse_address, dual_stack, threaded, daemon_thread, isocket_gen_class)

  def _server_initiate(self):
    self.isocket = self.isocketgen(type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
    if self.nssl_context:
      self.isocket = self.nssl_context.wrap_socket(self.isocket, server_side=True)
    if self.allow_reuse_address:
      self.isocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if self.dual_stack:
      self.isocket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
    self.isocket.bind(self.server_address)
    self.server_address = self.isocket.getsockname()
    self.isocket.listen(self.request_queue_size)

  def _get_request(self):
    return self.isocket.accept()

  def _handle_request(self, request, client_address):
    self.request_handler_class(request, client_address, self)

  def _close_request(self, request):
    request.shutclose()


class RequestHandler:

  def __init__(self, request, client_address, server):
    self.request = request
    self.client_address = client_address
    self.server = server
    self.address = (self.request if isinstance(self.request, socket.socket) else self.request[1]).getsockname()
    self.handle()

  def handle(self):
    closed = False
    while not closed and not self.server.closed:
      print(self.address, self.request)
      req = HTTPMessage(self.request, max_length=1073741824)
      if self.server.closed:
        break
      if req.expect_close:
        closed = True
      if not req.method:
        closed = True
        continue


class MultiUDPIServer(UDPIServer):

  def __init__(self, server_address, request_handler_class, allow_reuse_address=False, multicast_membership=None, dual_stack=True, max_packet_size=65507, threaded=False, daemon_thread=False, isocket_gen_class=None):
    if isinstance(server_address, int):
      server_address = tuple((ip, server_address) for ip in MultiUDPIServer.retrieve_ips())
    super().__init__(server_address, request_handler_class, allow_reuse_address, multicast_membership, dual_stack, max_packet_size, threaded, daemon_thread, isocket_gen_class)

  @staticmethod
  def retrieve_ips():
    s = ULONG(0)
    b = ctypes.create_string_buffer(s.value)
    while iphlpapi.GetIpAddrTable(b, byref(s), False) == 122:
      b = ctypes.create_string_buffer(s.value)
    r = ctypes.cast(b, P_MIB_IPADDRTABLE).contents
    n = r.dwNumEntries
    t = ctypes.cast(byref(r.table), POINTER(MIB_IPADDRROW * n)).contents
    return tuple(socket.inet_ntoa(e.dwAddr.to_bytes(4, 'little')) for e in t if e.wType & 1)

  def _server_initiate(self):
    self.isockets = tuple(self.isocketgen(type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP) for addr in self.server_address)
    for a, addr in enumerate(self.server_address):
      if self.allow_reuse_address or self.multicast_membership:
        self.isockets[a].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      if self.dual_stack:
        self.isockets[a].setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
      self.isockets[a].bind(addr)
    self.server_address = tuple(isock.getsockname() for isock in self.isockets)
    if self.multicast_membership:
      for a, addr in enumerate(self.server_address):
        self.isockets[a].setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, struct.pack('4s4s', socket.inet_aton(self.multicast_membership), socket.inet_aton(addr[0])))


  def _get_request(self, isocket):
    return isocket.recvfrom(self.max_packet_size)

  def _handle_request(self, request, client_address, isocket):
    self.request_handler_class((request, isocket), client_address, self)

  def _process_request(self, request, client_address, isocket):
    try:
      self._handle_request(request, client_address, isocket)
    except:
      pass
    if self.threaded:
      with self.lock:
        self.threads.remove(threading.current_thread())

  def serve(self):
    with self.lock:
      if self.closed is not None:
        return
      self.thread = threading.current_thread()
      self.closed = False
    while not self.closed:
      try:
        for isock in self.isocketgen.waitany(None, 'r'):
          request, client_address = self._get_request(isock)
          if self.closed:
            break
          if self.threaded:
            th = threading.Thread(target=self._process_request, args=(request, client_address, isock), daemon=self.daemon_thread)
            self.threads.add(th)
            th.start()
          else:
            self._process_request(request, client_address, isock)
      except:
        pass


class WebSocketHandler:

  FRAGMENT_FRAME = 1000000

  def __init__(self, connection, side='server'):
    self.connection = connection
    if not hasattr(self, 'path'):
      self.path = None
    self.inactive_maxtime = 180
    self.mask = side in ('client', 'c')
    self.text_message_only = False
    self.error = 0
    self.close_received = False
    self.close_sent = False
    self.close_requested = None
    self.closed = False
    self.buffer = bytearray()
    self.frame_type = None
    self.frame_length = None
    self.data_length = None
    self.message_type = None
    self.message_data = None
    self.message_ready = False
    self.ping_data = None
    self.pong_data = None
    self.close_data = None
    self.last_reception_time = None
    self.queue_lock = threading.Lock()
    self.ping_lock = threading.Lock()
    self.pending_pings = 0
    self.send_event = threading.Event()
    self.queue = []
    self.received_id = 0
    self.queued_id = 0
    self.sent_id = 0

  def connected_callback(self):
    pass

  def received_callback(self, id, data):
    pass

  def send_event_callback(self):
    pass

  def send_queued_callback(self, id):
    pass

  def sent_callback(self, id):
    pass

  def close_received_callback(self, code, data):
    pass

  def error_callback(self, error):
    pass

  def closed_callback(self):
    pass

  @staticmethod
  def xor32(mask, data):
    ld = len(data)
    if ld <= 1000000:
      l = (ld + 3) // 4
      m = int.from_bytes(mask * l, 'little')
      l *= 4
      return memoryview((int.from_bytes(data, 'little') ^ m).to_bytes(l, 'little'))[:ld]
    else:
      l = 250000
      m = int.from_bytes(mask * l, 'little')
      l = 1000000
      return memoryview(b''.join(((int.from_bytes(data[i:i+1000000], 'little') ^ m).to_bytes(l, 'little')) for i in range(0, ld, 1000000)))[:ld]

  def build_frame(self, type, data):
    opcodes = {'text_data': 0x01, 'binary_data': 0x02, 'close': 0x08, 'ping': 0x09, 'pong': 0x0a}
    if type == 'data':
      if isinstance(data, str):
        data_m = memoryview(data.encode('utf-8'))
        type = 'text_data'
      else:
        try:
          data_m = memoryview(data)
          type = 'binary_data'
        except:
          return None
    else:
      try:
        data_m = memoryview(data)
      except:
        return None
    if type not in opcodes:
      return None
    if self.mask:
      mask = os.urandom(4)
    opc = opcodes[type]
    if opc > 0x02:
      if len(data_m) <= 0x7d:
        return (struct.pack('BB4s', 0x80 + opcodes[type], 0x80 + len(data_m), mask) + WebSocketHandler.xor32(mask, data_m)) if self.mask else (struct.pack('BB', 0x80 + opcodes[type], len(data_m)) + data_m)
      else:
        return None
    data_f = tuple(data_m[i:i+self.FRAGMENT_FRAME] for i in range(0, len(data_m), self.FRAGMENT_FRAME))
    frames = []
    nf = len(data_f)
    fin = 0x00
    for f in range(nf):
      if f == 1:
        opc = 0x00
      if f == nf - 1:
        fin = 0x80
      df = data_f[f]
      if len(df) <= 0x7d:
        frames.append((struct.pack('BB4s', fin + opc, 0x80 + len(df), mask) + WebSocketHandler.xor32(mask, df)) if self.mask else (struct.pack('BB', fin + opc, len(df)) + df))
      elif len(df) <= 0xffff:
        frames.append((struct.pack('!BBH4s', fin + opc, 0xfe, len(df), mask) + WebSocketHandler.xor32(mask, df)) if self.mask else (struct.pack('!BBH', fin + opc, 0x7e, len(df)) + df))
      elif len(df) <= 0x7fffffffffffffff:
        frames.append((struct.pack('!BBQ4s', fin + opc, 0xff, len(df), mask) + WebSocketHandler.xor32(mask, df)) if self.mask else (struct.pack('!BBQ', fin + opc, 0x7f, len(df)) + df))
      else:
        return None
    return frames

  def send_ping(self):
    try:
      self.connection.sendall(self.build_frame('ping', b'ping'))
    except:
      return False
    return True

  def send_pong(self):
    with self.ping_lock:
      ping_data = self.ping_data
      if ping_data is None:
        return False
      self.ping_data = None
    try:
      self.connection.sendall(self.build_frame('pong', ping_data))
    except:
      return False
    return True

  def send_close(self, data=b''):
    try:
      self.connection.sendall(self.build_frame('close', data))
    except:
      return False
    return True

  def send_data(self, frame):
    try:
      self.connection.sendall(frame)
    except:
      return False
    return True

  def get_type(self):
    opcodes = {0x00: 'data', 0x01: 'data', 0x02: 'data', 0x08: 'close', 0x09: 'ping', 0x0a: 'pong'}
    if len(self.buffer) == 0:
      return False
    self.frame_type = opcodes.get(self.buffer[0] & 0x0f, 'bad')
    return True

  def get_length(self):
    if len(self.buffer) < 2:
      return False
    if self.buffer[1] & 0x7f <= 0x7d:
      self.data_length = self.buffer[1] & 0x7f
      self.frame_length = (2 if self.mask else 6) + self.data_length
    elif self.buffer[1] & 0x7f == 0x7e:
      if len(self.buffer) < 4:
        return False
      self.data_length = struct.unpack('!H', self.buffer[2:4])[0]
      self.frame_length = (4 if self.mask else 8) + self.data_length
    elif self.buffer[1] & 0x7f == 0x7f:
      if len(self.buffer) < 10:
        return False
      self.data_length = struct.unpack('!Q', self.buffer[2:10])[0]
      self.frame_length = (10 if self.mask else 14) + self.data_length
    return True

  def check_mask(self):
    if len(self.buffer) < 2:
      return False
    if self.buffer[1] >> 7 != 1:
      return False
    return True

  def get_data(self):
    if not self.frame_type or not self.frame_length or self.data_length is None:
      return False
    if len(self.buffer) < self.frame_length:
      return False
    if self.frame_type == 'data':
      if self.message_type is None:
        if self.buffer[0] & 0x0f not in (0x01, 0x02):
          return False
        else:
          self.message_type = {0x01: 'text', 0x02: 'binary'}[self.buffer[0] & 0x0f]
          self.message_data = []
      else:
        if self.buffer[0] & 0x0f in (0x01, 0x02):
          self.message_type = {0x01: 'text', 0x02: 'binary'}[self.buffer[0] & 0x0f]
          self.message_data = []
    if self.frame_type != 'data' and (self.buffer[0] >> 7 != 1 or self.data_length > 0x7d):
      return False
    with memoryview(self.buffer) as buff:
      if self.frame_type == 'data':
        dpos = self.frame_length - self.data_length
        self.message_data.append(buff[dpos:self.frame_length] if self.mask else WebSocketRequestHandler.xor32(buff[dpos-4:dpos].tobytes(), buff[dpos:self.frame_length]))
      elif self.frame_type == 'close':
        self.close_data = bytes(buff[2:self.frame_length] if self.mask else WebSocketRequestHandler.xor32(buff[2:6].tobytes(), buff[6:self.frame_length]))
      elif self.frame_type == 'ping':
        self.ping_lock.acquire()
        self.ping_data = bytes(buff[2:self.frame_length] if self.mask else WebSocketRequestHandler.xor32(buff[2:6].tobytes(), buff[6:self.frame_length]))
        self.ping_lock.release()
      elif self.frame_type == 'pong':
        self.pong_data = bytes(buff[2:self.frame_length] if self.mask else WebSocketRequestHandler.xor32(buff[2:6].tobytes(), buff[6:self.frame_length]))
      else:
        return False
    if self.frame_type == 'data' and self.buffer[0] >> 7 == 1:
      self.message_data = b''.join(self.message_data)
      if self.message_type == 'text':
        try:
          self.message_data = self.message_data.decode('utf-8')
        except:
          return False
      self.message_ready = True
    return True

  def purge_frame(self):
    self.frame_type = None
    del self.buffer[0:self.frame_length]
    self.frame_length = None
    self.data_length = None

  def send(self, data, track=False):
    if self.closed or self.close_received or self.close_requested is not None:
      return False
    frame = self.build_frame('data', data)
    if frame is None:
      return False
    with self.queue_lock:
      qid = self.queued_id
      self.queued_id += 1
      r = self.send_queued_callback(qid) if track else None
      self.queue.extend(frame)
    self.send_event.set()
    return True if r in (None, False) else r

  def close(self, data=b''):
    if isinstance(data, str):
      data = data.encode('utf-8')
    else:
      data = data or b''
    if len(data) <= 0x7d:
      self.close_requested = data
      self.send_event.set()
      return True
    return False

  def handle_out(self):
    self.send_event.set()
    while not self.closed:
      se = self.send_event.is_set()
      if se:
        self.send_event.clear()
      if self.close_received:
        if self.close_data is None:
          self.close_data = b''
        code = struct.unpack('!H', self.close_data[:2])[0] if len(self.close_data) >= 2 else 1005
        self.close_received_callback(code, self.close_data[2:])
        self.send_close(self.close_data[:2])
        self.close_data = None
        self.closed = True
        break
      if self.error:
        error = struct.pack('!H', self.error)
        self.error_callback(self.error)
        self.send_close(error)
        self.closed = True
        break
      if self.ping_data is not None:
        self.send_pong()
      if self.close_requested is not None:
        self.send_close((struct.pack('!H', 4000) + self.close_requested) if self.close_requested else b'')
        self.close_sent = True
        break
      if se:
        self.send_event_callback()
        if len(self.queue) > 0:
          frame = self.queue.pop(0)
          if not self.send_data(frame):
            self.error = 1002
            continue
          if frame[0] >> 7 :
            self.sent_callback(self.sent_id)
            self.sent_id += 1
        if len(self.queue) > 0:
          self.send_event.set()
      self.ping_lock.acquire()
      while self.pending_pings <= 1:
        rt = (self.pending_pings / 2 + 1) * self.inactive_maxtime / 2 + self.last_reception_time - time.monotonic()
        if rt <= 0:
          self.pending_pings += 1
          self.ping_lock.release()
          self.send_ping()
          self.ping_lock.acquire()
        else:
          break
      if self.pending_pings > 1:
        rt = self.inactive_maxtime / 2
      self.ping_lock.release()
      self.send_event.wait(rt)

  def handle(self):
    self.connected_callback()
    self.last_reception_time = time.monotonic()
    out_handler_thread = threading.Thread(target=self.handle_out)
    out_handler_thread.start()
    if self.FRAGMENT_FRAME <= 0x7d:
      chunk_size = self.FRAGMENT_FRAME + (2 if self.mask else 6)
    elif self.FRAGMENT_FRAME <= 0xffff:
      chunk_size = self.FRAGMENT_FRAME + (4 if self.mask else 8)
    else:
      chunk_size = self.FRAGMENT_FRAME + (10 if self.mask else 14)
    while not self.closed:
      if self.frame_type or not self.buffer:
        t = time.monotonic()
        rt = self.inactive_maxtime + self.last_reception_time - t
        self.connection.settimeout(max(rt, 0))
        chunk = None
        try:
          chunk = self.connection.recv(chunk_size)
        except:
          pass
        if not chunk:
          self.error = 1002
          self.send_event.set()
          break
        with self.ping_lock:
          self.last_reception_time = time.monotonic()
          self.pending_pings = 0
        self.buffer += chunk
      self.get_type()
      if self.frame_type == 'bad':
        self.error = 1002
        self.send_event.set()
        break
      if not self.get_length():
        continue
      if self.mask == self.check_mask():
        self.error = 1002
        self.send_event.set()
        break
      if len(self.buffer) < self.frame_length:
        continue
      if not self.get_data():
        self.error = 1002
        self.send_event.set()
        break
      if self.frame_type == 'close':
        if self.close_sent:
          self.closed = True
        else:
          self.close_received = True
          self.send_event.set()
        break
      elif self.frame_type == 'ping':
        self.send_event.set()
        self.purge_frame()
      elif self.frame_type == 'pong':
        self.purge_frame()
      elif self.frame_type == 'data':
        if self.message_ready:
          if self.text_message_only and self.message_type != 'text':
            self.error = 1003
            self.send_event.set()
            break
          self.received_callback(self.received_id, self.message_data)
          self.received_id += 1
          self.message_data = None
          self.message_ready = False
          self.message_type = None
        self.purge_frame()
    if out_handler_thread.is_alive():
      try:
        out_handler_thread.join()
      except:
        pass
    self.closed_callback()


class WebSocketDataStore:

  def __init__(self, incoming_event=None):
    self.outgoing = []
    self.outgoing_lock = threading.Lock()
    self.incoming = []
    self.incoming_text_only = False
    self.before_shutdown = None
    self.outgoing_condition = threading.Condition()
    if isinstance(incoming_event, threading.Event):
      self.incoming_event = incoming_event
    else:
      self.incoming_event = threading.Event()

  def notify_outgoing(self):
    with self.outgoing_condition:
      self.outgoing_condition.notify_all()

  def set_outgoing(self, ind, value, if_different = False):
    with self.outgoing_lock:
      if ind >= len(self.outgoing):
        self.outgoing.extend([(None, None)]*(ind - len(self.outgoing) + 1))
      if not if_different or value != self.outgoing[ind][1]:
        self.outgoing[ind] = ((0 if self.outgoing[ind][0] is None else (self.outgoing[ind][0] + 1)), value)
    self.notify_outgoing()

  def add_outgoing(self, value):
    with self.outgoing_lock:
      self.outgoing.append((0, value))
    self.notify_outgoing()

  def nest_outgoing(self, value):
    with self.outgoing_lock:
      if len(self.outgoing) == 0:
        self.outgoing.append((0, value))
      else:
        self.outgoing.append((0, self.outgoing[-1][1]))
        self.outgoing[-2] = ((0 if self.outgoing[-2][0] is None else (self.outgoing[-2][0] + 1)), value)
    self.notify_outgoing()

  def set_before_shutdown(self, value):
    self.before_shutdown = value

  def add_incoming(self, value):
    self.incoming.append(value)
    self.incoming_event.set()

  def get_incoming(self):
    if self.incoming:
      try:
        return self.incoming.pop(0)
      except:
        return None
    else:
      return None

  def wait_for_incoming_event(self, timeout=None, clear=None):
    if clear:
      self.incoming_event.clear()
    incoming_event = self.incoming_event.wait(timeout)
    if incoming_event:
      self.incoming_event.clear()
      return True
    else:
      return None


class WebSocketServerChannel:

  def __init__(self, path, datastore):
    self.path = path
    self.datastore = datastore
    self.closed = False
    self.handlers = {}


class WebSocketRequestHandler(RequestHandler, WebSocketHandler):

  def __init__(self, request, client_address, server):
    self.channel = None
    WebSocketHandler.__init__(self, request, 'server')
    self.inactive_maxtime = server.inactive_maxtime
    RequestHandler.__init__(self, request, client_address, server)

  def connected_callback(self):
    WebSocketHandler.connected_callback(self)
    if self.channel.datastore is not None:
      self.text_message_only = self.channel.datastore.incoming_text_only

  def received_callback(self, id, data):
    WebSocketHandler.received_callback(self, id, data)
    if not self.channel.closed and self.channel.datastore is not None:
      self.channel.datastore.add_incoming(data)

  def send_event_callback(self):
    WebSocketHandler.send_event_callback(self)
    if self.channel.datastore is None or not self.outgoing:
      return
    nb_values = len(self.channel.datastore.outgoing)
    for i in range(nb_values):
      if self.close_received or self.channel.closed:
        break
      if i == len(self.outgoing_seq):
        self.outgoing_seq.append(None)
      try:
        seq_value, data_value = self.channel.datastore.outgoing[i]
      except:
        break
      if seq_value != self.outgoing_seq[i]:
        if data_value is not None:
          self.send(data_value)
        self.outgoing_seq[i] = seq_value

  def send_queued_callback(self, id):
    WebSocketHandler.send_queued_callback(self, id)
    if self.channel.datastore is None:
      qe = threading.Event()
      self.queued_events[id] = qe
      return qe

  def sent_callback(self, id):
    WebSocketHandler.sent_callback(self, id)
    if self.channel.datastore is None:
      qe = self.queued_events.pop(id, None)
      if qe is not None:
        qe.set()

  def error_callback(self, error):
    WebSocketHandler.error_callback(self, error)

  def close_received_callback(self, code, data):
    WebSocketHandler.close_received_callback(self, code, data)

  def closed_callback(self):
    WebSocketHandler.closed_callback(self)

  def handle(self):
    if self.server.closed:
      return
    resp_err_br = \
      'HTTP/1.1 400 Bad Request\r\n' \
      'Content-Length: 0\r\n' \
      'Connection: close\r\n' \
      '\r\n'
    resp_err_nf = \
      'HTTP/1.1 404 File not found\r\n' \
      'Content-Length: 0\r\n' \
      'Connection: close\r\n' \
      '\r\n'
    req = HTTPMessage(self.request)
    if req.method != 'GET' or not req.in_header('Upgrade', 'websocket') or not req.header('Sec-WebSocket-Key'):
      try:
        self.request.sendall(resp_err_br.encode('ISO-8859-1'))
      except:
        pass
      return
    path = req.path.lstrip('/').strip()
    with self.server.lock:
      self.channel = self.server.channels.get(path, None) or self.server.channels.get(path.split('?', 1)[0], None)
      if self.channel is not None:
        self.path = path
        if self.channel.datastore is None:
          self.queued_events = {}
        else:
          self.outgoing_seq = []
          self.outgoing = True
        self.channel.handlers[self] = threading.current_thread()
    if self.channel is None:
      try:
        self.request.sendall(resp_err_nf.encode('ISO-8859-1'))
      except:
        pass
      return
    guid = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    sha1 = hashlib.sha1((req.header('Sec-WebSocket-Key') + guid).encode('utf-8')).digest()
    ws_acc = base64.b64encode(sha1).decode('utf-8')
    resp= \
      'HTTP/1.1 101 Switching Protocols\r\n' \
      'Upgrade: websocket\r\n' \
      'Connection: Upgrade\r\n' \
      'Sec-WebSocket-Accept: %s\r\n' \
      '\r\n' % (ws_acc)
    try:
      self.request.sendall(resp.encode('ISO-8859-1'))
    except:
      with self.server.lock:
        del self.channel.handlers[self]
      return
    WebSocketHandler.handle(self)
    with self.server.lock:
      del self.channel.handlers[self]


class WebSocketIDServer(TCPIServer):

  def __init__(self, server_address, allow_reuse_address=False, dual_stack=True, request_queue_size=100, daemon_thread=False, inactive_maxtime=180, nssl_context=None):
    if nssl_context is True:
      cid = base64.b32encode(os.urandom(10)).decode('utf-8')
      nssl_context = NestedSSLContext(ssl.PROTOCOL_TLS_SERVER, duplex=True)
      with RSASelfSigned('TCPIServer' + cid, 1) as cert:
        cert.pipe_PEM('cert' + cid, 'key' + cid, 2)
        nssl_context.load_cert_chain(r'\\.\pipe\cert%s.pem' % cid, r'\\.\pipe\key%s.pem' % cid)
    elif nssl_context is not None:
      nssl_context.duplex = True
    super().__init__(server_address, WebSocketRequestHandler, allow_reuse_address, dual_stack, request_queue_size, True, daemon_thread, IDSocketGenerator, nssl_context)
    self.address = server_address
    self.channels = {}
    self.inactive_maxtime = inactive_maxtime
    self.idsocket = self.isocket

  def _sendevents_dispatcher(self, channel):
    with channel.datastore.outgoing_condition:
      while not channel.closed:
        for h in channel.handlers:
          h.outgoing = True
          h.send_event.set()
        channel.datastore.outgoing_condition.wait()

  def open(self, path, datastore=None):
    path = path.lstrip('/').strip()
    with self.lock:
      if self.closed:
        return False
      channel = WebSocketServerChannel(path, datastore)
      if self.channels.setdefault(path, channel) is not channel:
        return False
      if channel.datastore is not None:
        t = threading.Thread(target=self._sendevents_dispatcher, args=(channel,), daemon=self.daemon_thread)
        t.start()
    return True

  def _close(self, channel, timeout, block):
    if channel.datastore is not None:
      try:
        channel.datastore.notify_outgoing()
      except:
        pass
    if not self._wait_threads(channel.handlers.values(), timeout):
      with self.lock:
        for idsock in channel.idsockets:
          idsock.shutclose()
      if block:
        self._wait_threads(channel.handlers.values)
    if not block:
      with self.lock:
        self.threads.remove(threading.current_thread())

  def close(self, path, data=b'', timeout=None, block_on_close=False):
    path = path.lstrip('/').strip()
    with self.lock:
      channel = self.channels.pop(path, None)
      if channel is None or channel.closed:
        return False
      channel.closed = True
      if channel.datastore is not None:
        data = channel.datastore.before_shutdown
      if isinstance(data, str):
        data = data.encode('utf-8')
      else:
        data = data or b''
      data = data[:0x7d]
      for h in channel.handlers:
        h.close(data)
    if block_on_close:
      self._close(channel, timeout, True)
    else:
      th = threading.Thread(target=self._close, args=(channel, timeout, False), daemon=self.daemon_thread)
      self.threads.add(th)
      th.start()
    return True

  def sendto(self, path, data, handler, track=False):
    path = path.lstrip('/').strip()
    with self.lock:
      channel = self.channels.get(path, None)
      if channel is None or channel.closed:
        return False
    if not handler in channel.handlers:
      return False
    return handler.send(data, track)

  def broadcast(self, path, data):
    path = path.lstrip('/').strip()
    with self.lock:
      channel = self.channels.get(path, None)
      if channel is None or channel.closed:
        return False
      handlers = list(channel.handlers)
    for handler in handlers:
      handler.send(data)

  def _shutdown(self, timeout, block):
    w = self._wait_threads(self.threads, timeout)
    self._server_close()
    if block and not w:
      self._wait_threads(self.threads)

  def shutdown(self, timeout=None, block_on_close=True):
    if timeout is not None:
      t = time.monotonic()
    with self.lock:
      if self.closed:
        return
      self.closed = True
      self.idsocket.close()
      pathes = list(self.channels.keys())
    for path in pathes:
      self.close(path, timeout=timeout, block_on_close=False)
    self.thread.join()
    self.thread = None
    rt = None if timeout is None else timeout + t - time.monotonic()
    if block_on_close:
      self._shutdown(rt, True)
    else:
      th = threading.Thread(target=self._shutdown, args=(rt, False), daemon=self.daemon_thread)
      th.start()


class WebSocketIDClient(WebSocketHandler):

  def __new__(cls, channel_address, datastore=None, own_address='', connection_timeout=3, daemon_thread=False, inactive_maxtime=180, proxy=None, idsocket_generator=None):
    self = object.__new__(cls)
    self.channel_address = channel_address
    ca_p = urllib.parse.urlsplit(channel_address, allow_fragments=False)
    channel_address = urllib.parse.urlunsplit(ca_p._replace(scheme=ca_p.scheme.replace('ws', 'http')))
    self.path = (ca_p.path + ('?' + ca_p.query if ca_p.query else '')).replace(' ', '%20').lstrip('/').strip()
    self.idsocketgen = idsocket_generator if isinstance(idsocket_generator, IDSocketGenerator) else IDSocketGenerator()
    self.pconnection = [None]
    key = base64.b64encode(os.urandom(16)).decode('utf-8')
    guid = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    sha1 = hashlib.sha1((key + guid).encode('utf-8')).digest()
    ws_acc = base64.b64encode(sha1).decode('utf-8')
    if proxy is not None:
      proxy['tunnel'] = True
    HTTPRequest = HTTPRequestConstructor(self.idsocketgen, proxy)
    HTTPRequest.SSLContext.duplex = True
    rep = HTTPRequest(channel_address, headers={'Upgrade': 'websocket', 'Connection': 'Upgrade', 'Sec-WebSocket-Version': '13', 'Sec-WebSocket-Key': key}, max_time=connection_timeout, decompress=False, pconnection=self.pconnection, max_redir=0, ip=own_address)
    if rep.code != '101' or not rep.in_header('Upgrade', 'websocket') or rep.header('Sec-WebSocket-Accept') != ws_acc or rep.expect_close:
      return None
    self.pconnection[0].settimeout(None)
    return self

  def __init__(self, channel_address, datastore=None, own_address=None, connection_timeout=3, daemon_thread=False, inactive_maxtime=180, proxy=None):
    self.idsocket = self.pconnection[0]
    WebSocketHandler.__init__(self, self.idsocket, 'client')
    self.datastore = datastore
    self.daemon_thread = daemon_thread
    if self.datastore is not None:
      self.outgoing_seq = []
      self.outgoing = True
    else:
      self.queued_events = {}
    self.inactive_maxtime = inactive_maxtime
    self.address = self.idsocket.getsockname()
    self.thread = threading.Thread(target=WebSocketHandler.handle, args=(self,), daemon=self.daemon_thread)
    self.thread.start()

  def connected_callback(self):
    WebSocketHandler.connected_callback(self)
    if self.datastore is not None:
      self.text_message_only = self.datastore.incoming_text_only
      t = threading.Thread(target=self._sendevent_dispatcher, daemon=self.daemon_thread)
      t.start()

  def received_callback(self, id, data):
    WebSocketHandler.received_callback(self, id, data)
    if self.datastore is not None:
      self.datastore.add_incoming(data)

  def send_event_callback(self):
    WebSocketHandler.send_event_callback(self)
    if self.datastore is None or not self.outgoing:
      return
    nb_values = len(self.datastore.outgoing)
    for i in range(nb_values):
      if self.close_received:
        break
      if i == len(self.outgoing_seq):
        self.outgoing_seq.append(None)
      try:
        seq_value, data_value = self.datastore.outgoing[i]
      except:
        break
      if seq_value != self.outgoing_seq[i]:
        if data_value is not None:
          self.send(data_value)
        self.outgoing_seq[i] = seq_value

  def send_queued_callback(self, id):
    WebSocketHandler.send_queued_callback(self, id)
    if self.datastore is None:
      qe = threading.Event()
      self.queued_events[id] = qe
      return qe

  def sent_callback(self, id):
    WebSocketHandler.sent_callback(self, id)
    if self.datastore is None:
      qe = self.queued_events.pop(id, None)
      if qe is not None:
        qe.set()

  def error_callback(self, error):
    WebSocketHandler.error_callback(self, error)

  def close_received_callback(self, code, data):
    WebSocketHandler.close_received_callback(self, code, data)

  def closed_callback(self):
    WebSocketHandler.closed_callback(self)
    try:
      self.idsocket.shutclose()
    except:
      pass
    if self.datastore is not None:
      try:
        self.datastore.notify_outgoing()
      except:
        pass
    self.pconnection = [None]

  def _sendevent_dispatcher(self):
    with self.datastore.outgoing_condition:
      while not self.closed and self.close_requested is None:
        self.outgoing = True
        self.send_event.set()
        self.datastore.outgoing_condition.wait()

  def _close(self, timeout, block):
    if self.datastore is not None:
      try:
        self.datastore.notify_outgoing()
      except:
        pass
    self.thread.join(timeout)
    if self.thread.is_alive():
      self.idsocket.shutclose()
      if block:
        self.thread.join()
    self.thread = None

  def close(self, data=b'', timeout=None, block_on_close=False):
    WebSocketHandler.close(self, data if self.datastore is None else (self.datastore.before_shutdown or b''))
    if block_on_close:
      self._close(timeout, True)
    else:
      th = threading.Thread(target=self._close, args=(timeout, False), daemon=self.daemon_thread)
      th.start()


class NTPClient:

  def __init__(self, server='time.windows.com'):
    self.server = server
    self.isocketgen = ISocketGenerator()

  def query(self, timeout=None):
    try:
      isocket = self.isocketgen(type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
      if not isocket:
        raise
      isocket.settimeout(timeout)
    except:
      return None
    tc1 = time.time()
    try:
      isocket.sendto(struct.pack('>40s2L', b'\x1b', int(tc1 + 2208988800), int((tc1 % 1) * 4294967296)), (self.server, 123))
      r = isocket.recv(48)
      if len(r) < 48:
        raise
    except:
      return None
    finally:
      isocket.shutclose()
    ts = struct.unpack('>4L', r[32:48])
    ts1 = ts[0] - 2208988800 + ts[1] / 4294967296
    ts2 = ts[2] - 2208988800 + ts[3] / 4294967296
    tc2 = time.time()
    return tc1, ts1, ts2, tc2

  def get_time(self, to_local=False, timeout=None):
    try:
      tc1, ts1, ts2, tc2 = self.query(timeout)
    except:
      return None
    if to_local:
      try:
        return datetime.datetime.fromtimestamp(ts2).strftime("%x %X.%f")[:-3]
      except:
        return None
    return ts2

  def get_offset(self, timeout=None):
    try:
      tc1, ts1, ts2, tc2 = self.query(timeout)
    except:
      return None
    return (ts1 - tc1 + ts2 - tc2) / 2

  def close(self):
    try:
      self.isocketgen.close()
    except:
      pass

  def __enter__(self):
    return self

  def __exit__(self, et, ev, tb):
    self.close()


class TOTPassword:

  def __new__(cls, key, password_length=6, time_origin=0, time_interval=30, ntp_server='', ntp_timeout=None):
    if ntp_server is None:
      to = 0
    else:
      with (NTPClient(ntp_server) if ntp_server else NTPClient()) as ntpc:
        to = ntpc.get_offset(ntp_timeout)
      if to is None:
        return None
    self = object.__new__(cls)
    self.to = to
    return self

  def __init__(self, key, password_length=6, time_origin=0, time_interval=30, **kwargs):
    self.key = base64.b32decode(key)
    self.origin = time_origin
    self.interval = time_interval
    self.length = password_length

  def get(self, clipboard=False):
    t = time.time() + self.to - self.origin
    d = hmac.digest(self.key, int(t / self.interval).to_bytes(8, 'big', signed=False), "sha1")
    o = d[-1] & 0xf
    p = str((int.from_bytes(d[o:o+4], 'big', signed=False) & 0x7fffffff) % (10 ** self.length)).rjust(self.length, '0')
    if clipboard:
      subprocess.run('<nul set /P ="%s"| clip' % p, shell=True)
    return p, self.interval - int(t % self.interval)

  def __enter__(self):
    return self

  def __exit__(self, et, ev, tb):
    self.key = b''