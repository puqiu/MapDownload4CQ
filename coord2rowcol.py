import math
import os
from PIL import Image
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True


class Coord2RowCol(object):
    def __init__(self, level=16, maptype=1, grid="all"):
        self._tilesize = 256
        self._originX = -180
        self._originY = 90
        self._mapUrl = r"http://www.digitalcq.com/RemoteRest/services/CQMap_VEC/MapServer/tile/"
        self._satilateUrl = r"http://www.digitalcq.com/RemoteRest/services/CQMap_IMG/MapServer/tile/"
        self._grid = grid
        self._fileList = []

        self._mapleveldic = {
            8: (1154287.4728857423, 0.002746582031250001),
            9: (577143.7364428712, 0.0013732910156250004),
            10: (288571.8682214356, 6.866455078125002E-4),
            11: (144285.9341107178, 3.433227539062501E-4),
            12: (72142.9670553589, 1.7166137695312505E-4),
            13: (36071.48352767945, 8.583068847656253E-5),
            14: (18035.741763839724, 4.2915344238281264E-5),
            15: (9017.870881919862, 2.1457672119140632E-5),
            16: (4508.935440959931, 1.0728836059570316E-5),
            17: (2254.4677204799655, 5.364418029785158E-6)
        }

        if maptype == 2:
            self._mapUrl = self._satilateUrl
        self._level = level
        self._strTmpDir = os.getcwd() + "/" + str(self._level) + "/"
        if not os.path.exists(self._strTmpDir):
            os.mkdir(self._strTmpDir)
        try:
            self._resolution = self._mapleveldic[self._level][1]
        except:
            print("地图级别设置错误：支持8-18级")

    def longitudeLatitude2ColRow(self, longitude, latitude):
        col = int(math.floor((longitude - self._originX) / (self._resolution * self._tilesize)))
        row = int(math.floor((self._originY - latitude) / (self._resolution * self._tilesize)))
        return col, row

    def coordtoQuant(self, topleftLongitude, topleftLatutide, bottomrightLongitude, bottomrightLatitude):
        topLeftCol, toplefRow = self.longitudeLatitude2ColRow(topleftLongitude, topleftLatutide)
        boRightCol, boRightRow = self.longitudeLatitude2ColRow(bottomrightLongitude, bottomrightLatitude)

        minCol = topLeftCol if topLeftCol < boRightCol else boRightCol
        minRow = toplefRow if toplefRow < boRightRow else boRightRow
        maxCol = topLeftCol if topLeftCol >= boRightCol else boRightCol
        maxRow = toplefRow if toplefRow >= boRightRow else boRightRow

        # modify in 20161124, correct the coordinate problem,switch the Col and Row
        self._topleftx = minCol
        self._toplefty = minRow

        urls = {}
        for i in range(minRow, maxRow + 1):
            imagerow = []
            for j in range(minCol, maxCol + 1):
                filename = self._strTmpDir + str(i) + "-" + str(j)
                imagerow.append(filename+".png")
                url = "".join([self._mapUrl, str(self._level), "/", str(i), "/", str(j)])
                urls[filename] = url
            self._fileList.append(imagerow)

        return urls

    def mergemap(self, imgtype='.jpg'):
        if not self._fileList:
           return

        _filetype = ".jpg"
        _coordfiletype = ".jpw"

        if imgtype == 'tiff':
            _filetype = ".tif"
            _coordfiletype = ".tfw"

        imagewidth = len( self._fileList[0]) * self._tilesize
        imageheight = len( self._fileList) * self._tilesize

        if os.path.exists(os.getcwd() + "/" + "result/" + str(self._level) + "/" + str(self._grid) +_filetype):
            return

        try:
            map = Image.new("RGBA", (imagewidth, imageheight), (0, 0, 0))
            if not os.path.exists(os.getcwd() + "/" + "result/" + str(self._level)):
                os.mkdir(os.getcwd() + "/" + "result/" + str(self._level))

            for i in range(0, len(self._fileList)):
                for j in range(0, len(self._fileList[0])):
                    try:
                        im = Image.open(self._fileList[i][j])
                    except:
                        im = Image.new("RGBA", (self._tilesize, self._tilesize), (255, 255, 255, 255))
                    map.paste(im, (j * self._tilesize, i * self._tilesize))
            map.save(os.getcwd() + "/" + "result/" + str(self._level) + "/" + str(self._grid) +_filetype)

            longitude = self._topleftx * self._tilesize * self._resolution + self._originX
            latitude = self._originY - self._toplefty * self._tilesize * self._resolution
            fp = open(os.getcwd() + "/" + "result/" + str(self._level) + "/" + str(self._grid) + _coordfiletype, 'w')
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


