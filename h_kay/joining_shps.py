#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 16:39:32 2020

@author: heatherkay
"""

import glob
import os
from multiprocessing import Pool
import geopandas as gpd
from joblib import Parallel, delayed
from functools import reduce


def gla14_join(filein, folderout, folderno):
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


def ez_join(filein, folderout, folderin):
    """
    Function to join a shapefile to another shape file (within).
    
    Parameters
    ----------
    filein: string
          Filepath for shp file to join with other shape files (folderin)
          
    folderout: string
             Filepath for folder to contain joined files
             
    folderin: string
            Filepath for shp files to join with other shape file (filein)        
    """
    files = glob.glob(folderin + '*.shp')
    for file in files:

        filename = os.path.splitext(os.path.basename(file))[0]
        base_gpd_df = gpd.read_file(file)
        join_gpg_df = gpd.read_file(filein)
        print(file)
        print(filein)
        if base_gpd_df.empty:
            continue
        join_gpg_df = gpd.sjoin(base_gpd_df, join_gpg_df, how="inner", op="within")
        if join_gpg_df.empty:
            print('empty' + file)
            continue
        other_filename = os.path.splitext(os.path.basename(filein))[0]
        oot = os.path.join(folderout, "{}_{}_join.shp".format(filename, other_filename))
        print(oot)
        join_gpg_df.to_file(oot)
        
def ez_join_2_folders(folderin1, folderout, folderin):
    """
    Function to join a folder of shapefiles to another folder of shapefiles (within).
    
    Parameters
    ----------
    folderin1: string
        Filepath for shp files to join with other shape files (filein2) 

    folderin: string
        Filepath for shp files to join with other shape files (filein1) 
        
    folderout: string
        Filepath for folder to contain joined files
    """    
    
    file_list = glob.glob(folderin1 + '*.shp')
     
    Parallel(n_jobs=50)(delayed(ez_join)(i, folderout, folderin) for i in file_list)   

def ez_join_parallel(filein, folderout, folderin):
    """
    Function to join a shapefile to another shape file (within) in parallel, 50 cores.
    
    Parameters
    ----------
    filein: string
          Filepath for shp file to join with other shape files (folderin)
          
    folderout: string
             Filepath for folder to contain joined files
             
    folderin: string
            Filepath for shp files to join with other shape file (filein)        
    """
    
    files = glob.glob(folderin + '*.shp')
    
    def join(i, filein, folderout):
        filename = os.path.splitext(os.path.basename(i))[0]
        base_gpd_df = gpd.read_file(i)
        join_gpg_df = gpd.read_file(filein)
        print(i)
        if base_gpd_df.empty:
            print('empty in' + i)
        else:
            join_gpg_df = gpd.sjoin(base_gpd_df, join_gpg_df, how="inner", op="within") 
            if join_gpg_df.empty:
                print('empty out' + i)
            else:
                other_filename = os.path.splitext(os.path.basename(filein))[0]
                oot = os.path.join(folderout, "{}_{}_join.shp".format(filename, other_filename))
                print(oot)
                join_gpg_df.to_file(oot)  
        
    Parallel(n_jobs=50)(delayed(join)(i, filein, folderout)for i in files)
    
def another_bleddy_join(folderin, folderout, col_nm='id'):
    """
    Function to join a shapefiles together based on a column.
    
    Parameters
    ----------          
    folderin: string
             Filepath for shp files to join based on column
             
    folderin: string
             Filepath for folder to contain joined files 
             
    col_nm: string
             Name of column for join         
    """        

    fileList=glob.glob(folderin + '*.shp')

    for file in fileList:
        df = gpd.read_file(file)
        basename = os.path.splitext(os.path.basename(file))[0]
        id_name = df[col_nm][0]
        oot = os.path.join(folderout, "{}_{}.shp".format(basename, id_name))
        df.to_file(oot)    
        
def union(folderin, fileout):
    """
    Function to join a shapefile to another shape file (within).
    
    Parameters
    ----------
    folderin: string
          Filepath for shp files to be joined
          
    fileout: string
             Filepath joined files shapefile
      
    """
    
    fileList = glob.glob(folderin + '*.shp')
    
    dfList = [gpd.read_file(d) for d in fileList]
    
    final_shp = reduce(lambda left,right: gpd.overlay(left,right,how='union'), dfList)

    final_shp.to_file = fileout