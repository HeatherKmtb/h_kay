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

        new_long = math.floor(lon)
        new_lati = math.ceil(lat)
      
        if new_long <0:
             pos1 = abs(new_long)
             pos = str(pos1)
             if len(pos) == 1:
                 posit = '00' + pos
             elif len(pos) == 2:
                 posit = '0' + pos 
             else:
                 posit = pos
             name_lon = 'W' + posit
             
        else:
            new_lon = str(new_long)
            if len(new_lon) == 1:
                long = '00' + new_lon
            elif len(new_lon) == 2:
                long = '0' + new_lon 
            else: 
                long = new_long
            name_lon = 'E' + str(long)
    
        if new_lati <0:
            po1 = abs(new_lati)
            po = str(po1)
            if len(po) == 1:
                posi = '0' + po   
            else:
                posi = po
            name_lat = 'S' + str(posi)
        else:
            new_lat = str(new_lati)
            if len(new_lat) == 1:
                 lati = '0' + new_lat 
            else:
                lati = new_lat
            name_lat = 'N' + str(lati)
            
        naming = name_lat + name_lon   
        
        df.to_file(folderout + 'gla14_grid_{}.shp'.format(naming))

