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
    __testHeaderFile  = r"\\itetnas01.ee.ethz.ch\glazioarch\GlacioBaseData\RadarData\20131203_Titlis\L1\20131203_Titlis_GSSI_flight1_profil-002_Header.txt"
    __testDataPath    = r"\\itetnas01.ee.ethz.ch\glazioarch\GlacioBaseData\RadarData\20131203_Titlis\L2"
    
    # Retrieved data
    __testDataFile         = r"\\itetnas01.ee.ethz.ch\glazioarch\GlacioBaseData\RadarData\20131203_Titlis\L2\20131203_Titlis_GSSI_flight1_profil-002_Bedrock.txt"
    __numberOfPoints       = 1010
    __testSummaryFile      = r"\\itetnas01.ee.ethz.ch\glazioarch\GlacioBaseData\RadarData\20131203_Titlis\L2\20131203_Titlis_GSSI_flight1_profil-002_Summary.pdf"
    __testBedrockImageFile = r"\\itetnas01.ee.ethz.ch\glazioarch\GlacioBaseData\RadarData\20131203_Titlis\L2\20131203_Titlis_GSSI_flight1_profil-002_Bedrock.jpg"
    __testMapImageFile     = r"\\itetnas01.ee.ethz.ch\glazioarch\GlacioBaseData\RadarData\20131203_Titlis\L2\20131203_Titlis_GSSI_flight1_profil-002_Map.jpg"
    __testMigImageFile     = r"\\itetnas01.ee.ethz.ch\glazioarch\GlacioBaseData\RadarData\20131203_Titlis\L2\20131203_Titlis_GSSI_flight1_profil-002_Proc2.jpg"

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
        self.assertEqual(self.__radarLine.frequency, 65, "Test of parsed frequency")
        
    def testLineProperty(self):
        self.assertEqual(self.__radarLine.line, "002", "Test of parsed line identifier")
        
    def testLineIdProperty(self):
        self.assertEqual(self.__radarLine.lineId, "20130312_002", "Test of concatenated line identifier")
        
    def testDateProperty(self):
        self.assertEqual(self.__radarLine.date, datetime.date(2013, 12, 03), "Test of parsed date")
        
    def testAcqusitionTypeProperty(self):
        self.assertEqual(self.__radarLine.acquisitionType, "AIRBORN", "Test of parsed acquisition type")
        
    def testInstrumentProperty(self):
        self.assertEqual(self.__radarLine.instrument, "GSSI", "Test of parsed instrument")
        
    def testCountRadarPointsProperty(self):
        self.assertEqual(self.__radarLine.countRadarPoints, self.__numberOfPoints, "Amount of analyzed radar points")
        
    def testCountRadarPointBedrockMeasurementResult(self):
        bedrockMeasurementResult = self.__radarLine.radarPoints[230].results[0]

        self.assertEqual(bedrockMeasurementResult.zBed,      2319.518, "Elevation of bedrock")
        self.assertEqual(bedrockMeasurementResult.zIce,      2459.530, "Elevation of ice surface")
        self.assertEqual(bedrockMeasurementResult.thickness,  140.012, "Ice thickness")
        self.assertEqual(bedrockMeasurementResult.quality,          2, "Quality")
        
    def testCountRadarPointBedrockMeasurementCountResults(self):
        
        self.assertEqual(self.__radarLine.radarPoints[250].countResults, 2, "Point with two sets of results")
        self.assertEqual(self.__radarLine.radarPoints[300].countResults, 2, "Point with two sets of results")
        self.assertEqual(self.__radarLine.radarPoints[350].countResults, 2, "Point with two sets of results")
        self.assertEqual(self.__radarLine.radarPoints[400].countResults, 2, "Point with two sets of results")
        self.assertEqual(self.__radarLine.radarPoints[450].countResults, 2, "Point with two sets of results")
        
    def testCountRadarPointBedrockMeasurementMultipleResult(self):
        
        bedrockMeasurement = self.__radarLine.radarPoints[111]
        
        if bedrockMeasurement.countResults != 3:
            self.fail("Not correct number of mutliple results")

        self.assertEqual(bedrockMeasurement.results[0].zBed,      2333.282, "Elevation of bedrock")
        self.assertEqual(bedrockMeasurement.results[0].zIce,      2452.060, "Elevation of ice surface")
        self.assertEqual(bedrockMeasurement.results[0].thickness,  118.778, "Ice thickness")
        self.assertEqual(bedrockMeasurement.results[0].quality,          2, "Quality")
        
        self.assertEqual(bedrockMeasurement.results[1].zBed,      2358.286, "Elevation of bedrock")
        self.assertEqual(bedrockMeasurement.results[1].zIce,      2452.060, "Elevation of ice surface")
        self.assertEqual(bedrockMeasurement.results[1].thickness,   93.774, "Ice thickness")
        self.assertEqual(bedrockMeasurement.results[1].quality,         12, "Quality")
        
        #self.assertEqual(bedrockMeasurement.results[2].zBed,      2301.560, "Elevation of bedrock")
        self.assertEqual(bedrockMeasurement.results[2].zIce,      2452.060, "Elevation of ice surface")
        #self.assertEqual(bedrockMeasurement.results[2].thickness,  150.500, "Ice thickness")
        self.assertEqual(bedrockMeasurement.results[2].quality,         22, "Quality")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testHeaderFile']
    unittest.main()