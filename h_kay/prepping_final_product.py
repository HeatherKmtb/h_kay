#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 11 11:19:19 2020

@author: heatherkay
"""

import geopandas as gpd


#write the functions that do difference in order to obtain the shapefiles with no overlaps
base = 
        
def concat_shps(base, join, out, col_nms=()):
    """
    Function to join shapefiles with same columns and NO SPATIAL OVERLAP. 
    It is essential that the shapefiles have the same naming of the columns 
    to be kept.
    
    Parameters
    ----------          
    base: string
             Filepath for first shp file to join 
             
    join: string
             Filepath for second shp file to join 
             
    out: string
             Filepath for resulting shp file     
    """     
    