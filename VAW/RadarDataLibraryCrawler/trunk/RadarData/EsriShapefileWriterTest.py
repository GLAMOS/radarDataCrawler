'''
Created on 04.05.2015

@author: yvow
'''
import unittest

from RadarLine import RadarLine
from RadarDataShapefileWriter import EsriShapefileWriter

class Test(unittest.TestCase):
    
    # Writer object to be tested.
    __shapefileWriter = None
    
    # Shapefiles to be created
    __shapeFileLine  = r"D:\GIS\GlaciologyDatabase\MiscellaneousScripts\Scripts\RadarDataLibrary\Shapefiles\RadarArchive_L2_Lines_lv03.shp"
    __shapeFilePoint = r"D:\GIS\GlaciologyDatabase\MiscellaneousScripts\Scripts\RadarDataLibrary\Shapefiles\RadarArchive_L2_Points_lv03.shp"
    
    # Radar line for testing
    __testHeaderFile  = r"\\itetnas01.ee.ethz.ch\glazioarch\_INCOMING\20090331_Aletsch\L1\20090331_Aletsch_BGR_flight1_profil-001_Header.txt"
    __testDataPath    = r"\\itetnas01.ee.ethz.ch\glazioarch\_INCOMING\20090331_Aletsch\L2"
    __numberOfPoints  = 2013

    def setUp(self):
        # Getting the radar line ready.
        self.__radarLine = RadarLine(self.__testHeaderFile, self.__testDataPath)
        self.__radarLine.analyzeRadarData()
        
        self.__shapefileWriter = EsriShapefileWriter(self.__radarLine, self.__shapeFileLine, self.__shapeFilePoint, False)


    def tearDown(self):
        del(self.__shapefileWriter)


    def testRadarLineProperty(self):
        self.assertEqual(self.__shapefileWriter.radarLine.countRadarPoints, self.__numberOfPoints, "Amount of radar points to be written")
        
    def testWriteData(self):
        self.__shapefileWriter.writeData()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()