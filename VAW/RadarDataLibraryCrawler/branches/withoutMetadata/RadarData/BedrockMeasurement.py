# Copyright ETH-VAW / Glaciology
#
# Module      : Scripts.RadarDataLibrary.RadarData.BedrockMeasurement
# 
# Created by: yvow
# Created on: 01.05.2015

# Imports
from RadarPoint import RadarPoint

class BedrockMeasurement(RadarPoint):
    '''
    classdocs
    '''
    #TODO: Include class description.
       
    __result = None
    
    @property
    def countResults(self):
        return len(self.__result)
        
    @countResults.getter
    def countResults(self):
        return len(self.__result)
    
    @property
    def results(self):
        return self.__result
        
    @results.getter
    def results(self):
        return self.__result

    def __init__(self, xCoord, yCoord):
        '''
        Constructor
        '''
        #TODO: Include constructor description.
        
        super(BedrockMeasurement, self).__init__(xCoord, yCoord)
        
        # Initializing the list of the results as empty containers.
        self.__result = list()
        
    def __str__(self):
        message = super(BedrockMeasurement, self).__str__()
        message = message + ", Number of results: " + str(self.countResults)
        
        return message
    
    def addResult(self, bedrockMeasurementResult):
        self.__result.append(bedrockMeasurementResult)
        

class BedrockMeasurementResult(object):
    '''
    classdocs
    '''
    #TODO: Include class description.
    
    # Measured values.
    __zBed = None
    __zIce = None
    __thickness = None
    __quality = None
    
    @property
    def zBed(self):
        return self.__zBed
        
    @zBed.getter
    def zBed(self):
        return self.__zBed
    
    @property
    def zIceSurface(self):
        return self.__zIceSurface
        
    @zIceSurface.getter
    def zIceSurface(self):
        return self.__zIceSurface
    
    @property
    def thickness(self):
        return self.__thickness
        
    @thickness.getter
    def thickness(self):
        return self.__thickness  
    
    @property
    def quality(self):
        return self.__quality
        
    @quality.getter
    def quality(self):
        return self.__quality     
    
    def __init__(self, zIceSurface, zBed, thickness, quality):
        '''
        Constructor
        '''
        #TODO: Include constructor description.
        
        #TODO: Getting a better solution for the differences between old and new file formats.
                            
        # Determination what kind of file format is used:
        # Old files: Bed IceSurface Thickness Quality
        # New files: IceSurface Bed Thickness Quality
        # General rule: zIceSurface > zBed

        # In case of correct parameters
        if zIceSurface > zBed:
            self.__zBed        = zBed
            self.__zIceSurface = zIceSurface
        # In case of swapped parameters
        else:
            self.__zBed        = zIceSurface
            self.__zIceSurface = zBed
        
        self.__thickness = thickness
        #TODO: What to do, if the given thickness is different of self.__zIce - self.__zBed?
        
        self.__quality   = quality
        
    def __str__(self):
        message = "Bedrock: " + str(self.__zBed) + ", Ice surface: " + str(self.__zIceSurface) + ", Thickness: " + str(self.__thickness) + ", Quality: " + str(self.__quality)
        return message