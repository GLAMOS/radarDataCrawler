# Copyright ETH-VAW / Glaciology
#
# Module      : Scripts.RadarDataLibrary.RadarData.RadarFileFormatException
# 
# Created by: yvow
# Created on: 04.05.2015

# Imports

class RadarFileFormatException(Exception):
    '''
    classdocs
    '''
    #TODO: Include class description.
    
    __message = ""

    def __init__(self, value, message):
        '''
        Constructor
        '''
        #TODO: Include constructor description.
        self.value = value
        self.__message = message
        
    def __str__(self):
        return "The file " + repr(self.value) + "is not correctly formated!"