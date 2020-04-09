#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 16:39:32 2020

@author: heatherkay
"""

import rsgislib.vectorutils
import math
import glob
import os.path
from multiprocessing import Pool

def shp_join(filein, folderout, folderno):
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
        import geopandas
        # Must have rtree installed - otherwise error "geopandas/tools/sjoin.py"
        # AttributeError: 'NoneType' object has no attribute 'intersection'
        base_gpd_df = geopandas.read_file(base_vec)
        join_gpg_df = geopandas.read_file(join_vec)
    
        join_gpg_df = geopandas.sjoin(base_gpd_df, join_gpg_df, how="inner", op="within")
        join_gpg_df.to_file(output_vec)

    def run_join(params):
        base_vec = params[0]
        join_vec = params[1]
        output_vec = params[2]
        performSpatialJoin(base_vec, '', join_vec, '', output_vec, '')
    
    nFeatures = rsgislib.vectorutils.getVecFeatCount('gla14/orig_gla_data/gla14.shp', 'gla14', computeCount=True)
    print(nFeatures)

    nfiles = 1000
    nfeat_split = math.ceil(nFeatures/nfiles)
    print("{} files outputted with {} features each/".format(nfiles, nfeat_split))

    rsgislib.vectorutils.splitVecLyr('gla14/orig_gla_data/gla14.shp', 'gla14', nfeat_split, 'ESRI Shapefile', './gla14/split_files', 'gla14_file', '.shp')


    split_files = glob.glob('./gla14/split_files/folder_{}/*.shp'.format(folderno))


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



