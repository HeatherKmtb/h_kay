#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 15:39:24 2020

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


def eco_per_annum(folderin, fileout):
    """
    Function to obtain average height and average cd per year and per ecoregion
    
    Parameters
    ----------
    
    folderin: string
            Filepath for folder with files ready for analysis

    fileout: string
           Filepath for results file ending '.csv'         
    """
    #import csv with IDs and convert to dict
    df_id2 = pd.read_csv('./eco/final_ID.csv')
    df_id = df_id2.astype({'ECO_ID': 'str'})
    eco_ID = df_id.set_index('ECO_ID')['ECO_NAME'].to_dict()

    #using 'file' to title plot  
    fileList = glob.glob(folderin + '*.shp')

    #create df for results
    resultsa = pd.DataFrame(columns = ['eco', 'ID', 'year', 'height', 'cd', 'deg_free'])
    #resultsb = pd.DataFrame(columns = ['eco', 'ID', 'qout', 'r_sq', 'deg_free', 'rmse'])

    for file in fileList:
        df = gpd.read_file(file)
        hd, tl = path.split(file)
        shp_lyr_name = path.splitext(tl)[0]
        name_comp = shp_lyr_name.split('_')
        eco_ID = name_comp[2]
        year = name_comp[4]
        ecoreg = eco_ID[name] 
        #remove data with H_100 >= 0 prior to logging
        test2 = df[df['i_h100']>=0] 
        footprints = len(df['i_h100'])
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
    
        #NEXT STEP. Bin remaining data in order to get mean and IQR of each bin

        cd = final['i_cd'].to_numpy()
        mean_cd = cd.mean()
        h = final['i_h100'].to_numpy()
        mean_h = h.mean()
        
        resultsa = resultsa.append({'eco': ecoreg, 'ID': eco_ID, 'year': year,
                                    'height': mean_h, 'cd': mean_cd, 
                                    'deg_free': footprints, ignore_index=True)

    resultsa.to_csv(fileout)


def eco_per_annum(folderin, fileout):
    """
    Function to obtain average height and average cd per year and per ecoregion
    
    Parameters
    ----------
    
    folderin: string
            Filepath for folder with files ready for analysis

    fileout: string
           Filepath for results file ending '.csv'         
    """
    #import csv with IDs and convert to dict
    df_id2 = pd.read_csv('./eco/final_ID.csv')
    df_id = df_id2.astype({'ECO_ID': 'str'})
    eco_ID = df_id.set_index('ECO_ID')['ECO_NAME'].to_dict()

    #using 'file' to title plot  
    fileList = glob.glob(folderin + '*.shp')

    #create df for results
    resultsa = pd.DataFrame(columns = ['eco', 'ID', 'year', 'height', 'cd', 'deg_free'])
    #resultsb = pd.DataFrame(columns = ['eco', 'ID', 'qout', 'r_sq', 'deg_free', 'rmse'])

    for file in fileList:
        df = gpd.read_file(file)
        hd, tl = path.split(file)
        shp_lyr_name = path.splitext(tl)[0]
        name_comp = shp_lyr_name.split('_')
        eco_ID = name_comp[2]
        year = name_comp[4]
        ecoreg = eco_ID[name] 
        #remove data with H_100 >= 0 prior to logging
        test2 = df[df['i_h100']>=0] 
        footprints = len(df['i_h100'])
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
    
        #NEXT STEP. Bin remaining data in order to get mean and IQR of each bin

        cd = final['i_cd'].to_numpy()
        mean_cd = cd.mean()
        h = final['i_h100'].to_numpy()
        mean_h = h.mean()
        
        resultsa = resultsa.append({'eco': ecoreg, 'ID': eco_ID, 'year': year,
                                    'height': mean_h, 'cd': mean_cd, 
                                    'deg_free': footprints, ignore_index=True)

    resultsa.to_csv(fileout)
