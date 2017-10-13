'''
Created on 03.05.2015

@author: yvow
'''
import unittest

from BedrockMeasurement import BedrockMeasurement
from BedrockMeasurement import BedrockMeasurementResult


class Test(unittest.TestCase):
    

    # User input data
    __xCoord  = 600000
    __yCoord  = 200000
    
    __resultObjects = list()
    
    # Bedrock measurement object to be tested.
    __bedrockMeasurement = None


    def setUp(self):
        self.__bedrockMeasurement = BedrockMeasurement(self.__xCoord, self.__yCoord)
        
        self.__resultObjects.append(BedrockMeasurementResult(0, 0, 0, 0))
        self.__resultObjects.append(BedrockMeasurementResult(0, 0, 0, 0))
        
        for resultObject in self.__resultObjects:
            self.__bedrockMeasurement.addResult(resultObject)


    def tearDown(self):
        del(self.__bedrockMeasurement)


    def testXCoordinatesProperty(self):
        self.assertEqual(self.__bedrockMeasurement.xCoordinate, self.__xCoord, "X coordinate of the measurement")
    
    def testYCoordinatesProperty(self):
        self.assertEqual(self.__bedrockMeasurement.yCoordinate, self.__yCoord, "X coordinate of the measurement")
        
    def testCountResultsProperty(self):
        self.assertEqual(self.__bedrockMeasurement.countResults, len(self.__resultObjects), "Number of result at the current location")
        
    def testBedrockMeasurementResultProperties(self):
        
        zBed        = 2200
        zIceSurface = 2400
        thickness   = 200
        quality     = 2
        
        bedrockMeasurementResult = BedrockMeasurementResult(zIceSurface, zBed, thickness, quality)
        
        self.assertEqual(bedrockMeasurementResult.zBed,        zBed,        "Elevation of bedrock")
        self.assertEqual(bedrockMeasurementResult.zIceSurface, zIceSurface, "Elevation of ice surface")
        self.assertEqual(bedrockMeasurementResult.thickness,   thickness,   "Ice thickness")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testXCoordinatesProperty']
    unittest.main()