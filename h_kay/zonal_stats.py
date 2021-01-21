#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 10:25:49 2021

@author: heatherkay
"""

import geopandas
from rasterstats import zonal_stats
import glob
import os.path

#gedi = '/Users/heatherkay/q_res/test/GEDI02_B_2019275183438_O04563_T02081_02_001_01_1.gpkg'
#vector = geopandas.read_file(gedi, layer='BEAM0000')
#raster = '/Users/heatherkay/q_res/layers/ESACCI-LC-L4-LCCS-Map-300m-P5Y-2010-v1.6.1.tif'
#stats = 'median'
#gedi = '/scratch/a.hek4/test/GEDI02_B_2019275183438_O04563_T02081_02_001_01_1.gpkg'
#vector = geopandas.read_file(gedi, layer='BEAM0000')
#raster = '/scratch/a.hek4/ESACCI-LC-L4-LCCS-Map-300m-P5Y-2010-v1.6.1.tif'

# For calculating zonal statistics
def get_zonal_stats(folderin, raster, fileout, stats):
    beams = ['BEAM0000','BEAM0001','BEAM0010','BEAM0011','BEAM0101','BEAM0110',
             'BEAM1000','BEAM1011']
    
    filelist = glob.glob(folderin + '*.gpkg')
    
    for vectorfile in filelist:
        name = os.path.splitext(os.path.basename(vectorfile))[0]
        for beam in beams:
            vector = geopandas.read_file(vectorfile, layer=beam)
            result = zonal_stats(vector, raster, stats=stats, geojson_out=True)
            geostats = geopandas.GeoDataFrame.from_features(result)
    
            geostats.to_file(fileout + name + ".gpkg", layer = beam, driver='GPKG')


def get_zonal_stats_shp(folderin, raster, fileout, stats):
    
    filelist = glob.glob(folderin + '*.shp')
    
    for vectorfile in filelist:
        name = os.path.splitext(os.path.basename(vectorfile))[0]

        vector = geopandas.read_file(vectorfile)
        result = zonal_stats(vector, raster, stats=stats, geojson_out=True)
        geostats = geopandas.GeoDataFrame.from_features(result)
        geostats.to_file(fileout + name + ".shp")
