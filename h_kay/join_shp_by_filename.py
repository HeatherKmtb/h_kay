#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 09:20:27 2021

@author: heatherkay
"""

import numpy as np
import rsgislib.vectorutils
import glob

def join_shps(folderin, folderout):
    """
    joins all data from shape files in list based on item in filename
    
    
    """
    grid = np.arange(0, 1001, 1 )
    for i in grid:
        fileList = glob.glob(folderin + 'gla14_file' + grid + '_join*.*')
        rsgislib.vectorutils.mergeShapefiles(fileList, folderout + 'gla14_grid_{}.shp'.format(grid))
