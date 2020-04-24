#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 16:43:23 2020

@author: heatherkay
"""


import rsgislib.vectorutils
from joblib import Parallel, delayed

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
    