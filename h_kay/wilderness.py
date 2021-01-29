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
             
    folderno: string
            Number - needs to be changed from 1 to 10 and run due to file quantity and size         
    """
    def performSpatialJoin(base_vec, base_lyr, join_vec, join_lyr, output_vec, output_lyr):
        # Must have rtree installed - otherwise error "geopandas/tools/sjoin.py"
        # AttributeError: 'NoneType' object has no attribute 'intersection'
        base_gpd_df = gpd.read_file(base_vec)
        join_gpg_df = gpd.read_file(join_vec)
    
        join_gpg_df = gpd.sjoin(base_gpd_df, join_gpg_df, how="inner", op="within")
        join_gpg_df.to_file(output_vec)


    def run_join(params):
        base_vec = params[0]
        join_vec = params[1]
        output_vec = params[2]
        performSpatialJoin(base_vec, '', join_vec, '', output_vec, '')
    
    split_files = glob.glob(folderin + '*.shp')

    params = []
    for filename in split_files:
        basename = os.path.splitext(os.path.basename(filename))[0]
        output_file = os.path.join(folderout, "{}_join.shp".format(basename))
        params.append([filename, filein, output_file])

    ncores = 50
    p = Pool(ncores)
    p.map(run_join, params)

    #joined_files = glob.glob('./intersect_koppen_split/*.shp')
    #rsgislib.vectorutils.mergeShapefiles(joined_files, './gla14/gla14_koppen.shp')        
        