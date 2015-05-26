# Copyright ETH-VAW / Glaciology
#
# Module     : Scripts.RadarDataLibrary.RadarDataLibraryPrototype
# 
# Created by: yvow
# Created on: 29.04.2015

'''
Main module to launch the analysis of ASCII-based radar data.

The module starts the analysis of a given directory of L1 radar header file. Based on the header information, 
all additional information an data a retrieved and converted as shapefile.
'''

# Imports
from RadarDataLibraryCrawler import RadarDataLibraryCrawler
import os
from exceptions import OSError

class FileNotFoundError(OSError):
    pass

class RadarDirectoryStructure(object):
    
    __baseName        = None
    __headerDirectory = None
    __dataDirectory   = None
    
    @property
    def baseName(self):
        return self.__baseName
        
    @baseName.getter
    def baseName(self):
        return self.__baseName
    
    @property
    def headerDirectory(self):
        return self.__headerDirectory
        
    @headerDirectory.getter
    def headerDirectory(self):
        return self.__headerDirectory
    
    @property
    def dataDirectory(self):
        return self.__dataDirectory
        
    @dataDirectory.getter
    def dataDirectory(self):
        return self.__dataDirectory
    
    def __init__(self, baseName, headerDirectory, dataDirectory):
        '''
        Constructor
        '''
        #TODO: Include constructor description.
        
        # Test if the giving header file is existing. Throwing exceptions if not existing.
        if os.path.exists(headerDirectory) == False:
            raise FileNotFoundError(headerDirectory)
        if os.path.exists(dataDirectory) == False:
            raise FileNotFoundError(dataDirectory)
        
        self.__baseName        = baseName  
        self.__headerDirectory = headerDirectory
        self.__dataDirectory   = dataDirectory
        
    def __str__(self):
        message = "Radar data structure '" + str(self.__baseName) + "':\nHeader -> " + str(self.__headerDirectory)  + "\nData   -> " + str(self.__dataDirectory)
        return message


# ------------------------------------------------------------------------------------------------
# --------------- Start of Radar Data Parsing ----------------------------------------------------
# ------------------------------------------------------------------------------------------------

# Setting up the data structure to be analyzed.
radarDataDirectories = list()
with open("RadarDataDirectories.txt") as inputDirectories:
    for dataFileLine in inputDirectories:
        lineContents = dataFileLine.split()
        radarDataDirectories.append(RadarDirectoryStructure(lineContents[0], lineContents[1], lineContents[2]))


# -------------- User input --------------
# headerDirectory = r"\\itetnas01.ee.ethz.ch\glazioarch\GlacioBaseData\RadarData\20131203_Titlis\L1"
# dataDirectory   = r"\\itetnas01.ee.ethz.ch\glazioarch\GlacioBaseData\RadarData\20131203_Titlis\L2"
# 
# radarDataStructure = RadarDirectoryStructure("20131203_Titlis", headerDirectory, dataDirectory)

# ---------- Static settings for the parsing --------
shapeDirectory  = r"\\itetnas01.ee.ethz.ch\glazioarch\GlacioBaseData\RadarData\gis"
shapeFileNameLine  = "RadarArchive_L2_Lines_lv03.shp"
shapeFileNamePoint = "RadarArchive_L2_Points_lv03.shp"
# ---------------------------------------------------


structureAnalyzed = 0

for radarDataDirectory in radarDataDirectories:
    
    print "Currently analyzed structure:\n" + str(radarDataDirectory)
    
    radarDataLibraryCrawler = RadarDataLibraryCrawler(radarDataDirectory.headerDirectory, radarDataDirectory.dataDirectory, shapeDirectory, shapeFileNameLine, shapeFileNamePoint)
    
    if structureAnalyzed == 0:
        radarDataLibraryCrawler.writeGeometries(False)
    else:
        radarDataLibraryCrawler.writeGeometries(True)

    structureAnalyzed += 1