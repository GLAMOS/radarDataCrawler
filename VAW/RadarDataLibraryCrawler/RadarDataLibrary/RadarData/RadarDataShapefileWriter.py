# Copyright ETH-VAW / Glaciology
#
# Module      : Scripts.RadarDataLibrary.RadarData.DataDataShapefileWriter
# 
# Created by: yvow
# Created on: 04.05.2015

# Imports
import os
import re
import abc

from RadarDataWriter import RadarDataWriter

class RadarDataShapefileWriter(RadarDataWriter):
    __metaclass__ = abc.ABCMeta
    '''
    classdocs
    '''
    #TODO: Include class description.
    
    _shapeFileLine  = ""
    _shapeFilePoint = ""
    
    
    # Field names for lines and points
    _FIELD_NAME_PROFILE_ID            = "PROFILE"
    _FIELD_NAME_DATE                  = "DATE_ACQ"    
    
    # Field names for lines
    _FIELD_NAME_LINE_ACQUISITION_TYPE = "ACQ_TYPE"
    _FIELD_NAME_LINE_INSTRUMENT       = "INSTRUMENT"
    _FIELD_NAME_LINE_FREQUENCY        = "FREQUENCY"
    _FIELD_NAME_LINE_SUMMARY          = "SUMMARY"
    _FIELD_NAME_LINE_IMAGE_BEDROCK    = "BED"
    _FIELD_NAME_LINE_IMAGE_MAP        = "MAP"
    _FIELD_NAME_LINE_IMAGE_MIG        = "MIG"
    
    # Field names for points
    _FIELD_NAME_COUNT_RESULTS         = "NUM_RES"
    _FIELD_NAME_POINT_Z_BEDROCK_1     = "Z_BED_1"
    _FIELD_NAME_POINT_Z_ICE_SUR_1     = "Z_ICE_1"
    _FIELD_NAME_POINT_THICKNESS_1     = "THICK_1"
    _FIELD_NAME_POINT_QUALITY_1       = "Q_1"
    _FIELD_NAME_POINT_Z_BEDROCK_2     = "Z_BED_2"
    _FIELD_NAME_POINT_Z_ICE_SUR_2     = "Z_ICE_2"
    _FIELD_NAME_POINT_THICKNESS_2     = "THICK_2"
    _FIELD_NAME_POINT_QUALITY_2       = "Q_2"


    def __init__(self, radarLine, shapeFileLine, shapeFilePoint, doAppend = True):
        '''
        Constructor
        '''
        #TODO: Include constructor description.
        
        super(RadarDataShapefileWriter, self).__init__(radarLine)
        
        self._shapeFileLine  = shapeFileLine
        self._shapeFilePoint = shapeFilePoint
        
        if doAppend == False:
            if os.path.exists(self._shapeFileLine):
                self._deleteShapefile(self._shapeFileLine)
            if os.path.exists(self._shapeFilePoint):
                self._deleteShapefile(self._shapeFilePoint)

        if doAppend == True and  os.path.exists(self._shapeFileLine) == False:
            pass
        if doAppend == True and  os.path.exists(self._shapeFilePoint) == False:
            pass
        
    def _deleteShapefile(self, shapefile):
            
        shapefileDirectory = os.path.dirname(shapefile)
        shapefileName = os.path.basename(shapefile)
        shapefileBasename = os.path.splitext(shapefileName)[0]
    
        for fileInDirectory in os.listdir(shapefileDirectory):
            if re.search(shapefileBasename, fileInDirectory):
                os.remove(os.path.join(shapefileDirectory, fileInDirectory))

    @abc.abstractmethod
    def writeData(self):
        return

# Imports used by EsriShapefileWriter
import arcpy
import arcpy.da
from arcpy import env
from arcpy.da import InsertCursor

