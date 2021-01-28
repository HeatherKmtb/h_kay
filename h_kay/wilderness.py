#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 09:00:13 2021

@author: heatherkay
"""

import geopandas as gpd
import glob
from os import path


def sort_wilderness_shps(folderin, folderout):
    """
    Function to extract IUCN categories Ia, Ib and II from wilderness shape files

    Parameters
    ----------
    folderin : String
        Filepath for folder with files ready for analysis
        
    folderout : String
        Filepath for folder to write new files

    Returns
    -------
    None.

    """

    filelist = glob.glob(folderin + '*.shp')
    
    for file in filelist:
        hd, tl = path.split(file)
        name = tl.replace('WDPA_WDOECM_wdpa_shp', "")
        name2 = name.replace('.shp', "")
        df = gpd.read_file(file)
        dfIa = df[df['IUCN_CAT']=='Ia']
        dfIb = df[df['IUCN_CAT']=='Ib']
        dfII = df[df['IUCN_CAT']=='II']
        dfI = dfIa.append(dfIb, sort=True)
        dfall = dfI.append(dfII, sort=True)
        dfall.tofile(folderout + name2 + '.shp')
        
        
        
        