from GPXTweaker import *
import random
import time
random.seed()

p = os.path.expandvars(r'%TEMP%\test')

m = WebMercatorMap()

matrix = 16
lat = 43.20403
lon = 5.49404

infos = WebMercatorMap.TSAlias('OSM')
m.GetTileInfos(infos, matrix, None, None)
print(infos)
m.GetTileInfos(infos, matrix, lat, lon)
print(infos)
# exit()

key = "cartes"
infos = WebMercatorMap.TSAlias('IGN_PLANV2')
pconnection = [None]
m.GetTileInfos(infos, matrix, None, None, key, pconnection=pconnection)
print(infos)
infos = WebMercatorMap.TSAlias('IGN_PLANV2')
m.GetTileInfos(infos, matrix, lat, lon, key, pconnection=pconnection)
print(infos)
pconnection[0].close()
# exit()

infos = WebMercatorMap.TSAlias('OSM')
pconnection = [None]
tile = m.GetTile(infos, matrix, lat, lon, pconnection=pconnection)
print(len(tile))
pconnection[0].close()
# exit()

infos = WebMercatorMap.TSAlias('OSM')
pconnection = [None]
tile = m.GetTile(infos, matrix, lat, lon, pconnection=pconnection)
print(infos)
print(len(tile))
print(m.SaveTile(p, infos , tile))
print(m.SaveTile(p, infos , tile, just_refresh=True))
infos = WebMercatorMap.TSAlias('OSM')
m.ReadTileInfos(p, infos, matrix, None, None)
print(infos)
m.ReadTileInfos(p, infos, matrix, lat, lon)
print(infos)
print(time.ctime(m.ReadKnownTile(p, infos, just_lookup=True)))
tile = m.ReadTile(p, infos, matrix, lat, lon)
print(infos)
print(len(tile))
# exit()

infos = WebMercatorMap.TSAlias('OSM')
g = m.TileGenerator(infos, matrix, local_pattern=p, local_store=True)
print(infos)
print(g(lat, lon, just_box=True))
Tile = g(lat, lon)
print(infos)
print(Tile['infos'], len(Tile['tile']))
Tile = g(lat+0.02, lon+0.02)
print(infos)
print(Tile['infos'], len(Tile['tile']))
g(close_connection=True)
print(g(lat, lat + 0.02, lon, lon + 0.01, True))
area = g(lat, lat + 0.02, lon, lon + 0.01)
print(area)
area=list(area)
print(list((Tile['infos']['row'], Tile['infos']['col'], len(Tile['tile'])) for Tile in area))
# exit()

infos = WebMercatorMap.TSAlias('OSM')
tiles=[]
pr=m.RetrieveTiles(infos, matrix, lat, lat+0.01, lon, lon+0.01, memory_store=tiles, threads=3)
print(infos)
pr['finish_event'].wait()
print(list(((len(t)) for c in tiles for t in c)))
print(pr)
# exit()

t = time.time()
infos = WebMercatorMap.TSAlias('OSM')
progress = m.DownloadTiles(p, infos, matrix, lat - 0.01, lat +0.02, lon - 0.01, lon + 0.01, threads=50)
print('%6i s écoulées - fin de l\'initialisation -> ' % int(time.time() - t), progress)
while not progress['finish_event'].is_set():
  progress['process_event'].clear()
  print('%6i s écoulées :   nombre total de tuiles: %6i -   progression: %s -   téléchargées: %6i -   sautées: %6i -   manquées: %6i' % (int(time.time() - t), progress['total'], progress['percent'], progress['downloaded'], progress['skipped'], progress['failed']))
  progress['process_event'].wait()
print('%6i s écoulées :   nombre total de tuiles: %6i -   progression: %s -   téléchargées: %6i -   sautées: %6i -   manquées: %6i' % (int(time.time() - t), progress['total'], progress['percent'], progress['downloaded'], progress['skipped'], progress['failed']))
# exit()

tiles=[]
import time
t = time.time()
infos = WebMercatorMap.TSAlias('OSM')
progress = m.RetrieveTiles(infos, matrix, lat - 0.01, lat +0.01, lon - 0.01, lon + 0.01, memory_store=tiles)
print('%6i s écoulées - fin de l\'initialisation -> ' % int(time.time() - t), progress)
while not progress['finish_event'].is_set():
  progress['process_event'].clear()
  print('%6i s écoulées :   nombre total de tuiles: %6i -   progression: %s -   téléchargées: %6i -   sautées: %6i -   manquées: %6i' % (int(time.time() - t), progress['total'], progress['percent'], progress['downloaded'], progress['skipped'], progress['failed']))
  progress['process_event'].wait()
print('%6i s écoulées :   nombre total de tuiles: %6i -   progression: %s -   téléchargées: %6i -   sautées: %6i -   manquées: %6i' % (int(time.time() - t), progress['total'], progress['percent'], progress['downloaded'], progress['skipped'], progress['failed']))
row1, col1 = progress['box'][0]
row2, col2 = progress['box'][1]
print(list((r, c, len(tiles[c][r])) for c in range(col2 + 1 - col1) for r in range(row2 - row1 + 1)))
# exit()

m.ReadTileInfos(p, infos, matrix)
tiles = [[m.ReadKnownTile(p, {**infos, **{'row': row, 'col': col}}) for row in range(24024, 24027)] for col in range(33760, 33771)]
print(tiles)
# exit()

