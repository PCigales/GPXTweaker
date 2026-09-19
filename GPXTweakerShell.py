from wic import *
from wic import _COMMeta, _COM_IShellExtInit, _COM_IShellPropSheetExt, _COM_IShellPropSheetExt_impl, _COM_IInitializeWithStream, _COM_IPropertyStoreCapabilities, _COM_IPropertyStoreDelegating, _COM_IPropertyHandler_impl, _SPSUtil
import GPXTweaker

FR_STRINGS = {
  'Path': 'Chemin',
  'Track': 'Trace',
  'track': 'trace',
  'Name': 'Nom',
  'trackname': 'nom-trace',
  'Trackname': 'Nom trace',
  'Description': 'Description',
  'trackdescription': 'description-trace',
  'Trackdescription': 'Description trace',
  'Start': 'Début',
  'trackstart': 'début-trace',
  'Trackstart': 'Début trace',
  'End': 'Fin',
  'trackend': 'fin-trace',
  'Trackend': 'Fin trace',
  'Duration': 'Durée',
  'trackduration': 'durée-trace',
  'Trackduration': 'Durée trace',
  'Distance': 'Distance',
  'trackdistance': 'distance-trace',
  'Trackdistance': 'Distance trace',
  'EleGain': 'Dénivelé élé',
  'trackelegain': 'dénivelé-élé-trace',
  'Trackelegain': 'Dénivelé élé trace',
  'AltGain': 'Dénivelé alt',
  'trackaltgain': 'dénivelé-alt-trace',
  'Trackaltgain': 'Dénivelé alt trace',
  'Waypoints': 'Points de cheminement',
  'trackwpts': 'repère-trace | repères-trace',
  'Trackwpts': 'Repères trace',
  'segment': 'segment',
  'point': 'point',
  'h': 'h',
  'mn': 'mn',
  's': 's',
  'km': 'km',
  'm': 'm',
  'Errtitle': 'Action interrompue',
  'Errmsg': 'Une erreur vous empêche d\'appliquer des propriétés au fichier',
  'Error': 'Erreur',
  'Retry': 'Réessayer'
}

EN_STRINGS = {
  'Path': 'Path',
  'Track': 'Track',
  'track': 'track',
  'Name': 'Name',
  'trackname': 'track-name',
  'Trackname': 'Track name',
  'Description': 'Description',
  'trackdescription': 'track-description',
  'Trackdescription': 'Track description',
  'Start': 'Start',
  'trackstart': 'track-start',
  'Trackstart': 'Track start',
  'End': 'End',
  'trackend': 'track-end',
  'Trackend': 'Track end',
  'Duration': 'Duration',
  'trackduration': 'track-duration',
  'Trackduration': 'Track duration',
  'Distance': 'Distance',
  'trackdistance': 'track-distance',
  'Trackdistance': 'Track distance',
  'EleGain': 'Ele gain',
  'trackelegain': 'track-ele-gain',
  'Trackelegain': 'Track ele gain',
  'AltGain': 'Alt gain',
  'trackaltgain': 'track-alt-gain',
  'Trackaltgain': 'Track alt gain',
  'Waypoints': 'Waypoints',
  'trackwpts': 'track-waypoint | track-waypoints',
  'Trackwpts': 'Track waypoints',
  'segment': 'segment',
  'point': 'point',
  'h': 'h',
  'mn': 'mn',
  's': 's',
  'km': 'km',
  'm': 'm',
  'Errtitle': 'Interrupted action',
  'Errmsg': 'An error is keeping you from applying properties to the file',
  'Error': 'Error',
  'Retry': 'Retry'
}

LSTRINGS = EN_STRINGS
try:
  if GPXTweaker.locale.getlocale()[0][:2].lower() == 'fr':
    LSTRINGS = FR_STRINGS
except:
  pass

