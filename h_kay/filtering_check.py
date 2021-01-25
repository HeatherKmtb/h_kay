#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 09:59:32 2021

@author: heatherkay
"""

import geopandas as gpd
import glob
from os import path
import pandas as pd



def get_stats(orig_folder, lc_folder, vcf_folder, both_folder, fileoot, 
              naming='/Users/heatherkay/q_res/filtering/'):
    folderlist = [orig_folder, lc_folder, vcf_folder, both_folder]
    results = pd.DataFrame(columns = ['grid','file','footprints'])

    for folder in folderlist: 
        hd, tl = path.split(folder)
        name1 = hd.replace(naming, "")
        
        fileList = glob.glob(folder + '*.shp')
        print(name1)
    
        for filename in fileList:
            hd, tl = path.split(filename)
            name2 = tl.replace("gla14_grid_", "")
            grid = name2.replace('.shp', "")
            df = gpd.read_file(filename) 
            footprints = len(df['i_h100'])
            print(grid)
            results = results.append({'grid':grid, 'file':name1, 'footprints':footprints}, ignore_index=True)
            results.to_csv(fileoot)
            

        