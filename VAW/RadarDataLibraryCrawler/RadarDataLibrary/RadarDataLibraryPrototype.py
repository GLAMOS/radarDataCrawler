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

# -------------- User input --------------
headerDirectory = r"\\itetnas01.ee.ethz.ch\glazioarch\_INCOMING\20090331_Aletsch\L1"
dataDirectory   = r"\\itetnas01.ee.ethz.ch\glazioarch\_INCOMING\20090331_Aletsch\L2"
shapeDirectory  = r"D:\GIS\GlaciologyDatabase\MiscellaneousScripts\Scripts\RadarDataLibrary\Shapefiles"
shapeFileNameLine  = "RadarArchive_L2_Lines_lv03.shp"
shapeFileNamePoint = "RadarArchive_L2_Points_lv03.shp"
# ----------------------------------------

radarDataLibraryCrawler = RadarDataLibraryCrawler(headerDirectory, dataDirectory, shapeDirectory, shapeFileNameLine, shapeFileNamePoint)

radarDataLibraryCrawler.writeGeometries()