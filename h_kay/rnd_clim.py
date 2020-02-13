#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 09:24:01 2020

@author: heatherkay
"""

import glob
import os
import geopandas as gpd
import numpy as np


def rnd_clim(folderin, folderout, roundto, column='b1', dec=0):
    """
    Function to round values in one column of shapefile
    
    folderin: string
            Filepath for folder containing shapefiles
            
    folderin: string
            Filepath for folder for new shapefiles

    roundto: integer
           value to round to nearest...
           
    column: string
          column title to round. Default = 'b1'

    dec: integer
            number of decimal points to retain. Default = 0            
    """
    fileList = glob.glob(folderin + '*_eco_*.shp')
    print(fileList)
    for filename in fileList:
        basename = os.path.splitext(os.path.basename(filename))[0]
        df = gpd.read_file(filename) 
        clim1 = df[column].astype(float)
        clim = np.around(clim1/roundto, decimals=dec)
        df2 = df.assign(clim=clim)
        df2.to_file(folderout + '{}.shp'.format(basename))

        