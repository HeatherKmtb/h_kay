#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 14:05:38 2019

@author: heatherkay
"""

import pandas as pd
from functools import reduce
from glob import glob
from os import path

def stack_df (filein1, filein2, fileout):
    """
    A function which stacks data from two dataframes one aove the other
    
    Parameters
    ----------
    filein1: string
           filepath for first csv
           
    filein2: string
           filepath for second csv
           
    fileout: string
           filepath to save merged dataframe       
    """
    df1 = pd.read_csv(filein1)
    df2 = pd.read_csv(filein2)
    df = df1.append(df2, sort=True)
    df.to_csv(fileout)
    
       
def merge_on_col(folder, fileout, column='ID'):
    """
    A function which merges multiple dataframes on a specified column. 
    
    Dataframe files need to be contained in one folder
    
    Parameters
    ----------
    folder: string
          filepath for folder containing dataframes to be merged
          
    fileout: string
           filepath to save merged dataframe
           
    column: string
          column to join on. Default = 'ID'       
    """
    data_frames = glob((path.join(folder, '*.csv')))
 
    dfList = [pd.read_csv(d) for d in data_frames]
        
    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=[column],
                                            how='outer'), dfList)
    
    df_merged.to_csv(fileout)
