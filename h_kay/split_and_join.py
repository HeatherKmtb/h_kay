	#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 15:46:03 2020

@author: heatherkay
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 15:52:58 2019

@author: heatherkay
"""
import pandas as pd
import numpy as np
from pandas import DataFrame
import glob
import os.path
import geopandas as gpd
from multiprocessing import Pool
import rsgislib.vectorutils
import math
from joblib import Parallel, delayed


def split_per(folderin, folderout, split_col='ECO_ID', colNms=['i_h100','i_cd',
    'doy','i_wflen','i_acqdate','b1','vcf','ECO_NAME','ECO_ID','BIOME','geometry']):
    """
    Function which will divide shapefiles by individual elements in one column to generate new shapefiles 
    with filename referring to element in column (e.g split data by ecoregion and give each new file ecoregion number)
    
    Parameters
    ----------
    folderin: string
          filepath for folder containing shapefiles
          
    folderout: string
             filepath for folder where new files will be saved
             
    split_col: string
             name of column in files to use for split
             
    colNms: list of strings
          names of columns to be retained in output shapefile.
          Default = ['i_h100','i_cd','doy','i_wflen','i_acqdate','b1','vcf','ECO_NAME','ECO_ID','BIOME','geometry']                
    """

    split_files = glob.glob(folderin + '*.shp')

    for filename in split_files:
        print(filename)
        basename = os.path.splitext(os.path.basename(filename))[0]
        dfa = gpd.read_file(filename)
        df = dfa.astype({split_col: 'int32'})
        ecoNames = list(np.unique(df[split_col]))#get list of unique ecoregions    
        
        for eco in ecoNames:
            #create new df with just columns I want
            df2 = gpd.GeoDataFrame(df, columns=colNms)
            ID = str(eco)
            df_eco = df.loc[df2[split_col]==eco, colNms]
            df_eco.to_file(folderout + '/{}_eco_{}.shp'.format(basename, ID))    



def join_per(folderin, folderout, IDfile='./eco/final_ID.csv', column='ECO_ID'):
    """
    Function to regroup files that have been split with spilt_per function on elements of split
    
    Parameters
    ----------
    folderin: string
            filepath for folder containing shapefiles to be joined
            
    folderout: string
             filepath for folder where output shapefiles will be saved 
             
    IDfile: string
          filepath for csv with column containing list of elements for the join.
          Default = './eco/final_ID.csv'
          
    column: string
          column name from IDfile containing elements for the join.   
          Default = 'ECO_ID'
    """
    #import csv with IDs to obtain list for merge
    df = pd.read_csv(IDfile)
    ecoNms = list(np.unique(df[column]))#get list of unique ecoregions     

    for ecoNm in ecoNms:
        fileList = glob.glob(folderin + '*_eco_{}.shp'.format(ecoNm))#here also need dict ref
        rsgislib.vectorutils.mergeShapefiles(fileList, folderout + 'gla14_eco_{}.shp'.format(ecoNm))#use dict to get ecoNm, create new folder too?
 
    #mkdir is make new folder

def rmv_cat(folderin, folderout, column='b1', cat=['0.0', '190.0','200.0','202.0', '210.0', '220.0']):
    """
    Function to remove categories e.g. land cover classifications, vcf categories, ecoregions
    
    Parameters
    ----------
    folderin: string
            filepath for folder containing shapefiles to be processed
    
    folderout: string
             filepath for folder where output shapefiles will be saved
             
    column: string
          column from shapefile with categories for removal.
          Default = 'b1'
          
    cat: list of strings
       names of categories to be dropped      
    """
    fileList = glob.glob(folderin + '*_eco_*.shp')

    for filename in fileList:
        basename = os.path.splitext(os.path.basename(filename))[0]
        df = gpd.read_file(filename) 
        new = df[np.logical_not(df[column].isin(cat))]
        if new.empty:
            continue
        new.to_file(folderout + '{}.shp'.format(basename))
             

def join_per_grid_parallel(folderin, folderout, naming='*_eco_*_eco_{}.shp',rngmn = 0, rngmx = 56001, cores=50):
    """
    Function to regroup files that have been split with spilt_per function on 
    grid numbers using a range 
    
    Parameters
    ----------
    folderin: string
            filepath for folder containing shapefiles to be joined
            
    folderout: string
             filepath for folder where output shapefiles will be saved 
      
    naming: string
            file name with {} for section included in range
            default = '*_eco_*_eco_{}.shp'
    rngmn: int
            minimum range value for grid square numbers 
            Default = 0
            
    rngmx: int
            maximum range value for grid square numbers
            Default = 56001 (equivalent to 1 degree grid)
            
    cores: int
            number of cores to be used in parallel
            Default = 50
    """
 
    rge = np.arange(rngmn, rngmx,1)
    
    def merge(i, folderin, folderout):
        fileList = glob.glob(folderin + naming.format(i))
        if len(fileList)==0:
            print(i)
        else: 
            rsgislib.vectorutils.mergeShapefiles(fileList, folderout + 'gla14_grid_{}.shp'.format(i))
    
    Parallel(n_jobs=cores)(delayed(merge)(i, folderin, folderout) for i in rge)
    