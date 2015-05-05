'''
Created on 01.05.2015

@author: yvow
'''
import unittest

from RadarLine import RadarLine
from RadarFileNotFoundException import RadarFileNotFoundException
import datetime

class Test(unittest.TestCase):

    # User input data
    __testHeaderFile  = r"\\itetnas01.ee.ethz.ch\glazioarch\_INCOMING\20090331_Aletsch\L1\20090331_Aletsch_BGR_flight1_profil-001_Header.txt"
    __testDataPath    = r"\\itetnas01.ee.ethz.ch\glazioarch\_INCOMING\20090331_Aletsch\L2"
    
    # Retrieved data
    __testDataFile         = r"\\itetnas01.ee.ethz.ch\glazioarch\_INCOMING\20090331_Aletsch\L2\20090331_Aletsch_BGR_flight1_profil-001_Bedrock.txt"
    __numberOfPoints       = 2013
    __testSummaryFile      = r"\\itetnas01.ee.ethz.ch\glazioarch\_INCOMING\20090331_Aletsch\L2\20090331_Aletsch_BGR_flight1_profil-001_Summary.pdf"
    __testBedrockImageFile = r"\\itetnas01.ee.ethz.ch\glazioarch\_INCOMING\20090331_Aletsch\L2\20090331_Aletsch_BGR_flight1_profil-001_Bedrock.jpg"
    __testMapImageFile     = r"\\itetnas01.ee.ethz.ch\glazioarch\_INCOMING\20090331_Aletsch\L2\20090331_Aletsch_BGR_flight1_profil-001_Map.jpg"
    __testMigImageFile     = r"\\itetnas01.ee.ethz.ch\glazioarch\_INCOMING\20090331_Aletsch\L2\20090331_Aletsch_BGR_flight1_profil-001_Mig.jpg"

    # Radar line object to be tested.
    __radarLine = None

    def setUp(self):

        self.__radarLine = RadarLine(self.__testHeaderFile, self.__testDataPath)
        self.__radarLine.analyzeRadarData()

    def tearDown(self):
        del(self.__radarLine)

    def testHeaderFileProperty(self):
        self.assertEqual(self.__radarLine.headerFile, self.__testHeaderFile, "Test of HeaderFile property")
    
    def testDataFileProperty(self):
        self.assertEqual(self.__radarLine.dataFile, self.__testDataFile, "Test of DataFile property")
        
    def testHeaderFileNotExisting(self):
        self.assertRaises(RadarFileNotFoundException, RadarLine, "this is not a file" , "this is not a path")
        
    def testSummaryFileProperty(self):
        self.assertEqual(self.__radarLine.summaryFile, self.__testSummaryFile, "Test of SummaryFile property")
        
    def testAuxiliaryFileProperties(self):
        self.assertEqual(self.__radarLine.bedrockImageFile, self.__testBedrockImageFile, "Test of BedrockImageFile property")
        self.assertEqual(self.__radarLine.mapImageFile,     self.__testMapImageFile,     "Test of MapImageFile property")
        self.assertEqual(self.__radarLine.migImageFile,     self.__testMigImageFile,     "Test of MigImageFile property")
        
    def testFrequencyProperty(self):
        self.assertEqual(self.__radarLine.frequency, 30, "Test of parsed frequency")
        
    def testLineProperty(self):
        self.assertEqual(self.__radarLine.line, "001", "Test of parsed line identifier")
        
    def testLineIdProperty(self):
        self.assertEqual(self.__radarLine.lineId, "20090331_001", "Test of concatenated line identifier")
        
    def testDateProperty(self):
        self.assertEqual(self.__radarLine.date, datetime.date(2009, 03, 31), "Test of parsed date")
        
    def testAcqusitionTypeProperty(self):
        self.assertEqual(self.__radarLine.acquisitionType, "AIRBORN", "Test of parsed acquisition type")
        
    def testInstrumentProperty(self):
        self.assertEqual(self.__radarLine.instrument, "BGR-P30", "Test of parsed instrument")
        
    def testCountRadarPointsProperty(self):
        self.assertEqual(self.__radarLine.countRadarPoints, self.__numberOfPoints, "Amount of analyzed radar points")
        
    def testCountRadarPointBedrockMeasurementResult(self):
        bedrockMeasurementResult = self.__radarLine.radarPoints[1973].results[0]

        self.assertEqual(bedrockMeasurementResult.zBed,      2555.906, "Elevation of bedrock")
        self.assertEqual(bedrockMeasurementResult.zIce,      2686.200, "Elevation of ice surface")
        self.assertEqual(bedrockMeasurementResult.thickness,  130.294, "Ice thickness")
        self.assertEqual(bedrockMeasurementResult.quality,          2, "Quality")
        
    def testCountRadarPointBedrockMeasurementCountResults(self):
        
        self.assertEqual(self.__radarLine.radarPoints[1975].countResults, 1, "Multiple results")
        self.assertEqual(self.__radarLine.radarPoints[1976].countResults, 2, "Multiple results")
        self.assertEqual(self.__radarLine.radarPoints[1977].countResults, 2, "Multiple results")
        self.assertEqual(self.__radarLine.radarPoints[1978].countResults, 3, "Multiple results")
        self.assertEqual(self.__radarLine.radarPoints[1979].countResults, 1, "Multiple results")
        
    def testCountRadarPointBedrockMeasurementMultipleResult(self):
        bedrockMeasurement = self.__radarLine.radarPoints[1978]

        self.assertEqual(bedrockMeasurement.results[0].zBed,      2560.908, "Elevation of bedrock")
        self.assertEqual(bedrockMeasurement.results[0].zIce,      2685.770, "Elevation of ice surface")
        self.assertEqual(bedrockMeasurement.results[0].thickness,  124.862, "Ice thickness")
        self.assertEqual(bedrockMeasurement.results[0].quality,          2, "Quality")
        
        self.assertEqual(bedrockMeasurement.results[1].zBed,      2540.816, "Elevation of bedrock")
        self.assertEqual(bedrockMeasurement.results[1].zIce,      2687.400, "Elevation of ice surface")
        self.assertEqual(bedrockMeasurement.results[1].thickness,  146.584, "Ice thickness")
        self.assertEqual(bedrockMeasurement.results[1].quality,          2, "Quality")
        
        self.assertEqual(bedrockMeasurement.results[2].zBed,      2568.520, "Elevation of bedrock")
        self.assertEqual(bedrockMeasurement.results[2].zIce,      2684.840, "Elevation of ice surface")
        self.assertEqual(bedrockMeasurement.results[2].thickness,  116.319, "Ice thickness")
        self.assertEqual(bedrockMeasurement.results[2].quality,          2, "Quality")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testHeaderFile']
    unittest.main()