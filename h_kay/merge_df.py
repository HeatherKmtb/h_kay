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

def stack_multi_df(folderin, fileout):
    """
    A function which stacks data from two dataframes one aove the other
    
    Parameters
    ----------
    folderin: string
           filepath for folder containing dataframes to be stacked
                      
    fileout: string
           filepath to save merged dataframe       
    """
    data_frames = glob((path.join(folderin, '*.csv')))
 
    dfList = [pd.read_csv(d) for d in data_frames]
    
    df = pd.concat(dfList)  
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

def join_col_shp(filein, fileout, column1, column2, join_column='join'):
    """
    Function to join data in 2 columns as a string, plus remove brackets from 'qout' column
    
    Parameters
    ----------
    filein: string
            filepath for shp file to process
            
    folderout: string
            filepath to save processed file
            
    column1: string
            name of first column to join
            
    column2: string
            name of second column to join  

    join_column: string
            name of column with join string
            Default = 'join'             
    """      
    
    df = gpd.read_file(filein)
    df[join_column] = df[column1].astype(str) + '_' + df[column2].astype(str)
    df1 = df['qout'] = df.qout.astype(str)
    df2 = df1.str.strip('[]').astype(float)
    df3 = df.assign(q = df2)
    df3.to_file(fileout)
    
def join_col_csv(filein, fileout, column1, column2, join_column='join'):
    """
    Function to join data in 2 columns as a string, plus remove brackets from 'qout' column
    
    Parameters
    ----------
    filein: string
            filepath for shp file to process
            
    folderout: string
            filepath to save processed file
            
    column1: string
            name of first column to join
            
    column2: string
            name of second column to join  

    join_column: string
            name of column with join string
            Default = 'join'             
    """      
    
    df = pd.read_csv(filein)
    df[join_column] = df[column1].astype(str) + '_' + df[column2].astype(str)
    df1 = df['qout'] = df.qout.astype(str)
    df2 = df1.str.strip('[]').astype(float)
    df3 = df.assign(q = df2)
    df3.to_csv(fileout)    
