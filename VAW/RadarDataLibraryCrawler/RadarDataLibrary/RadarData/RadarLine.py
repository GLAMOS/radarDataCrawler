# Copyright ETH-VAW / Glaciology
#
# Module      : Scripts.RadarDataLibrary.RadarData.RadarLine
# 
# Created by: yvow
# Created on: 29.04.2015

# Imports
import os
import datetime

from RadarFileNotFoundException import RadarFileNotFoundException
from RadarFileFormatException import RadarFileFormatException 
from BedrockMeasurement import BedrockMeasurement
from BedrockMeasurement import BedrockMeasurementResult

class RadarLine(object):
    '''
    classdocs
    '''
    #TODO: Include class description.
    
    # Constants
    __HEADER_FILE_NAME  = "Header"
    __HEADER_FILE_TYPE  = "txt"
    __BEDROCK_FILE_NAME = "Bedrock"
    __BEDROCK_FILE_TYPE = "txt"
    __SUMMARY_FILE_NAME = "Summary"
    __SUMMARY_FILE_TYPE = "pdf"
    
    __BEDROCK_IMAGE_FILE_NAME = "Bedrock"
    __BEDROCK_IMAGE_FILE_TYPE = "jpg"
    __MAP_IMAGE_FILE_NAME     = "Map"
    __MAP_IMAGE_FILE_TYPE     = "jpg"
    __MIG_IMAGE_FILE_NAME     = "Mig"
    __MIG_IMAGE_FILE_TYPE     = "jpg"
    
    # Radar files stored in the file system.
    __headerFile       = None
    __dataFile         = None
    __dataSummaryFile  = None
    __bedrockImageFile = None
    __mapImageFile     = None
    __migImageFile     = None

    # Basic information of the line derived from the header file.
    __lineId          = ""
    __frequency       = -1
    __line            = "-999"
    __date            = datetime.date(1900, 01, 01)
    __acquisitionType = "UNKNOWN"
    __instrument      = "UNKNONW"
    
    # Collection of individual radar measurements along the line.
    __radarPoints = None
    
    @property
    def headerFile(self):
        return self.__headerFile
        
    @headerFile.getter
    def headerFile(self):
        return self.__headerFile
    
    @property
    def dataFile(self):
        return self.__dataFile
    
    @dataFile.getter
    def dataFile(self):
        return self.__dataFile
    
    @property
    def summaryFile(self):
        return self.__dataSummaryFile
    
    @summaryFile.getter
    def summaryFile(self):
        return self.__dataSummaryFile
    
    @property
    def bedrockImageFile(self):
        return self.__bedrockImageFile
    
    @bedrockImageFile.getter
    def bedrockImageFile(self):
        return self.__bedrockImageFile

    @property
    def mapImageFile(self):
        return self.__mapImageFile
    
    @mapImageFile.getter
    def mapImageFile(self):
        return self.__mapImageFile 

    @property
    def migImageFile(self):
        return self.__migImageFile
    
    @migImageFile.getter
    def migImageFile(self):
        return self.__migImageFile
    
    @property
    def frequency(self):
        return self.__frequency
    
    @frequency.getter
    def frequency(self):
        return self.__frequency
    
    @property
    def line(self):
        return self.__line
    
    @line.getter
    def line(self):
        return self.__line
    
    @property
    def lineId(self):
        return self.__lineId
    
    @lineId.getter
    def lineId(self):
        return self.__lineId
    
    @property
    def date(self):
        return self.__date
    
    @date.getter
    def date(self):
        return self.__date
    
    @property
    def acquisitionType(self):
        return self.__acquisitionType
    
    @acquisitionType.getter
    def acquisitionType(self):
        return self.__acquisitionType
    
    @property
    def instrument(self):
        return self.__instrument
    
    @instrument.getter
    def instrument(self):
        return self.__instrument
    
    @property
    def countRadarPoints(self):
        return len(self.__radarPoints)
    
    @countRadarPoints.getter
    def countRadarPoints(self):
        return len(self.__radarPoints)
    
    @property
    def radarPoints(self):
        return self.__radarPoints
    
    @radarPoints.getter
    def radarPoints(self):
        return self.__radarPoints

    def __init__(self, headerFile, dataPath):
        '''
        Constructor
        '''
        #TODO: Include constructor description.
        
        # Test if the giving header file is existing. Throwing exceptions if not existing.
        if os.path.exists(headerFile) == False:
            raise RadarFileNotFoundException(headerFile)
        
        self.__headerFile = headerFile
        
        # Retrieving and test if the giving data file is existing. Throwing exceptions if not existing.
        self.__dataFile = self.__findDataFile(dataPath)
        if os.path.exists(self.__dataFile) == False:
            raise RadarFileNotFoundException(self.__dataFile)
        
        # Retrieving and test if the given auxiliary files are existing. Throwing exceptions if not existing.
        self.__dataSummaryFile = self.__findAuxiliaryFile(dataPath, self.__SUMMARY_FILE_NAME, self.__SUMMARY_FILE_TYPE)
        if os.path.exists(self.__dataSummaryFile) == False:
            raise RadarFileNotFoundException(self.__dataSummaryFile)
        
        self.__bedrockImageFile = self.__findAuxiliaryFile(dataPath, self.__BEDROCK_IMAGE_FILE_NAME, self.__BEDROCK_IMAGE_FILE_TYPE)
        if os.path.exists(self.__bedrockImageFile) == False:
            raise RadarFileNotFoundException(self.__bedrockImageFile)
        
        self.__mapImageFile = self.__findAuxiliaryFile(dataPath, self.__MAP_IMAGE_FILE_NAME, self.__MAP_IMAGE_FILE_TYPE)
        if os.path.exists(self.__mapImageFile) == False:
            raise RadarFileNotFoundException(self.__mapImageFile)
        
        self.__migImageFile = self.__findAuxiliaryFile(dataPath, self.__MIG_IMAGE_FILE_NAME, self.__MIG_IMAGE_FILE_TYPE)
        if os.path.exists(self.__migImageFile) == False:
            raise RadarFileNotFoundException(self.__migImageFile)

        # Initializing a new list of individual radar points.
        self.__radarPoints = list()
        
        # Reading the basic information out of the header file.
        self.__parseHeaderFile()


    def __findDataFile(self, dataPath):
        splitPath = os.path.split(self.__headerFile)
        headerFileName = splitPath[1]
        
        dataFileName = headerFileName.replace(self.__HEADER_FILE_NAME, self.__BEDROCK_FILE_NAME)

        return os.path.join(str(dataPath), str(dataFileName))

    
    def __findAuxiliaryFile(self, dataPath, auxiliaryFileName, auxiliaryFileType):
        splitPath = os.path.split(self.__headerFile)
        headerFileName = splitPath[1]
        
        auxiliaryName = headerFileName.replace(self.__HEADER_FILE_NAME, auxiliaryFileName)
        auxiliaryName = auxiliaryName.replace(self.__HEADER_FILE_TYPE, auxiliaryFileType)

        return os.path.join(str(dataPath), str(auxiliaryName))
    
    def __parseHeaderFile(self):
        
        with open(self.__headerFile) as headerFile:
            
            for headerFileLine in headerFile:
            
                lineContents = headerFileLine.split()
            
                if len(lineContents) > 0:
                    if lineContents[0] == "C01":
                        
                        dateParts = lineContents[2].split('/')
                        self.__date = datetime.date(int(dateParts[2]), int(dateParts[0]), int(dateParts[1]))
                        
                        self.__line = lineContents[4]
                        
                        self.__lineId = dateParts[2] + dateParts[0] + dateParts[1] + "_" + self.__line
                        
                    elif lineContents[0] == "C02":
                        
                        self.__acquisitionType = lineContents[2]
                        self.__instrument = lineContents[3]
                        
                    elif lineContents[0] == "C03":
                        self.__frequency = int(lineContents[4])
            
    
    def __str__(self):
        message = "Header file: " + str(self.__headerFile) + "\n" + "Data file: " + str(self.__dataFile) + "\n" + \
        "Number of points: " + str(len(self.__radarPoints))
        return message
        
    def analyzeRadarData(self):
        
        # Currently only bedrock measurements are supported. Implementation of a factory pattern
        # for the different types of measurements would be the next step.
        #TODO: Factory pattern for other type of measurements.
        
        with open(self.__dataFile) as dataFile:
            
            lineCounter = 0
            for dataFileLine in dataFile:
                
                lineCounter = lineCounter + 1
                
                lineContents = dataFileLine.split()
                
                #TODO: Implementing test if values are valid floats.
                xCoord = float(lineContents[1])
                yCoord = float(lineContents[2])
                
                bedrockMeasurement = BedrockMeasurement(xCoord, yCoord)
                
                offset = 3
                if (len(lineContents) - offset) % 4 != 0:
                    message = "Number of data column does not fit!"
                    raise RadarFileFormatException(self.__dataFile, message)
                
                numberResults = (len(lineContents) - offset) / 4
                
                zBed = 0.0
                zIce = 0.0
                thickness = 0.0
                quality = 0
                                    
                # Getting all the detailed measurements parsed.
                j = 0
                while j < numberResults:
                    
                    i = 0
                    while i < 4:
                        
                        value = lineContents[offset + i]
                        
                        if i == 0:
                            try:
                                zBed = float(value)
                            except:
                                raise RadarFileFormatException(self.__dataFile, "Bedrock value " + value + " wrongly formated in line " + str(lineCounter))
                        elif i == 1:
                            try:
                                zIce = float(value)
                            except:
                                raise RadarFileFormatException(self.__dataFile, "Ice surface elevation value " + value + " wrongly formated in line " + str(lineCounter))
                        elif i == 2:
                            try:
                                thickness = float(value)
                            except:
                                raise RadarFileFormatException(self.__dataFile, "Thickness value " + value + " wrongly formated in line " + str(lineCounter))
                        elif i == 3:
                            try:
                                quality = float(value)
                            except:
                                raise RadarFileFormatException(self.__dataFile, "Quality value " + value + " wrongly formated in line " + str(lineCounter))
                        
                        i = i + 1
                        
                       
                    bedrockMeasurementResult = BedrockMeasurementResult(zBed, zIce, thickness, quality)
                                              
                    bedrockMeasurement.addResult(bedrockMeasurementResult)
                    
                    offset = offset + 4  
                    j = j + 1

                self.__radarPoints.append(bedrockMeasurement)