#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 15:19:54 2020

@author: heatherkay
"""


import pandas as pd
import numpy as np
from pandas import DataFrame
from scipy.optimize import curve_fit
import geopandas as gpd
import glob
from os import path
from sklearn.utils import resample as smpl
from joblib import Parallel, delayed

def ecoregions(folderin, fileout, naming=3, eco_loc=2):
    """
    Function to run bootstrpping with replacement over 100 iterations
    
    Parameters
    ----------
    
    folderin: string
            Filepath for folder with files ready for analysis
                         
    fileout: string
           Filepath for results file ending '.csv'

    naming: int
          Section of filename to obtain ID (here grid number). Obtained
          by splitting filename by '_' and indexing
          Default = 3

    eco_loc: int
          Section of filename to obtain ecoregion (if applicable). 
          Obtained as with naming
          Default = 2           
    """


    fileList = glob.glob(folderin + '*.shp')
    q_samples = pd.DataFrame(columns=['ID', 'mean_q', 'sd_q', 'SE'])
    
    def get_se(f,folderin, fileout, q_samples, naming=3, eco_loc=2):
        df2 = gpd.read_file(f)
        hd, tl = path.split(f)
        shp_lyr_name = path.splitext(tl)[0]
        name_comp = shp_lyr_name.split('_')
        name = name_comp[naming] 
        eco = name_comp[eco_loc]
        print(name)
        print(eco)

        q_values = pd.DataFrame(columns=['q'])
    
        for i in range(100):
            df = smpl(df2)
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
        
            def f(x,q):
                return 1- np.exp(-q * x)
    
            x = final['i_h100'].as_matrix()
            y = final['i_cd'].as_matrix() 
    
            qout, qcov = curve_fit(f, x, y, 0.04)
            qout = qout.round(decimals=4)
        
            q_values = q_values.append({'q':qout}, ignore_index=True)
            del df, final, x, y, qout
       
        mean_q = q_values['q'].mean()
        sd_q = q_values['q'].std()
        SE = sd_q/10
        q_samples = q_samples.append({'ID':name, 'mean_q':mean_q, 'sd_q':sd_q, 'SE':SE}, ignore_index=True)
        del mean_q, sd_q, q_values   
            #df2 = smpl(df, stratify=df['h_100'])
    q_samples.to_csv(fileout)   
            #means x is just the h100 data - needs logging to normalise (not skewed) 
    Parallel(n_jobs=50)(delayed(get_se)(f,folderin, fileout, naming=3, eco_loc=2)for f in fileList)