class _COM_IGPXShellPropSheetExt(_COM_IShellPropSheetExt):
  Title = 'GPX'
  @classmethod
  def GPXTemplate(cls, file, content, readonly):
    nbtrk = 1
    nbvtrk = 0
    trk = 0
    trck = None
    tconts = []
    tnames = []
    tdescs = []
    twpts = None
    tstarts = []
    tends = []
    tdurs = []
    tdists = []
    tegains = []
    tagains = []
    while trk < nbtrk:
      track = GPXTweaker.WGS84PropertiesTrack()
      trck = trck or track
      if not track.LoadGPX(content, trk, trck, 'f'):
        if trck.Wpts is None:
          nbtrk = 0
          break
        tconts.append(None)
        tnames.append(None)
        tdescs.append(None)
        tstarts.append(None)
        tends.append(None)
        tdurs.append(None)
        tdists.append(None)
        tegains.append(None)
        tagains.append(None)
      else:
        nbvtrk += 1
        tconts.append(ctypes.create_unicode_buffer('%d %s%s, %d %s%s' %(track.NSegs, LSTRINGS['segment'], ('s' if track.NSegs >= 2 else ''), track.NPts, LSTRINGS['point'], ('s' if track.NPts >= 2 else ''))))
        tnames.append(ctypes.create_unicode_buffer(track.Name))
        tdescs.append(ctypes.create_unicode_buffer(track.Desc))
        tstarts.append(ctypes.create_unicode_buffer('' if track.Start is None else datetime.datetime.fromtimestamp(track.Start).strftime('%x %X')))
        tends.append(ctypes.create_unicode_buffer('' if track.End is None else datetime.datetime.fromtimestamp(track.End).strftime('%x %X')))
        tdurs.append(ctypes.create_unicode_buffer('' if track.Dur is None else '%d%s%02d%s%02.0f%s' % (track.Dur // 3600, LSTRINGS['h'], track.Dur % 3600 // 60, LSTRINGS['mn'], track.Dur % 60, LSTRINGS['s'])))
        tdists.append(ctypes.create_unicode_buffer('' if track.Dist is None else '%s%s' % (('%.2f ' % track.Dist_r).rstrip('0').rstrip('.'), LSTRINGS['km'])))
        tegains.append(ctypes.create_unicode_buffer('' if track.EGain is None else '%.0f%s' % (track.EGain_r, LSTRINGS['m'])))
        tagains.append(ctypes.create_unicode_buffer('' if track.AGain is None else '%.0f%s' % (track.AGain_r, LSTRINGS['m'])))
      if nbtrk == 1:
        nbtrk = track.NbGPXTrks
        if track.Wpts:
          twpts = ctypes.create_unicode_buffer('\r\n'.join(track.Wpts))
      trk += 1
    del trck.Track
    tr = '%s %%-%dd' % (LSTRINGS['Track'], len(str(max(0, nbtrk - 1))))
    ts = tuple(map(ctypes.create_unicode_buffer, ('GPX', 'MS Shell Dlg', ('%s:' % LSTRINGS['Path']), file, tr % 0, ('%s:' % LSTRINGS['Name']), ('%s:' % LSTRINGS['Description']), ('%s:' % LSTRINGS['Start']), ('%s:' % LSTRINGS['End']), ('%s:' % LSTRINGS['Duration']), ('%s:' % LSTRINGS['Distance']), ('%s:' % LSTRINGS['EleGain']), ('%s:' % LSTRINGS['AltGain']), ('%s:' % LSTRINGS['Waypoints']))))
    b = ctypes.create_string_buffer(cls._header_size(ts[0], ts[1]) + cls._text_item_size(ts[2]) + cls._text_item_size(ts[3]) + (nbtrk + 1) * cls._text_item_size() + nbtrk * cls._text_item_size(ts[4]) + nbvtrk * sum(cls._text_item_size(ts[i]) for i in range(5, 13)) + sum(cls._text_item_size(t) for ts in (tconts, tnames, tdescs, tstarts, tends, tdurs, tdists, tegains, tagains) for t in ts if t is not None) + (cls._text_item_size(ts[13]) + cls._text_item_size(twpts) if twpts is not None else 0))
    dt, o = cls._header(b, 'Child | Visible | Caption | VScroll | ModalFrame | SetFont', 0, 2 * nbtrk + 17 * nbvtrk + (5 if twpts else 3), 0, 0, 150, 250, ts[0], (9, ts[1]))
    dit, o = cls._text_item(b, o, 'Child | Visible | TabStop', 0, 5, 2, 30, 10, 0xffff, 0x0082, ts[2])
    dit, o = cls._text_item(b, o, 'Child | Visible | EditAutoHScroll | EditReadOnly', 0, 40, 2, 94, 10, 10, 0x0081, ts[3])
    y = 17
    for i in range(nbtrk):
      dit, o = cls._text_item(b, o, 'Child | Visible | StaticEtchedHorz', 0, 0, y, 150, 1, 0xffff, 0x0082)
      dit, o = cls._text_item(b, o, 'Child | Visible', 0, 5, (y := y + 3), 45, 10, 0xffff, 0x0082, ctypes.create_unicode_buffer(tr % i))
      if tconts[i] is not None:
        dit, o = cls._text_item(b, o, 'Child | Visible | EditRight | EditAutoHScroll | EditReadOnly', 0, 60, y, 74, 10, 10 * (i + 1) + 1, 0x0081, tconts[i])
        dit, o = cls._text_item(b, o, 'Child | Visible', 0, 10, (y := y + 10), 45, 10, 0xffff, 0x0082, ts[5])
        dit, o = cls._text_item(b, o, 'Child | Visible | EditAutoHScroll | TabStop%s' % (' | EditReadOnly' if readonly else ''), 0, 60, y, 74, 10, 10 * (i + 1) + 2, 0x0081, tnames[i])
        dit, o = cls._text_item(b, o, 'Child | Visible', 0, 10, (y := y + 10), 45, 10, 0xffff, 0x0082, ts[7])
        dit, o = cls._text_item(b, o, 'Child | Visible | TabStop | EditReadOnly', 0, 60, y, 10, 10, 10 * (i + 1) + 4, 0x0081, tstarts[i])
        dit, o = cls._text_item(b, o, 'Child | Visible', 0, 74, y, 45, 10, 0xffff, 0x0082, ts[8])
        dit, o = cls._text_item(b, o, 'Child | Visible | TabStop | EditReadOnly', 0, 124, y, 10, 10, 10 * (i + 1) + 5, 0x0081, tends[i])
        dit, o = cls._text_item(b, o, 'Child | Visible', 0, 10, (y := y + 10), 45, 10, 0xffff, 0x0082, ts[9])
        dit, o = cls._text_item(b, o, 'Child | Visible | TabStop | EditReadOnly', 0, 60, y, 10, 10, 10 * (i + 1) + 6, 0x0081, tdurs[i])
        dit, o = cls._text_item(b, o, 'Child | Visible', 0, 74, y, 45, 10, 0xffff, 0x0082, ts[10])
        dit, o = cls._text_item(b, o, 'Child | Visible | TabStop | EditReadOnly', 0, 124, y, 10, 10, 10 * (i + 1) + 7, 0x0081, tdists[i])
        dit, o = cls._text_item(b, o, 'Child | Visible', 0, 10, (y := y + 10), 45, 10, 0xffff, 0x0082, ts[11])
        dit, o = cls._text_item(b, o, 'Child | Visible | TabStop | EditReadOnly', 0, 60, y, 10, 10, 10 * (i + 1) + 8, 0x0081, tegains[i])
        dit, o = cls._text_item(b, o, 'Child | Visible', 0, 74, y, 45, 10, 0xffff, 0x0082, ts[12])
        dit, o = cls._text_item(b, o, 'Child | Visible | EditAutoHScroll | TabStop | EditReadOnly', 0, 124, y, 10, 10, 10 * (i + 1) + 9, 0x0081, tagains[i])
        dit, o = cls._text_item(b, o, 'Child | Visible', 0, 10, (y := y + 10), 45, 10, 0xffff, 0x0082, ts[6])
        dit, o = cls._text_item(b, o, 'Child | Visible | VScroll | EditAutoVScroll | EditWantReturn | EditMultiline | TabStop%s' % (' | EditReadOnly' if readonly else ''), 0, 60, y, 74, 32, 10 * (i + 1) + 3, 0x0081, tdescs[i])
        y += 22
      y += 12
    dit, o = cls._text_item(b, o, 'Child | Visible | StaticEtchedHorz', 0, 0, y, 150, 1, 0xffff, 0x0082)
    if twpts is not None:
      dit, o = cls._text_item(b, o, 'Child | Visible', 0, 5, (y := y + 3), 75, 10, 0xffff, 0x0082, ts[13])
      dit, o = cls._text_item(b, o, 'Child | Visible | VScroll | EditAutoVScroll | EditMultiline | EditReadOnly', 0, 10, (y := y + 10), 124, 32, 10 * (i + 3), 0x0081, twpts)
    return DLGPTEMPLATE(dt)
  @classmethod
  def _DlgProc(cls, hWnd, uMsg, wParam, lParam):
    r = 0
    if uMsg == 1024:
      d = DLGHWND(hWnd)
      if (rd0 := d.MapDialogRect((0, 0, 150, 250))) is not None and (r := _SPSUtil.GetTabDisplayRect(d)) is not None and d.Move((r.left, r.top, r.right - r.left, r.bottom - r.top), False) and (rd := d.Rect) is not None:
        wg = rd.right - rd.left + rd0.left - rd0.right
        c = None
        while (c := d.FindChildWindow(c, 'Static', '')):
          if (r := c.Rect) is not None:
            c.Move((0, r.top - rd.top, r.right - r.left + wg, r.bottom - r.top), False)
        for n in (('%s:' % LSTRINGS['End']), ('%s:' % LSTRINGS['Distance']), ('%s:' % LSTRINGS['AltGain'])):
          c = None
          while (c := d.FindChildWindow(c, 'Static', n)):
            if (r := c.Rect) is not None:
              c.Move((r.left - rd.left + wg // 2, r.top - rd.top, r.right - r.left, r.bottom - r.top), False)
        c = None
        while (c := d.FindChildWindow(c, 'Edit')):
          if (i := d.GetItemID(c)) and (r := c.Rect) is not None:
            i %= 10
            if i <= 3:
              c.Move((r.left - rd.left, r.top - rd.top, r.right - r.left + wg, r.bottom - r.top), False)
            elif i % 2:
              c.Move((r.left - rd.left + wg // 2, r.top - rd.top, r.right - r.left + wg // 2, r.bottom - r.top), False)
            else:
              c.Move((r.left - rd.left, r.top - rd.top, r.right - r.left + wg // 2, r.bottom - r.top), False)
        d.Update()
      r = 1
    elif uMsg == 78:
      if DLGNMHDR.from_address(lParam).code == 4294967094:
        d = DLGHWND(hWnd)
        trck = None
        track = None
        pstream = None
        pdeststream = None
        file = d.GetItemText(10)
        r = 0x80004005
        i = 1
        while (cn := d.GetItem(i * 10 + 2)) and (cd := d.GetItem(i * 10 + 3)):
          if d.GetItemModify(cn) or d.GetItemModify(cd):
            if (vn := d.GetItemText(cn)) is None or (vd := d.GetItemText(cd)) is None:
              break
            track = GPXTweaker.WGS84PropertiesTrack()
            if trck is None:
              if not file or not (pstream := PCOMSTREAM.CreateOnFile(file, 0x12)) or (content := pstream.GetContent()) is None or not (pdeststream := pstream.GetDestinationStream()):
                r = 0x80030005
                break
              trck = track
            if not track.LoadGPX(content, i - 1, trck, 'u') or not track.UpdateGPX(vn, vd):
              break
          i += 1
        else:
          if track is None:
            r = 0
          else:
            if (content := track.SaveGPX()) is not None and pdeststream.Write(content) is not None and not ((r := pdeststream.Commit()) & 0x80000000):
              r = pstream.Commit()
        if track is not None:
          del track.Track
        if pdeststream:
          pdeststream.Release()
        if pstream:
          pstream.Release()
        if r & 0x80000000:
          if hasattr(DialogWindow, 'TaskDialogIndirect'):
            b = wintypes.INT()
            DialogWindow.TaskDialogIndirect((d.Parent, Window.ModuleHandle, 'PositionRelativeToWindow', 'Yes | No', LSTRINGS['Errtitle'], 0,'', '%s.\r\n\r\n%s: %s\r\n\r\n%s %s\r\n\r\n%s ?' % (LSTRINGS['Errmsg'], LSTRINGS['Path'], file, LSTRINGS['Error'], str(WError(r))[1:-1], LSTRINGS['Retry']), 0, None, 'Retry', 0, None, 0), b, None, None)
            b = b.value
          else:
            b = DialogWindow.MessageBox(d, '%s.\r\n\r\n%s: %s\r\n\r\n%s %s\r\n\r\n%s ?' % (LSTRINGS['Errmsg'], LSTRINGS['Path'], file, LSTRINGS['Error'], str(WError(r))[1:-1], LSTRINGS['Retry']), LSTRINGS['Errtitle'], 0x10004)
          if b == 7:
            d.ReturnValue = 0
          else:
            d.ReturnValue = 1
        else:
          d.ReturnValue = 0
        r = 1
    return super()._DlgProc(hWnd, uMsg, wParam, lParam) or r
  @classmethod
  def _CallbackProc(cls, hwnd, uMsg, ppsp):
    if (r := super()._CallbackProc(hwnd, uMsg, ppsp)) and uMsg == 2:
      if not ppsp:
        return 0
      psp = ppsp.contents
      with cls[psp.lParam] as self:
        if not self:
          return 0
        if (nelts := self.nelts) <= 1:
          e = 0
        else:
          try:
            e = int(psp.pszTitle.rsplit(' ', 1)[1]) - 1
          except:
            return 0
        trk = nelts - 1 - e
        if e < 0 or e >= nelts or (file := self.pdtobj.GetFileName(trk)) is None or (s := self.pdtobj.GetFileContent(trk)) is None:
          return None
        content = s.GetContent()
        s.Release()
        if content is None:
          return 0
        self.ppsp[e].pResource = psp.pResource = cls.GPXTemplate(file, content, bool((d := self.pdtobj.GetFileDescriptor(trk)) is not None and d['dwFileAttributes'] & 1))
        return 1
    return r

class _COM_IGPXShellPropSheetExt_impl(metaclass=_COMMeta, interfaces=(_COM_IShellExtInit, _COM_IGPXShellPropSheetExt)):
  CLSID = True
  Exts = ('.gpx',)
  _destroy = _COM_IShellPropSheetExt_impl._destroy
_COM_IGPXShellPropSheetExt._impl = _COM_IGPXShellPropSheetExt_impl

class _COM_IGPXInitializeWithStream(_COM_IInitializeWithStream):
  pass

class _COM_IGPXPropertyStoreDelegating(_COM_IPropertyStoreDelegating):
  FMTID_GPXTWEAKER_GPX = GUID.from_name('GPXTweaker.GPX')
  PKEY_GPXTWEAKER_GPX_PROPGROUP = (FMTID_GPXTWEAKER_GPX, 100)
  PKEY_GPXTWEAKER_GPX_NAME = (FMTID_GPXTWEAKER_GPX, 101)
  PKEY_GPXTWEAKER_GPX_DESC = (FMTID_GPXTWEAKER_GPX, 102)
  PKEY_GPXTWEAKER_GPX_WPTS = (FMTID_GPXTWEAKER_GPX, 103)
  PKEY_GPXTWEAKER_GPX_START = (FMTID_GPXTWEAKER_GPX, 104)
  PKEY_GPXTWEAKER_GPX_END = (FMTID_GPXTWEAKER_GPX, 105)
  PKEY_GPXTWEAKER_GPX_DUR = (FMTID_GPXTWEAKER_GPX, 106)
  PKEY_GPXTWEAKER_GPX_DIST = (FMTID_GPXTWEAKER_GPX, 107)
  PKEY_GPXTWEAKER_GPX_EGAIN = (FMTID_GPXTWEAKER_GPX, 108)
  PKEY_GPXTWEAKER_GPX_AGAIN = (FMTID_GPXTWEAKER_GPX, 109)
  @classmethod
  def LazyLoad(cls, self, pKey=None):
    if pKey is not None and pKey.contents.fmtid != cls.FMTID_GPXTWEAKER_GPX:
      return 1
    pcache = self.pcache
    pstream = self.pstream
    pstream.Seek(0, 0)
    if (content := pstream.GetContent()) is None:
      return 0x80030005
    track = None
    m = 's' if pKey is not None and pKey.contents.pid % 100 <= 3 else 'f'
    if not pcache.GetValue(_COM_IGPXPropertyStoreDelegating.PKEY_GPXTWEAKER_GPX_PROPGROUP):
      track = GPXTweaker.WGS84PropertiesTrack()
      if not track.LoadGPX(content, 0, None, m):
        return 0x80004005
      pcache.SetValueAndState(cls.PKEY_GPXTWEAKER_GPX_PROPGROUP, ('VT_LPWSTR', '\u200d'), 0)
      pcache.SetValueAndState(cls.PKEY_GPXTWEAKER_GPX_NAME, ('VT_LPWSTR', track.Name), 0)
      pcache.SetValueAndState(cls.PKEY_GPXTWEAKER_GPX_DESC, ('VT_LPWSTR', track.Desc), 0)
      pcache.SetValueAndState(cls.PKEY_GPXTWEAKER_GPX_WPTS, ('VT_VECTOR | VT_LPWSTR', track.Wpts), 0)
    if m == 'f':
      if track is None:
        track = GPXTweaker.WGS84PropertiesTrack()
        if not track.LoadGPX(content, 0, None, m):
          return 0x80004005
      pcache.SetValueAndState(cls.PKEY_GPXTWEAKER_GPX_START, (('VT_EMPTY', None) if track.Start is None else ('VT_FILETIME', datetime.datetime.fromtimestamp(track.Start, datetime.UTC))), 0)
      pcache.SetValueAndState(cls.PKEY_GPXTWEAKER_GPX_END, (('VT_EMPTY', None) if track.End is None else ('VT_FILETIME', datetime.datetime.fromtimestamp(track.End, datetime.UTC))), 0)
      pcache.SetValueAndState(cls.PKEY_GPXTWEAKER_GPX_DUR, (('VT_EMPTY', None) if track.Dur is None else ('VT_UI8', round(track.Dur) * 10000000)), 0)
      pcache.SetValueAndState(cls.PKEY_GPXTWEAKER_GPX_DIST, (('VT_EMPTY', None) if track.Dist is None else ('VT_R8', track.Dist_r)), 0)
      pcache.SetValueAndState(cls.PKEY_GPXTWEAKER_GPX_EGAIN, (('VT_EMPTY', None) if track.EGain is None else ('VT_UI4', track.EGain_r)), 0)
      pcache.SetValueAndState(cls.PKEY_GPXTWEAKER_GPX_AGAIN, (('VT_EMPTY', None) if track.AGain is None else ('VT_UI4', track.AGain_r)), 0)
    if track is not None:
      del track.Track
    return 0 if m == 'f' else 1
  @classmethod
  def Save(cls, self):
    if self.ManualSafeSave:
      pdeststream = yield True
    pcache = self.pcache
    if (v_s_n := pcache.GetValueAndState(cls.PKEY_GPXTWEAKER_GPX_NAME)) is None or ((v_s_d := pcache.GetValueAndState(cls.PKEY_GPXTWEAKER_GPX_DESC))) is None:
      return IGetLastError() or 0x80004005
    if (v_s_n[1] != 2 and v_s_d[1] != 2):
      return 1
    pstream = self.pstream
    if pstream.Seek(0, 0) is None or (content := pstream.GetContent()) is None:
      return 0x80030005
    track = GPXTweaker.WGS84PropertiesTrack()
    if not track.LoadGPX(content, 0, None, 'u'):
      return 0x80004005
    if track.UpdateGPX(v_s_n[0], v_s_d[0]) and (content := track.SaveGPX()) is not None:
      if self.ManualSafeSave and pdeststream:
        r = 0x80030005 if pdeststream.Write(content) is None else 0
      else:
        r = 0x80030005 if pstream.SetSize(0) is None or pdeststream.Write(content) is None else 0
      r = IGetLastError() or r
    else:
      r = 0x80004005
    del track.Track
    return r

class _COM_IGPXPropertyStoreCapabilities(_COM_IPropertyStoreCapabilities):
  ReadOnly = {_COM_IGPXPropertyStoreDelegating.PKEY_Search_Contents, _COM_IGPXPropertyStoreDelegating.PKEY_GPXTWEAKER_GPX_PROPGROUP, _COM_IGPXPropertyStoreDelegating.PKEY_GPXTWEAKER_GPX_WPTS, _COM_IGPXPropertyStoreDelegating.PKEY_GPXTWEAKER_GPX_START, _COM_IGPXPropertyStoreDelegating.PKEY_GPXTWEAKER_GPX_END, _COM_IGPXPropertyStoreDelegating.PKEY_GPXTWEAKER_GPX_DUR, _COM_IGPXPropertyStoreDelegating.PKEY_GPXTWEAKER_GPX_DIST, _COM_IGPXPropertyStoreDelegating.PKEY_GPXTWEAKER_GPX_EGAIN, _COM_IGPXPropertyStoreDelegating.PKEY_GPXTWEAKER_GPX_AGAIN}
  @classmethod
  def _IsPropertyWritable(cls, pI, pKey):
    with cls[pI] as self:
      if not self or not pKey:
        return 0x80004003
      return 0 if pKey.contents.to_key() not in cls.ReadOnly and self.pcache.GetValue(_COM_IGPXPropertyStoreDelegating.PKEY_GPXTWEAKER_GPX_PROPGROUP) else 1

class _COM_IGPXPropertyHandler_impl(metaclass=_COMMeta, interfaces=(_COM_IGPXInitializeWithStream, _COM_IGPXPropertyStoreDelegating, _COM_IGPXPropertyStoreCapabilities)):
  CLSID = True
  Exts = ('.gpx',)
  ManualSafeSave = True
  _destroy = _COM_IPropertyHandler_impl._destroy
_COM_IGPXInitializeWithStream._impl = _COM_IGPXPropertyStoreDelegating._impl = _COM_IGPXPropertyStoreCapabilities._impl = _COM_IGPXPropertyHandler_impl

def DllInstall(bInstall, pszCmdLine):
  if (l := len((cmdline := pszCmdLine if isinstance(pszCmdLine, str) else ctypes.wstring_at(pszCmdLine)).split('|'))) >= 3:
    return ISetLastError(0x80070057)
  user = cmdline[1].lower() not in {'f', 'false'} if l == 2 else True
  r = os.path.dirname(os.path.abspath(cmdline[0]))
  p = os.path.join(r, 'GPXTweaker.propdesc')
  Initialize()
  if bInstall:
    r = os.system('icacls "%s" /grant *S-1-5-32-545:(OI)(CI)M /inheritance:d > nul' % r) == 0
    with open(p, 'wt', encoding='utf-8') as f:
      f.write('''\
<?xml version="1.0" encoding="utf-8"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://schemas.microsoft.com/windows/2006/propertydescription" schemaVersion="1.0">
  <propertyDescriptionList publisher="PCigales" product="GPXTweaker">
    <propertyDescription name="GPXTweaker.GPX.PropGroup" formatID="{11a23e44-faa0-b561-9aa6-cdb49267a313}" propID="100">
      <description>Separator for track 0</description>
      <searchInfo inInvertedIndex="false" isColumn="false"/>
      <typeInfo type="Null" isGroup="true" isInnate="true" isViewable="true"/>
      <labelInfo label="%s"/>
    </propertyDescription>
    <propertyDescription name="GPXTweaker.GPX.Name" formatID="{11a23e44-faa0-b561-9aa6-cdb49267a313}" propID="101">
      <description>Name of the track 0</description>
      <searchInfo inInvertedIndex="true" isColumn="true" columnIndexType="OnDisk" mnemonics="%s"/>
      <typeInfo type="String" isInnate="false" multipleValues="false" isViewable="true" conditionType="String"/>
      <labelInfo label="%s"/>
      <displayInfo displayType="String">
        <stringFormat formatAs="General"/>
      </displayInfo>
    </propertyDescription>
    <propertyDescription name="GPXTweaker.GPX.Desc" formatID="{11a23e44-faa0-b561-9aa6-cdb49267a313}" propID="102">
      <description>Description of the track 0</description>
      <searchInfo inInvertedIndex="true" isColumn="true" columnIndexType="OnDisk" mnemonics="%s"/>
      <typeInfo type="String" isInnate="false" multipleValues="false" isViewable="true" conditionType="String"/>
      <labelInfo label="%s"/>
      <displayInfo displayType="String">
        <stringFormat formatAs="General"/>
        <drawControl control="MultiLineText"/>
        <editControl control="MultiLineText"/>
      </displayInfo>
    </propertyDescription>
    <propertyDescription name="GPXTweaker.GPX.Wpts" formatID="{11a23e44-faa0-b561-9aa6-cdb49267a313}" propID="103">
      <description>Waypoints of the track 0</description>
      <searchInfo inInvertedIndex="true" isColumn="true" columnIndexType="OnDiskVector" mnemonics="%s"/>
      <typeInfo type="String" isInnate="true" multipleValues="true" isViewable="true" conditionType="String"/>
      <labelInfo label="%s"/>
      <displayInfo displayType="String">
        <stringFormat formatAs="General"/>
        <drawControl control="MultiValueText"/>
      </displayInfo>
    </propertyDescription>
    <propertyDescription name="GPXTweaker.GPX.Start" formatID="{11a23e44-faa0-b561-9aa6-cdb49267a313}" propID="104">
      <description>Start date of the track 0</description>
      <searchInfo inInvertedIndex="false" isColumn="true" columnIndexType="OnDisk" mnemonics="%s"/>
      <typeInfo type="DateTime" isInnate="true" multipleValues="false" isViewable="true" conditionType="DateTime" aggregationType="DateRange"/>
      <labelInfo label="%s"/>
      <displayInfo displayType="DateTime">
        <dateTimeFormat formatAs="General" formatTimeAs="LongTime" formatDateAs="ShortDate"/>
        <drawControl control="StaticText"/>
      </displayInfo>
    </propertyDescription>
    <propertyDescription name="GPXTweaker.GPX.End" formatID="{11a23e44-faa0-b561-9aa6-cdb49267a313}" propID="105">
      <description>End date of the track 0</description>
      <searchInfo inInvertedIndex="false" isColumn="true" columnIndexType="OnDisk" mnemonics="%s"/>
      <typeInfo type="DateTime" isInnate="true" multipleValues="false" isViewable="true" conditionType="DateTime" aggregationType="DateRange"/>
      <labelInfo label="%s"/>
      <displayInfo displayType="DateTime">
        <dateTimeFormat formatAs="General" formatTimeAs="LongTime" formatDateAs="ShortDate"/>
        <drawControl control="StaticText"/>
      </displayInfo>
    </propertyDescription>
    <propertyDescription name="GPXTweaker.GPX.Dur" formatID="{11a23e44-faa0-b561-9aa6-cdb49267a313}" propID="106">
      <description>Duration of the track 0</description>
      <searchInfo inInvertedIndex="false" isColumn="true" columnIndexType="OnDisk" mnemonics="%s"/>
      <typeInfo type="UInt64" isInnate="true" multipleValues="false" isViewable="true" conditionType="Number" aggregationType="Sum"/>
      <labelInfo label="%s"/>
      <displayInfo displayType="Number" alignment="Center">
        <numberFormat formatAs="Duration" formatDurationAs="hh:mm:ss"/>
        <drawControl control="StaticText"/>
      </displayInfo>
    </propertyDescription>
    <propertyDescription name="GPXTweaker.GPX.Dist" formatID="{11a23e44-faa0-b561-9aa6-cdb49267a313}" propID="107">
      <description>Distance of the track 0</description>
      <searchInfo inInvertedIndex="false" isColumn="true" columnIndexType="OnDisk" mnemonics="%s"/>
      <typeInfo type="Double" isInnate="true" multipleValues="false" isViewable="true" conditionType="Number" aggregationType="Sum"/>
      <labelInfo label="%s"/>
      <displayInfo displayType="Number" alignment="Center">
        <numberFormat formatAs="General"/>
        <drawControl control="StaticText"/>
      </displayInfo>
    </propertyDescription>
    <propertyDescription name="GPXTweaker.GPX.EGain" formatID="{11a23e44-faa0-b561-9aa6-cdb49267a313}" propID="108">
      <description>Elevation gain of the track 0</description>
      <searchInfo inInvertedIndex="false" isColumn="true" columnIndexType="OnDisk" mnemonics="%s"/>
      <typeInfo type="UInt32" isInnate="true" multipleValues="false" isViewable="true" conditionType="Number" aggregationType="Sum"/>
      <labelInfo label="%s"/>
      <displayInfo displayType="Number" alignment="Center">
        <numberFormat formatAs="General"/>
        <drawControl control="StaticText"/>
      </displayInfo>
    </propertyDescription>
    <propertyDescription name="GPXTweaker.GPX.AGain" formatID="{11a23e44-faa0-b561-9aa6-cdb49267a313}" propID="109">
      <description>Altitude gain of the track 0</description>
      <searchInfo inInvertedIndex="false" isColumn="true" columnIndexType="OnDisk" mnemonics="%s"/>
      <typeInfo type="UInt32" isInnate="true" multipleValues="false" isViewable="true" conditionType="Number" aggregationType="Sum"/>
      <labelInfo label="%s"/>
      <displayInfo displayType="Number" alignment="Center">
        <numberFormat formatAs="General"/>
        <drawControl control="StaticText"/>
      </displayInfo>
    </propertyDescription>
  </propertyDescriptionList>
</schema>''' % (LSTRINGS['Track'], LSTRINGS['trackname'], LSTRINGS['Trackname'], LSTRINGS['trackdescription'], LSTRINGS['Trackdescription'], LSTRINGS['trackwpts'], LSTRINGS['Trackwpts'], LSTRINGS['trackstart'], LSTRINGS['Trackstart'], LSTRINGS['trackend'], LSTRINGS['Trackend'], LSTRINGS['trackduration'], LSTRINGS['Trackduration'], LSTRINGS['trackdistance'], LSTRINGS['Trackdistance'], LSTRINGS['trackelegain'], LSTRINGS['Trackelegain'], LSTRINGS['trackaltgain'], LSTRINGS['Trackaltgain']))
    r = r and \
      COMRegistration.RegistryAddPropertySchema(p) and \
      COMRegistration.RegistryAddCOMFactory(_COM_IGPXShellPropSheetExt_impl) and \
      COMRegistration.RegistryAddShellPropSheetHandler(_COM_IGPXShellPropSheetExt_impl, 'GPXTweaker') and \
      COMRegistration.RegistryAddCOMFactory(_COM_IGPXPropertyHandler_impl, user=False) and \
      COMRegistration.RegistryAddPropertyHandler(_COM_IGPXPropertyHandler_impl, full_details='+GPXTweaker.GPX.PropGroup;GPXTweaker.GPX.Name;GPXTweaker.GPX.Start;GPXTweaker.GPX.End;GPXTweaker.GPX.Dur;GPXTweaker.GPX.Dist;GPXTweaker.GPX.EGain;GPXTweaker.GPX.AGain;GPXTweaker.GPX.Desc;GPXTweaker.GPX.Wpts', preview_details='+GPXTweaker.GPX.Name;*GPXTweaker.GPX.Start;*GPXTweaker.GPX.End;*GPXTweaker.GPX.Dur;*GPXTweaker.GPX.Dist;*GPXTweaker.GPX.EGain;*GPXTweaker.GPX.AGain;GPXTweaker.GPX.Desc;*GPXTweaker.GPX.Wpts', content_layout='alpha', content_mode_browse='~GPXTweaker.GPX.Name;GPXTweaker.GPX.Dur;~System.ItemNameDisplay;~GPXTweaker.GPX.Desc;GPXTweaker.GPX.Dist;GPXTweaker.GPX.EGain;GPXTweaker.GPX.AGain', content_mode_search='~GPXTweaker.GPX.Name;GPXTweaker.GPX.Dur;~System.ItemPathDisplay;~GPXTweaker.GPX.Desc;GPXTweaker.GPX.Dist;GPXTweaker.GPX.EGain;GPXTweaker.GPX.AGain')
  else:
    r = \
      COMRegistration.RegistryRemovePropertySchema(p) and \
      COMRegistration.RegistryRemovePropertyHandler(_COM_IGPXPropertyHandler_impl) and \
      COMRegistration.RegistryRemoveCOMFactory(_COM_IGPXPropertyHandler_impl, user=False) and \
      COMRegistration.RegistryRemoveShellPropSheetHandler(_COM_IGPXShellPropSheetExt_impl, 'GPXTweaker') and \
      COMRegistration.RegistryRemoveCOMFactory(_COM_IGPXShellPropSheetExt_impl)
  Uninitialize()
  return ISetLastError(0 if r else IGetLastError() or 0x8000ffff)

if __name__ == '__main__' and len(sys.argv) >= 2:
  if COMRegistration.IsAdmin() is False:
    if (r := COMRegistration.RunAsAdmin()) is None:
      r = 0x8000ffff
    print(WError(r))
    sys.exit(r)
  if (a := sys.argv[1].lstrip('-/').lower()) == 'register':
    r = DllInstall(True, '|'.join((os.path.dirname(os.path.abspath(__file__)), *sys.argv[2:])))
  elif a == 'unregister':
    r = DllInstall(False, '|'.join((os.path.dirname(os.path.abspath(__file__)), *sys.argv[2:])))
  else:
    r = 0x80070057
  print(WError(r))
  sys.exit(r)