class EsriShapefileWriter(RadarDataShapefileWriter):
    '''
    classdocs
    '''
    #TODO: Include class description.
    
    __SHAPE_GEOMETRY_TYPE_POLYLINE = "POLYLINE"
    __SHAPE_GEOMETRY_TYPE_POINT = "POINT"
    
    __spatialReferenceString = "CH1903 LV03"
    __spatialReference = None
    
    def __init__(self, radarLine, shapeFileLine, shapeFilePoint, doAppend = True):
        '''
        Constructor
        '''
        #TODO: Include constructor description.
        
        super(EsriShapefileWriter, self).__init__(radarLine, shapeFileLine, shapeFilePoint, doAppend)
        
        self.__spatialReference = arcpy.SpatialReference(self.__spatialReferenceString)
        
        if doAppend == False:
            self.__prepareFeatureClass(self._shapeFileLine, self.__SHAPE_GEOMETRY_TYPE_POLYLINE)
            self.__createAttributesLine()
            self.__prepareFeatureClass(self._shapeFilePoint, self.__SHAPE_GEOMETRY_TYPE_POINT)
            self.__createAttributesPoint()
        
    
    def __prepareFeatureClass(self, shapefile, shapefileType):
        
        shapeDirectory = os.path.dirname(shapefile)
        env.workspace = shapeDirectory
        
        shapefileName = os.path.basename(shapefile)
        
        arcpy.CreateFeatureclass_management(shapeDirectory, shapefileName, shapefileType, "", "", "", self.__spatialReference)
    
        
    def __createAttributesLine(self):
        
        #TODO: Getting one general function to create attributes for lines and points.
        
        env.workspace = os.path.dirname(self._shapeFileLine)
        shapefileName = os.path.basename(self._shapeFileLine)
               
        # Adding the needed fields
        arcpy.AddField_management(shapefileName, self._FIELD_NAME_PROFILE_ID           ,   "TEXT", "", "",  20,  "", "NULLABLE", "")
        arcpy.AddField_management(shapefileName, self._FIELD_NAME_DATE                 ,   "DATE", "", "",  "",  "", "NULLABLE", "")
        # ---
        arcpy.AddField_management(shapefileName, self._FIELD_NAME_LINE_ACQUISITION_TYPE,   "TEXT", "", "",  50,  "", "NULLABLE", "")
        arcpy.AddField_management(shapefileName, self._FIELD_NAME_LINE_INSTRUMENT      ,   "TEXT", "", "",  50,  "", "NULLABLE", "")
        arcpy.AddField_management(shapefileName, self._FIELD_NAME_LINE_FREQUENCY       , "DOUBLE", "", "", "", "", "NULLABLE", "")

        # Fields with file information
        arcpy.AddField_management(shapefileName, self._FIELD_NAME_LINE_SUMMARY      ,  "TEXT", "", "", 500,  "", "NULLABLE", "")
        arcpy.AddField_management(shapefileName, self._FIELD_NAME_LINE_IMAGE_BEDROCK,  "TEXT", "", "", 500,  "", "NULLABLE", "")
        arcpy.AddField_management(shapefileName, self._FIELD_NAME_LINE_IMAGE_MAP    ,  "TEXT", "", "",  "", 500, "NULLABLE", "")
        arcpy.AddField_management(shapefileName, self._FIELD_NAME_LINE_IMAGE_MIG    ,  "TEXT", "", "",  "", 500, "NULLABLE", "")
    
        # Removing the default Id field
        arcpy.DeleteField_management(shapefileName, ["Id"])
        
    def __createAttributesPoint(self):
        
        #TODO: Getting one general function to create attributes for lines and points.
        
        env.workspace = os.path.dirname(self._shapeFilePoint)
        shapefileName = os.path.basename(self._shapeFilePoint)
               
        # Adding the needed fields: General information
        arcpy.AddField_management(shapefileName, self._FIELD_NAME_PROFILE_ID      ,    "TEXT", "", "",  20,  "", "NULLABLE", "")
        arcpy.AddField_management(shapefileName, self._FIELD_NAME_DATE            ,    "DATE", "", "",  "",  "", "NULLABLE", "")
        arcpy.AddField_management(shapefileName, self._FIELD_NAME_COUNT_RESULTS     , "SHORT", "", "",  "",  "", "NULLABLE", "")
        # Adding the needed fields: Analyzed information
        arcpy.AddField_management(shapefileName, self._FIELD_NAME_POINT_Z_BEDROCK_1, "DOUBLE", "", "", "", "", "NULLABLE", "")
        arcpy.AddField_management(shapefileName, self._FIELD_NAME_POINT_Z_ICE_SUR_1, "DOUBLE", "", "", "", "", "NULLABLE", "")
        arcpy.AddField_management(shapefileName, self._FIELD_NAME_POINT_THICKNESS_1, "DOUBLE", "", "", "", "", "NULLABLE", "")
        arcpy.AddField_management(shapefileName, self._FIELD_NAME_POINT_QUALITY_1  ,  "SHORT", "", "", "", "", "NULLABLE", "")
        # ------------
        arcpy.AddField_management(shapefileName, self._FIELD_NAME_POINT_Z_BEDROCK_2, "DOUBLE", "", "", "", "", "NULLABLE", "")
        arcpy.AddField_management(shapefileName, self._FIELD_NAME_POINT_Z_ICE_SUR_2, "DOUBLE", "", "", "", "", "NULLABLE", "")
        arcpy.AddField_management(shapefileName, self._FIELD_NAME_POINT_THICKNESS_2, "DOUBLE", "", "", "", "", "NULLABLE", "")
        arcpy.AddField_management(shapefileName, self._FIELD_NAME_POINT_QUALITY_2  ,  "SHORT", "", "", "", "", "NULLABLE", "")
    
        # Removing the default Id field
        arcpy.DeleteField_management(shapefileName, ["Id"])
    
    def writeData(self):
        self.__writeLines()
        self.__writePoints()
    
    def __writeLines(self):
        
        array = arcpy.Array()
        
        cursor = InsertCursor(self._shapeFileLine, [ \
                 "SHAPE@", \
                 self._FIELD_NAME_LINE_ACQUISITION_TYPE, self._FIELD_NAME_LINE_INSTRUMENT, self._FIELD_NAME_LINE_FREQUENCY, \
                 self._FIELD_NAME_PROFILE_ID, self._FIELD_NAME_DATE, self._FIELD_NAME_LINE_SUMMARY, \
                 self._FIELD_NAME_LINE_IMAGE_BEDROCK, self._FIELD_NAME_LINE_IMAGE_MAP, self._FIELD_NAME_LINE_IMAGE_MIG, \
                 ])

        for radarPoint in self._radarLine.radarPoints:        
            array.add(arcpy.Point(radarPoint.xCoordinate, radarPoint.yCoordinate))
            
        lineGeometry = arcpy.Polyline(array)
        
        cursor.insertRow([ \
        lineGeometry, \
        self._radarLine.acquisitionType, self._radarLine.instrument, self._radarLine.frequency, \
        self._radarLine.lineId, self._radarLine.date, self._radarLine.summaryFile, \
        self._radarLine.bedrockImageFile, self._radarLine.mapImageFile, self._radarLine.migImageFile, \
        ])
        
        del(cursor)
            
    
    def __writePoints(self):
        
        cursor = InsertCursor(self._shapeFilePoint, [ \
        "SHAPE@", \
        self._FIELD_NAME_PROFILE_ID, self._FIELD_NAME_DATE, self._FIELD_NAME_COUNT_RESULTS, \
        self._FIELD_NAME_POINT_Z_BEDROCK_1, self._FIELD_NAME_POINT_Z_ICE_SUR_1, self._FIELD_NAME_POINT_THICKNESS_1, self._FIELD_NAME_POINT_QUALITY_1, \
        self._FIELD_NAME_POINT_Z_BEDROCK_2, self._FIELD_NAME_POINT_Z_ICE_SUR_2, self._FIELD_NAME_POINT_THICKNESS_2, self._FIELD_NAME_POINT_QUALITY_2 \
        ])

        for radarPoint in self._radarLine.radarPoints:
            
            pointGeometry = arcpy.Point(radarPoint.xCoordinate, radarPoint.yCoordinate)
            
            zBed_1      = 0.0
            zIce_1      = 0.0
            thickness_1 = 0.0
            quality_1   = 0.0
            zBed_2      = 0.0
            zIce_2      = 0.0
            thickness_2 = 0.0
            quality_2   = 0.0
            
            if radarPoint.countResults > 0:
                zBed_1      = radarPoint.results[0].zBed
                zIce_1      = radarPoint.results[0].zIce
                thickness_1 = radarPoint.results[0].thickness
                quality_1   = radarPoint.results[0].quality
                
            if radarPoint.countResults >= 2:
                zBed_2      = radarPoint.results[1].zBed
                zIce_2      = radarPoint.results[1].zIce
                thickness_2 = radarPoint.results[1].thickness
                quality_2   = radarPoint.results[1].quality
            
            cursor.insertRow([ \
            pointGeometry, \
            self._radarLine.lineId, self._radarLine.date, radarPoint.countResults, \
            zBed_1, zIce_1, thickness_1, quality_1, \
            zBed_2, zIce_2, thickness_2, quality_2 \
            ])
            
        del(cursor)