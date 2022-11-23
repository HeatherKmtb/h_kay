#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 12:34:05 2022

@author: heather
"""

import geopandas as gpd
import math
import glob

def grid_naming(folderin, folderout):
    
    """
    Function to convert the file naming from numbered grid to JAXA 
    top left corner system

    Parameters
    ----------

    folderin: string
        Filepath for folder with files ready for conversion
            
    folderout: string
         Filepath for folder to save the new files            
    """
    file_list = glob.glob(folderin + '*.shp')

    for file in file_list:
        df = gpd.read_file(file)

        lon = df.geometry[0].x
        lat = df.geometry[0].y

        new_lon = math.floor(lon)
        new_lat = math.ceil(lat)

        if new_lon <0:
             posit = abs(new_lon)
             name_lon = 'W' + str(posit)
        else:
             name_lon = 'E' + str(new_lon)
    
        if new_lat <0:
            posi = abs(new_lat)
            name_lat = 'S' + str(posi)
        else:
            name_lat = 'N' + str(new_lat)

        naming = name_lat + name_lon   
        
        df.to_file(folderout + 'gla14_grid_{}.shp'.format(naming))

