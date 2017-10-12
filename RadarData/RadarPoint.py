# Copyright ETH-VAW / Glaciology
#
# Module      : Scripts.RadarDataLibrary.RadarData.RadarPoint
# 
# Created by: yvow
# Created on: 29.04.2015

# Imports

class RadarPoint(object):
    '''
    classdocs
    '''
    #TODO: Include class description.
    _xCoord = None
    _yCoord = None
        
    @property
    def xCoordinate(self):
        return self._xCoord
        
    @xCoordinate.getter
    def xCoordinate(self):
        return self._xCoord
    
    @property
    def yCoordinate(self):
        return self._yCoord
        
    @yCoordinate.getter
    def yCoordinate(self):
        return self._yCoord    

    def __init__(self, xCoord, yCoord):
        '''
        Constructor
        '''
        #TODO: Include constructor description.
        
        # 
        # Getting the location of the radar measurement initialized.
        self._xCoord = xCoord
        self._yCoord = yCoord

    def __str__(self):
        message = "xCoord: " + str(self._xCoord) + ", yCoord: " + str(self._yCoord)
        return message