#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 16:22:47 2020

@author: heatherkay
"""

import geopandas as gpd
import glob
from os import path
import numpy as np
import pandas as pd


def prep_clim(folderin, folderout):
    """
    Function to delete b1 column and rename clim as b1 for further processing. Also removes and NaN rows
    
    Parameters
    ----------
    folderin: string
            filepath for folder containing files to process
            
    folderout: string
            filepath for folder to save processed files           
    """    

    fileList = glob.glob(folderin + '*.shp')
    remove = [np.nan, np.inf, -np.inf]
    
    for file in fileList:
        hd, tl = path.split(file)
        name = tl.replace('.shp', "")
        print(name)
        df = gpd.read_file(file)
        df2 = df[np.logical_not(df['clim'].isin(remove))]
        del df2['b1']
        df3 = df2.rename(columns={'clim':'b1'})
        if df3.empty:
            continue
        df3.to_file(folderout + '{}.shp'.format(name))


def clim_var(filein, fileout):
    """
    Function to find varation in q within ecoregion, based on effect of climate variable
    
    Parameters
    ----------
    
    Filein: string
            Filepath with files to read in
                       
    Fileout: string
           Filepath for .csv with results        
    """
 
    df = gpd.read_file(filein) 
    df1 = df['deg_free'] = df.deg_free.astype(float)
    df2 = df.assign(ftprts=df1)
    ready = df2[df2['ftprts']>=70] #first make deg_free int or float
    results = pd.DataFrame(columns = ['eco','no_zones','variation'])   
    #import eco id
    #create list of ecoregions
    ecoregions = list(np.unique(df['ID']))
    for eco in ecoregions:
        new = ready.loc[ready['ID']==eco]
        data = new['qout'].str.strip('[]').astype(float)
        #maxi = data.max()
        #mini = data.min()
        #mean = data.mean()
        #variation = np.subtract(maxi, mini)
        variation = np.var(data)
        ecoR = eco
        no_zones = (len(data))
        results = results.append({'eco': ecoR, 'no_zones': no_zones, 
                                  'variation':variation}, ignore_index=True)
    
    results.to_csv(fileout)
      

