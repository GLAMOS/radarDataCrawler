# Copyright ETH-VAW / Glaciology
#
# Module      : Scripts.RadarDataLibrary.RadarData.RadarLine
# 
# Created by: yvow
# Created on: 29.04.2015

# Imports
import os
import datetime
import logging

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
    __PROC2_IMAGE_FILE_NAME     = "Proc2"      # Alternative file replacement for the *_mig.* files. Caused by different operators.
    __PROC2_IMAGE_FILE_TYPE     = "jpg"
    
    __NOT_A_VALUE_PLACEHOLDER = "NaN"
    __NOT_A_VALUE_VALUE       = 0.0
    
    # Radar files stored in the file system.
    __headerFile       = None
    __dataFile         = None
    __dataSummaryFile  = None
    __bedrockImageFile = None
    __mapImageFile     = None
    __migImageFile     = None

    # Basic information of the line derived from the header file.
    __lineId          = ""
    __frequencyFrom   = -1
    __frequencyTo     = -1
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
    def headerFileName(self):
        return os.path.split(self.__headerFile)[1]
        
    @headerFileName.getter
    def headerFileName(self):
        return os.path.split(self.__headerFile)[1]
    
    @property
    def dataFile(self):
        return self.__dataFile
    
    @dataFile.getter
    def dataFile(self):
        return self.__dataFile
    
    @property
    def dataFileName(self):
        return os.path.split(self.__dataFile)[1]

    @dataFileName.getter
    def dataFileName(self):
        return os.path.split(self.__dataFile)[1]
    
    @property
    def summaryFile(self):
        return self.__dataSummaryFile
    
    @summaryFile.getter
    def summaryFile(self):
        return self.__dataSummaryFile
 
    @property
    def summaryFileName(self):
        return os.path.split(self.__dataSummaryFile)[1]
    
    @summaryFileName.getter
    def summaryFileName(self):
        return os.path.split(self.__dataSummaryFile)[1]
    
    @property
    def bedrockImageFile(self):
        return self.__bedrockImageFile
    
    @bedrockImageFile.getter
    def bedrockImageFile(self):
        return self.__bedrockImageFile
  
    @property
    def bedrockImageFileName(self):
        return os.path.split(self.__bedrockImageFile)[1]
    
    @bedrockImageFileName.getter
    def bedrockImageFileName(self):
        return os.path.split(self.__bedrockImageFile)[1]      

    @property
    def mapImageFile(self):
        return self.__mapImageFile
    
    @mapImageFile.getter
    def mapImageFile(self):
        return self.__mapImageFile 

    @property
    def mapImageFileName(self):
        return os.path.split(self.__mapImageFile)[1]
    
    @mapImageFileName.getter
    def mapImageFileName(self):
        return os.path.split(self.__mapImageFile)[1] 

    @property
    def migImageFile(self):
        return self.__migImageFile
    
    @migImageFile.getter
    def migImageFile(self):
        return self.__migImageFile

    @property
    def migImageFileName(self):
        return os.path.split(self.__migImageFile)[1]
    
    @migImageFileName.getter
    def migImageFileName(self):
        return os.path.split(self.__migImageFile)[1]
    
    @property
    def frequencyFrom(self):
        return self.__frequencyFrom
    
    @frequencyFrom.getter
    def frequencyFrom(self):
        return self.__frequencyFrom

    @property
    def frequencyTo(self):
        return self.__frequencyFrom
    
    @frequencyTo.getter
    def frequencyTo(self):
        return self.__frequencyTo

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
        
        # -----------------------------------------------------
        # Retrieving and test if the given auxiliary files are existing. Throwing exceptions if not existing.
        # -----------------------------------------------------
        # PDF with the summary of header, map and bedrock.
        self.__dataSummaryFile = self.__findAuxiliaryFile(dataPath, self.__SUMMARY_FILE_NAME, self.__SUMMARY_FILE_TYPE)
        if os.path.exists(self.__dataSummaryFile) == False:
            logging.warning("Auxiliary file not found: " + self.__dataSummaryFile)
            self.__dataSummaryFile = None
            #raise RadarFileNotFoundException(self.__dataSummaryFile)
        
        # JPG of bedrock.
        self.__bedrockImageFile = self.__findAuxiliaryFile(dataPath, self.__BEDROCK_IMAGE_FILE_NAME, self.__BEDROCK_IMAGE_FILE_TYPE)
        if os.path.exists(self.__bedrockImageFile) == False:
            logging.warning("Auxiliary file not found: " + self.__bedrockImageFile)
            self.__bedrockImageFile = None
            #raise RadarFileNotFoundException(self.__bedrockImageFile)
        
        # JPG of overview map.
        self.__mapImageFile = self.__findAuxiliaryFile(dataPath, self.__MAP_IMAGE_FILE_NAME, self.__MAP_IMAGE_FILE_TYPE)
        if os.path.exists(self.__mapImageFile) == False:
            logging.warning("Auxiliary file not found: " + self.__mapImageFile)
            self.__mapImageFile = None
            #raise RadarFileNotFoundException(self.__mapImageFile)
        
        # JPG of migrated or processed data.
        self.__migImageFile = self.__findAuxiliaryFile(dataPath, self.__MIG_IMAGE_FILE_NAME, self.__MIG_IMAGE_FILE_TYPE)
        if os.path.exists(self.__migImageFile) == False:
            
            # In some cases instead of a mig file a proc2 file will be set
            self.__migImageFile = self.__findAuxiliaryFile(dataPath, self.__PROC2_IMAGE_FILE_NAME, self.__PROC2_IMAGE_FILE_TYPE)
            if os.path.exists(self.__migImageFile) == False:
                message = "The auxiliary files '" + self.__MIG_IMAGE_FILE_NAME + "' or '" + self.__PROC2_IMAGE_FILE_NAME + "' are missing."
                logging.warning(message)
                self.__migImageFile = None
                #raise RadarFileNotFoundException(message)
        # -----------------------------------------------------

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
                        
                        # Parsing the date out of the header
                        yearHeader  = self._castNumericValue(dateParts[2])
                        monthHeader = self._castNumericValue(dateParts[0])
                        dayHeader   = self._castNumericValue(dateParts[1])

                        splitPath = os.path.split(self.__headerFile)
                        headerFileName = splitPath[1]
                        dateParameters = headerFileName.split("_")[0]
                        
                        yearFilename  = self._castNumericValue(dateParameters[0:4])
                        monthFilename = self._castNumericValue(dateParameters[4:6])
                        dayFilename   = self._castNumericValue(dateParameters[6:8])
                        
                        # Check the consistency between the date information in the header and in the filename
                        if yearHeader != yearFilename or monthHeader != monthFilename or dayHeader != dayFilename:
                            message = "WARNING: Inconsistent date information between filename and header in " + str(self.__headerFile) 
                            print message
                            logging.warning(message)

                        # Constructor date: yyyy, mm, dd
                        self.__date = datetime.date(yearFilename, monthFilename, dayFilename)
                        #self.__date = datetime.date(yearHeader, monthHeader, dayHeader)
                        
                        self.__line = lineContents[4]
                        
                        self.__lineId = dateParts[2] + dateParts[0] + dateParts[1] + "_" + self.__line
                        
                    elif lineContents[0] == "C02":
                        
                        self.__acquisitionType = lineContents[2]
                        self.__instrument = lineContents[3]
                        
                    elif lineContents[0] == "C03":
                        frequencyString = lineContents[4]
                        frequencyStringSplit = frequencyString.split("-")
                        if len(frequencyStringSplit) == 2:
                            self.__frequencyFrom = int(frequencyStringSplit[0])
                            self.__frequencyTo   = int(frequencyStringSplit[1])
                        else:
                            self.__frequencyTo = int(frequencyString)
            
    
    def __str__(self):
        message = "Header file: " + str(self.__headerFile) + "\n" + "Data file: " + str(self.__dataFile) + "\n" + \
        "Number of points: " + str(len(self.__radarPoints))
        return message
    
    def _castNumericValue(self, value):
        
        parsedValue = 0
        
        # Check if the value is defined as NotAValue
        if value == self.__NOT_A_VALUE_PLACEHOLDER:
            parsedValue = self.__NOT_A_VALUE_VALUE
        elif value.isdigit():
            parsedValue = int(value)
        else:
            parsedValue = float(value)
        
        return parsedValue
        
    def analyzeRadarData(self):
        
        # Currently only bedrock measurements are supported. Implementation of a factory pattern
        # for the different types of measurements would be the next step.
        # TODO: Factory pattern for other type of measurements.
        
        with open(self.__dataFile) as dataFile:
            
            lineCounter = 0
            for dataFileLine in dataFile:
                
                lineCounter = lineCounter + 1
                
                lineContents = dataFileLine.split()
                
                #TODO: Implementing test if values are valid floats.
                xCoord = float(lineContents[1])
                yCoord = float(lineContents[2])
                
                bedrockMeasurement = BedrockMeasurement(xCoord, yCoord)
                
                # ------------ Setup of counters and 
                # Number of columns with a general meaning (e.g. profile id, easting, nothing)
                offset = 3 
                # Setting a counter to 4 which indicates the number of columns of a first result set which are analyzed in any case.
                analyzedResultColumns = 4
                # In case of multiple results, only the column Thickness and Quality are repeated.
                # The number 2 indicates the amount of repeating columns for the result.
                numberRepeatingColumns = 2
                
                if (len(lineContents) - offset) % 2 != 0:
                    message = "Number of data column does not fit!"
                    raise RadarFileFormatException(self.__dataFile, message)
                

                if len(lineContents) == offset + analyzedResultColumns:
                    numberResults = 1
                else:
                    numberColumns = len(lineContents)
                    numberResults = ((numberColumns - (offset + analyzedResultColumns)) / numberRepeatingColumns) + 1 
                
                zBed = 0.0
                zIce = 0.0
                thickness = 0.0
                quality = 0
                                                   
                # Getting all the detailed measurements parsed.
                j = 0
                while j < numberResults:
                    
                    # In case of the first set of results, 4 values have to been read.
                    if j == 0:
                        # Setting the counter of the set of result column
                        i = 0
                        
                        while i < 4:
                             
                            value = lineContents[offset + i]
                             
                            if i == 0:
                                try:
                                    zBed = self._castNumericValue(value)
                                except ValueError:
                                    raise RadarFileFormatException(self.__dataFile, "Bedrock value " + value + " wrongly formated in line " + str(lineCounter))
                            elif i == 1:

                                try:
                                    zIce = self._castNumericValue(value)
                                except ValueError:
                                    raise RadarFileFormatException(self.__dataFile, "Ice surface elevation value " + value + " wrongly formated in line " + str(lineCounter))
                                
                            elif i == 2:
                                try:
                                    thickness = self._castNumericValue(value)
                                except ValueError:
                                    raise RadarFileFormatException(self.__dataFile, "Thickness value " + value + " wrongly formated in line " + str(lineCounter))
                            elif i == 3:
                                try:
                                    quality = self._castNumericValue(value)
                                except ValueError:
                                    raise RadarFileFormatException(self.__dataFile, "Quality value " + value + " wrongly formated in line " + str(lineCounter))
                                
                            i = i + 1
                    
                    # In all other cases of multiple results, only two repeating columns have to been read (thickness and quality).
                    # The value for the ice surface will be taken by the first set of result.
                    # The value for the bedrock will be calculated based on the new thickness and ice surface.
                    else:

                        # Setting the counter of the set of result column
                        i = 0
                        while i < 2:
                            
                            value = lineContents[offset + analyzedResultColumns + i]
                            
                            
                            if i == 0:
                                try:
                                    thickness = self._castNumericValue(value)
                                except ValueError:
                                    raise RadarFileFormatException(self.__dataFile, "Thickness value " + value + " wrongly formated in line " + str(lineCounter))
                            elif i == 1:
                                try:
                                    quality = self._castNumericValue(value)
                                except ValueError:
                                    raise RadarFileFormatException(self.__dataFile, "Quality value " + value + " wrongly formated in line " + str(lineCounter))
                        
                            i = i + 1
                            
                        # Increasing the number of analyzed result columns with the number of repeating columns.
                        analyzedResultColumns += numberRepeatingColumns

                        # Reading of the existing ice surface.
                        zIce = bedrockMeasurement.results[0].zIce  
                        zBed = zIce - thickness                       
                       
                    bedrockMeasurementResult = BedrockMeasurementResult(zBed, zIce, thickness, quality)                     
                    bedrockMeasurement.addResult(bedrockMeasurementResult)
                    
                    j = j + 1

                self.__radarPoints.append(bedrockMeasurement)