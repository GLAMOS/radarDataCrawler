# Copyright ETH-VAW / Glaciology
#
# Module      : Scripts.RadarDataLibrary.RadarDataLibraryCrawler
# 
# Created by: yvow
# Created on: 05.05.2015

# Imports
import os
from os import walk
from os.path import splitext, join
import logging

from RadarData.RadarLine import RadarLine
from RadarData.RadarDataShapefileWriter import EsriShapefileWriter

class RadarDataLibraryCrawler(object):
    '''
    Helper class crawling through the given directories to retrieve all available radar data header files.
    Based on the header files the detailed information about each individual radar survey line will be retrieved.
    
    The class allows further analysis and data storage of the found radar information.
    '''
    
    __RADAR_DATA_FILE_TYPE = ".txt"
    
    __LOG_FILE_NAME        = "RadarCrawlerLog.log"
    
    __headerDirectory    = None
    __dataDirectory      = None
    __shapeDirectory     = None
    __shapefileLine      = None
    __shapefilePoint     = None
    
    __selectedFiles      = []
    
    @property
    def radarLineDataLineCount(self):
        return len(self.__selectedFiles)
        
    @radarLineDataLineCount.getter
    def radarLineDataLineCount(self):
        return len(self.__selectedFiles)
    
    @property
    def radarLineDataLines(self):
        return self.__selectedFiles
        
    @radarLineDataLines.getter
    def radarLineDataLines(self):
        return self.__selectedFiles
    
    
    def __init__(self, headerDirectory, dataDirectory, shapeDirectory, shapefileNameLine, shapefileNamePoint):
        
        self.__headerDirectory    = headerDirectory
        self.__dataDirectory      = dataDirectory
        self.__shapeDirectory     = shapeDirectory
        self.__shapefileLine      = os.path.join(shapeDirectory, shapefileNameLine)
        self.__shapefilePoint     = os.path.join(shapeDirectory, shapefileNamePoint)
        
        self.__selectedFiles = self.__buildRecursiveDirectoryTree(self.__headerDirectory, [self.__RADAR_DATA_FILE_TYPE])
        
        # Getting the default of the logger set.
        logging.basicConfig(filename = self.__LOG_FILE_NAME, level = logging.WARNING)

    
    def __buildRecursiveDirectoryTree(self, path, fileExtensions):
        """
        Walks recursively through a tree of directories.
        
        @param path: Root directory to start analysis.
        @type path: UNC path
        
        @return: Array with selected files matching a given pattern. 
        """
        
        print "The following file extensions are analyzed: "
        for fileExtension in fileExtensions:
            print "-> " + fileExtension
    
        selectedFiles = []
    
        for root, dirs, files in walk(path):
            print "Current depth of directory from root: " + str(len(dirs))
            selectedFiles += self.__selectFiles(root, files, fileExtensions)
    
        return selectedFiles
    
    def __selectFiles(self, root, files, fileExtensions):
        """
        Recursive function to walk through a given directory tree.
        Adds all the files with the given (hard coded) extensions into an array.
        
        @param root: Current directory to be analyzed.
        @param files: Files within the directory to be analyzed.
        
        @return: Array with all the dataset fitting the given file extensions.
        """
    
        selectedFiles = []
    
        for foundFile in files:
            # Concatenation to get full path 
            fullPath = join(root, foundFile)
            ext = splitext(foundFile)[1]
            
            for fileExtension in fileExtensions:
                if ext.upper() == fileExtension.upper():
                    selectedFiles.append(fullPath)
    
        return selectedFiles
    
    def writeGeometries(self):
        """
        Writes the found information of the radar lines and radar points into 
        the given shapefiles.
        """
        
        message = "Number of header files found: " + str(len(self.__selectedFiles)) 
        print message 
        logging.info(message)
        
        fileCounter = 0
        
        for selectedFile in self.__selectedFiles:
            
            fileCounter = fileCounter + 1
            doAppend = True
            
            message = str(fileCounter) + " -> " + selectedFile
            print message 
            logging.info(message)
            
            radarLine = RadarLine(selectedFile, self.__dataDirectory)
            radarLine.analyzeRadarData()
            
            if fileCounter == 1:
                doAppend = False
            
            esriShapefileWriter = EsriShapefileWriter(radarLine, self.__shapefileLine, self.__shapefilePoint, doAppend)
            esriShapefileWriter.writeData()
            
            print str(radarLine)
            logging.info(str(radarLine))
            
            
            
            
            
            