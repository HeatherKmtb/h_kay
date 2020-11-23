#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 13:19:32 2020

@author: heatherkay
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
from scipy.optimize import curve_fit
import geopandas as gpd
import glob
from os import path

def grid_only(folderin, fileout, naming=2):
    """
    Function to compute q and provide results (csv) and figures (pdf)
    
    Parameters
    ----------
    
    folderin: string
            Filepath for folder with files ready for analysis
                
    naming: int
          Section of filename to obtain ID (here grid number). Obtained
          by splitting filename by '_' and indexing
          Default = 3

    eco_loc: int
          Section of filename to obtain ecoregion (if applicable). 
          Obtained as with naming
          Default = 2
          
    fileout: string
           Filepath for results file ending '.csv'
           
    folderout: string
             Filepath for folder to save the figures            
    """

    #using 'file' to title plot  
    fileList = glob.glob(folderin + '*.shp')

    #create df for results
    resultsa = pd.DataFrame(columns = ['ID', 'deg_free'])
    #resultsb = pd.DataFrame(columns = ['eco', 'ID', 'qout', 'r_sq', 'deg_free', 'rmse'])

    for file in fileList:
        df = gpd.read_file(file)
        if df.empty:
            continue 
        hd, tl = path.split(file)
        shp_lyr_name = path.splitext(tl)[0]
        name_comp = shp_lyr_name.split('_')
        name = name_comp[naming] 
        
        print(name)
        
        #remove data with H_100 >= 0 prior to logging
        test2 = df[df['i_h100']>=0] 
        
        #means x is just the h100 data - needs logging to normalise (not skewed) 
        x = test2['i_h100']
        
        #create new column in df with log of H_100 
        y = np.log(x)
        test2a = test2.assign(log_i_h100 = y)
        
        if test2a.empty:
            continue

        #get quantiles
        a = np.quantile(test2a['log_i_h100'],0.95)
        b = np.quantile(test2a['log_i_h100'],0.05)

        #remove data outside of 5% quantiles
        test3 = test2a[test2a.log_i_h100 >b]
        final = test3[test3.log_i_h100 <a]

        if final.empty:
            continue
        del a, b, x, y, test2, test2a, test3

        footprints = len(final['i_h100'])
        
        resultsa = resultsa.append({'ID':name, 'deg_free':footprints}, ignore_index=True)
        resultsa.to_csv(fileout)