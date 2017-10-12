# Copyright ETH-VAW / Glaciology
#
# Module      : Scripts.RadarDataLibrary.RadarData.RadarDataWriter
# 
# Created by: yvow
# Created on: 04.05.2015

# Imports
import abc

class RadarDataWriter(object):
    __metaclass__ = abc.ABCMeta
    '''
    classdocs
    '''
    #TODO: Include class description.
    
    _radarLine = None
    
    @property
    def radarLine(self):
        return self._radarLine
        
    @radarLine.getter
    def radarLine(self):
        return self._radarLine

    def __init__(self, radarLine):
        '''
        Constructor
        '''
        #TODO: Include constructor description.
        
        self._radarLine = radarLine
        
    @abc.abstractmethod
    def writeData(self):
        return

