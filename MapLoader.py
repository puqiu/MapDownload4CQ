from urllib import request
from PIL import Image
import math
import os


class MapDownloader(object):
    def __init__(self, level=16, maptype=1, grid="all"):
        self._tilesize = 256
        self._originX = -180
        self._originY = 90
        self._mapUrl = r"http://www.digitalcq.com/RemoteRest/services/CQMap_VEC/MapServer/tile/"
        self._satilateUrl = r"http://www.digitalcq.com/RemoteRest/services/CQMap_IMG/MapServer/tile/"
        self._grid = grid

        self._mapleveldic = {
                             8: (1154287.4728857423, 0.002746582031250001),
                             9: (577143.7364428712, 0.0013732910156250004),
                             10:  (288571.8682214356, 6.866455078125002E-4),
                             11: (144285.9341107178, 3.433227539062501E-4),
                             12: (72142.9670553589, 1.7166137695312505E-4),
                             13: (36071.48352767945, 8.583068847656253E-5),
                             14: (18035.741763839724, 4.2915344238281264E-5),
                             15: (9017.870881919862, 2.1457672119140632E-5),
                             16: (4508.935440959931, 1.0728836059570316E-5),
                             17: (2254.4677204799655, 5.364418029785158E-6)
                            }
        if maptype==2:
            self._mapUrl = self._satilateUrl

        self._level = level
        self._strTmpDir = os.getcwd() + "/" + str(self._level) + "/"
        try:
            self._resolution = self._mapleveldic[self._level][1]
        except:
            print("地图级别设置错误：支持16-18级")


    def QueryMap(self, topleftLongitude, topleftLatutide, bottomrightLongitude, bottomrightLatitude):
        topLeftCol, toplefRow = self.LongitudeLatitude2ColRow(topleftLongitude, topleftLatutide)
        boRightCol, boRightRow = self.LongitudeLatitude2ColRow(bottomrightLongitude, bottomrightLatitude)

        minCol = topLeftCol if topLeftCol<boRightCol else boRightCol
        minRow = toplefRow if toplefRow<boRightRow else boRightRow
        maxCol = topLeftCol if topLeftCol>=boRightCol else boRightCol
        maxRow = toplefRow if toplefRow>=boRightRow else boRightRow

        imageList = []
        for i in range(minRow, maxRow+1):
            imagerow = []
            for j in range(minCol, maxCol+1):
                strSavePath = "".join([self._strTmpDir+ str(i), "_", str(j) + ".png"])
                self.doDownload(i, j, strSavePath)
                imagerow.append(strSavePath)
            imageList.append(imagerow)

        self.MergeMap(imageList, minRow, minCol)

    def LongitudeLatitude2ColRow(self, longitude, latitude):
        col = int(math.floor((longitude-self._originX)/(self._resolution*self._tilesize)))
        row = int(math.floor((self._originY-latitude)/(self._resolution*self._tilesize)))
        return col, row

    def MergeMap(self, imagelist, topleftY, topleftX):

        imagewidth = len(imagelist[0]) * self._tilesize
        imageheight = len(imagelist) * self._tilesize
        try:
            map = Image.new("RGBA", (imagewidth, imageheight), (0, 0, 0))
            if not os.path.exists(os.getcwd()+"/"+"result/"+str(self._level)):
                os.mkdir(os.getcwd()+"/"+"result/"+str(self._level))

            for i in range(0, len(imagelist)):
                for j in range(0, len(imagelist[0])):
                    im = Image.open(imagelist[i][j])
                    map.paste(im, (j*self._tilesize, i*self._tilesize))
            map.save(os.getcwd() + "/"+"result/"+str(self._level)+"/"+str(self._grid)+".tif")

            longitude = topleftX*self._tilesize*self._resolution + self._originX
            latitude = self._originY - topleftY*self._tilesize*self._resolution
            fp = open(os.getcwd() + "/"+"result/"+str(self._level)+"/"+str(self._grid)+".tfw", 'w')
            fp.write(str(self._resolution))
            fp.write("\n")
            fp.write("0")
            fp.write("\n")
            fp.write("0")
            fp.write("\n")
            fp.write(str(-self._resolution))
            fp.write("\n")
            fp.write(str(longitude))
            fp.write("\n")
            fp.write(str(latitude))
            fp.close()
        except Exception as e:
            print("拼接图像出错")
            print(e)

    def doDownload(self, row, col, savepath):
        strUrl = "".join([self._mapUrl,str(self._level), "/", str(row), "/", str(col)])
        # strSavepath = "".join([self._strTmpDir+ str(row), "_", str(col) + ".png"])
        #print(strUrl)
        if not os.path.exists(self._strTmpDir):
            os.mkdir(self._strTmpDir)
        try:
            request.urlretrieve(strUrl, savepath, reporthook=self.callbackDownload)
        except:
            img = Image.new("RGBA", (self._tilesize, self._tilesize), (255,255,255,255))
            img.save(savepath)
            print("获取图片出错！")

    @staticmethod
    def callbackDownload( blocknum, blocksize, totalsize):
        percent = 100.0 * blocknum * blocksize / totalsize
        if percent > 100:
            percent = 100
        print("%.2f%%" % percent)

import sys
if __name__ == '__main__':
    if len(sys.argv)>1:
        lv = int(sys.argv[1])
        if lv > 7 and lv < 18:
            md = MapDownloader(level=lv, maptype=1)
            md.QueryMap(105.27052617701887, 28.227887744786042, 110.25081215151275, 32.23757010272941)
    md = MapDownloader(level=8, maptype=1)
    md.QueryMap(105.27052617701887, 28.227887744786042, 110.25081215151275,32.23757010272941)

    # md.QueryMap(105.87, 29.30, 105.97, 29.40)
    # col, row = md.LongitudeLatitude2ColRow(104.20, 30.58)
    # md.doDownload(col, row)
