# Copyright ETH-VAW / Glaciology
#
# Module      : Scripts.RadarDataLibrary.RadarData.RadarFileNotFoundException
# 
# Created by: yvow
# Created on: 01.05.2015

# Imports

class RadarFileNotFoundException(Exception):
    '''
    classdocs
    '''
    #TODO: Include class description.


    def __init__(self, value):
        '''
        Constructor
        '''
        #TODO: Include constructor description.
        self.value = value

    def __str__(self):
        return "The file " + repr(self.value) + " was not found!"