tiles=[]
key = "ortho"
referer = ""
infos = WebMercatorMap.TSAlias('IGN_PHOTOS')
pr=m.RetrieveTiles(infos, matrix, lat, lat+0.16, lon, lon+0.22, key=key, referer=referer, memory_store=tiles, local_pattern=p, local_store=True, threads=4)
print(infos)
pr['finish_event'].wait()
t=time.time()
map = m.MergeTiles(infos, tiles)
print(len(tiles) * len(tiles[0]), time.time() - t)
print(len(map))
f = open(p + r'\map.jpg', 'wb')
f.write(map)
f.close()
print(time.time()-t)
# exit()

key = "ortho"
referer = ""
infos = WebMercatorMap.TSAlias('IGN_PHOTOS')
m.AssembleMap(infos, 16, lat - 0.01, lat +0.01, lon - 0.01, lon + 0.01, key=key, referer=referer, threads=4)
print(m.MapInfos, m.MapResolution, len(m.Map))
print(m.SaveMap(p + r'\map.jpg'))
print(m.LoadMap(p + r'\map.jpg'))
print(m.MapInfos, m.MapResolution)
# exit()

key='ortho'
referer=''
infos = WebMercatorMap.MSAlias('IGN_PHOTOS')
m.FetchMap(infos, 43.20403, 43.21191, 5.49404, 5.5217, 200, 400, dpi=90, key=key, referer=referer)
print(m.MapInfos, m.MapResolution)
print(m.SaveMap(p + r'\map.png'))
print(m.LoadMap(p + r'\map.png'))
print(m.MapInfos, m.MapResolution)
# exit()

key='altimetrie'
referer=''
e=WGS84Elevation()
infos = WGS84Elevation.MSAlias('IGN_RGEALTI')
e.FetchMap(infos, 43.20403, 43.21191, 5.49404, 5.5217, 1024, 1536, key=key, referer=referer)
print(e.MapInfos, e.MapResolution, len(e.Map))
print(e.SaveMap(p + r'\map_f.bil'))
print(e.LoadMap(p + r'\map_f.bil'))
print(e.MapInfos, e.MapResolution, len(e.Map))
point = (43.21191, 5.49404)
print(e.WGS84toElevation((point,)))
# exit

key='choisirgeoportail'
referer=''
e=WGS84Elevation()
infos = WGS84Elevation.ASAlias('IGN_ALTI')
point = (43.21191, 5.49404)
print(e.RequestElevation(infos, point, key=key))
points = ((48.0551, 0.2367), (46.6077, 2.1570))
print(e.RequestElevation(infos, points, key=key))
print(infos)
# exit()

key='altimetrie'
referer=''
e=WGS84Elevation()
infos = WGS84Elevation.TSAlias('IGN_RGEALTI')
e.AssembleMap(infos, 14, 43.20403, 43.21191, 5.49404, 5.5217, key=key, referer=referer, local_pattern=p)
print(e.MapInfos, e.MapResolution, len(e.Map))
print(e.SaveMap(p + r'\map_a.bil'))
points = list((lat + random.randrange(1000)/200000, lon + random.randrange(1000)/40000) for i in range(5))
print(points)
e3 = e.WGS84toElevation(points)
print('tilesmap', e3)
infos = WGS84Elevation.MSAlias('IGN_RGEALTI')
e.LoadMap(p + r'\map_f.bil')
e4 = e.WGS84toElevation(points)
print('map', e4)
infos = WGS84Elevation.ASAlias('IGN_ALTI')
key='choisirgeoportail'
e1 = e.RequestElevation(infos, points, key=key, referer=referer)
print('as', e1)
infos = WGS84Elevation.TSAlias('IGN_RGEALTI')
key='altimetrie'
e2=e.WGS84toElevation(points, infos, 14, key=key, referer=referer)
print('tiles', e2)
print(list(int(1000*(e1[i]-e2[i])/math.sqrt(e1[i]**2+e2[i]**2)) for i in range(5)))
print(list(int(1000*(e1[i]-e3[i])/math.sqrt(e1[i]**2+e3[i]**2)) for i in range(5)))
print(list(int(1000*(e1[i]-e4[i])/math.sqrt(e1[i]**2+e4[i]**2)) for i in range(5)))
# exit()

m = WebMercatorMap(30, 5)
infos = WebMercatorMap.TSAlias('OSM')
id = (0, matrix)
print(m.SetTilesProvider(id, infos, matrix, local_pattern=p, local_store=True))
ti=time.time()
def t(r,c):
  time.sleep(0.5)
  print(r, c, len(m.Tiles[id, (r, c)](8)), time.time() - ti)
thr=[None] * 10
for th in thr:
  row, col = 24026 + random.randrange(3), 33768 + random.randrange(3)
  print(row, col)
  th=threading.Thread(target=t, args=(row, col))
  th.start()
while threading.active_count() > 1:
  print(list(e[1] for e in m.Tiles.Buffer.keys()))
  time.sleep(0.2)
  print(len(m.Tiles.Buffer))
# exit()

GPXTweakerInterface = GPXTweakerWebInterfaceServer(p + r"\t.gpx")
#GPXTweakerInterface = GPXTweakerWebInterfaceServer(p + r"\t.gpx", 'IGN PLANV2', True, maxheight=3000, maxwidth=6000)
GPXTweakerInterface.run()
webbrowser.open('http://127.0.0.1:%s/GPXTweaker.html' % GPXTweakerInterface.Ports[0])
while True:
  k = msvcrt.getch()
  if k == b'\xe0':
    k = msvcrt.getch()
    k = b''
  if k.upper() == b'S':
      break
GPXTweakerInterface.shutdown()
# exit()
