import shapefile
from MapLoader import MapDownloader
from coord2rowcol import Coord2RowCol
import asynMapLoader


sf = shapefile.Reader('shpfile/gg05.shp')

records = sf.records()
print(len(records))

for record in records:
    minx = record[1]
    maxx = record[2]
    miny = record[3]
    maxy = record[4]
    # if record[0] < 29:
    #     continue
    # if record[0] == 44 or record[0] == 55:
    #     # md = MapDownloader(level=17, maptype=2, grid=record[0])
    #     # md.QueryMap(minx, miny, maxx, maxy)
    #     ml = Coord2RowCol(level=14, maptype=1, grid=record[0])
    #     listUrl = ml.coordtoQuant(minx, miny, maxx, maxy)
    #     try:
    #         asynMapLoader.main(listUrl)
    #         ml.mergemap()
    #     except Exception as e:
    #         with open('download_log.txt', 'a') as logfile:
    #             logfile.write(str(record[0]) + "|" + str(e) + "\n")
    #         print(e)
    ml = Coord2RowCol(level=10, maptype=1, grid=record[0])
    listUrl = ml.coordtoQuant(minx, miny, maxx, maxy)
    try:
        asynMapLoader.main(listUrl, ""+str(record[0]))
        ml.mergemap()
    except Exception as e:
        with open('download_log.txt', 'a') as logfile:
            logfile.write(str(record[0]) + "|" + str(e)+"\n")
        print(e)


