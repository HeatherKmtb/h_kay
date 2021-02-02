#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 09:00:13 2021

@author: heatherkay
"""

import geopandas as gpd
import glob
import os
from multiprocessing import Pool
import geopandas as gpd
from joblib import Parallel, delayed
from functools import reduce


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
        
        



def gla14_join(filein, folderout, folderin):
    """
    Function to join a shapefile to the gla14 data. Must be run for folderno from 1-10
    
    Parameters
    ----------
    filein: string
          Filepath for shp file to join with gla14 data
          
    folderout: string
             Filepath for folder to contain joined files
             
    folderin: string
            Filepath for folder contaning gla14 files        
    """

    split_files = glob.glob(folderin + '*.shp')

    join_gpg_df = gpd.read_file(filein)

    for filename in split_files:
        basename = os.path.splitext(os.path.basename(filename))[0]
        base_gpd_df = gpd.read_file(filename)
        base_gpd_df = base_gpd_df.set_geometry(col='geometry', crs="ESPG:4326")
        join_gpg_df = gpd.sjoin(base_gpd_df, join_gpg_df, how="inner", op="within")
        if join_gpg_df.empty:
            continue
        join_gpg_df.to_file(folderout, "{}_join.shp".format(basename))
        



    #joined_files = glob.glob('./intersect_koppen_split/*.shp')
    #rsgislib.vectorutils.mergeShapefiles(joined_files, './gla14/gla14_koppen.shp')        
        