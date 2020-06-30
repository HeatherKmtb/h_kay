#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 15:30:03 2020

@author: heatherkay
"""

import pandas as pd
import datetime
from datetime import timedelta
import glob
from os import path
import geopandas as gpd

def csv_date_file(filein, fileout):
    """
    Function to convert matlab datenum to day, month, year. For one file in 
    csv format
    
    Parameters
    ----------
    
    filein: string
            Filepath for .csv file with dates in matlab format
                          
    fileout: string
           Filepath for results file ending '.csv'
   
    """   
    df = pd.read_csv(filein)
    date = []
    year = []
    month = []
    
    matlab_datenum = df['i_acqdate']#.to_numpy()  
    datenum = matlab_datenum.astype(int)  
    
    for i in datenum:
        python_datetime = datetime.date.fromordinal(int(i) - 366) + timedelta(days=i%1)
        year1 = python_datetime.year
        month1 = python_datetime.month
        date.append(python_datetime)
        year.append(year1)
        month.append(month1)
    
    df['date'] = date
    df['year'] = year
    df['month'] = month

    df.to_csv(fileout)

def csv_date_folder(folderin, folderout):
    """
    Function to convert matlab datenum to day, month, year. For a folder of
    files in csv format
    
    Parameters
    ----------
    
    folderin: string
            Filepath for folder containing .csv files with dates in matlab format
                          
    folderout: string
           Filepath for folder for results files ending '.csv'
   
    """   
    fileList = glob.glob(folderin + '*.csv')
    
    for file in fileList:  
        hd, tl = path.split(file)
        name = tl.replace(".csv", "")
        df = pd.read_csv(file)
        date = []
        year = []
        month = []
        
        matlab_datenum = df['i_acqdate']#.to_numpy()  
        datenum = matlab_datenum.astype(int)  
        
        for i in datenum:
            python_datetime = datetime.date.fromordinal(int(i) - 366) + timedelta(days=i%1)
            year1 = python_datetime.year
            month1 = python_datetime.month
            date.append(python_datetime)
            year.append(year1)
            month.append(month1)
    
        df['date'] = date
        df['year'] = year
        df['month'] = month

        df.to_csv(folderout + '{}.csv'.format(name))
 
def shp_date_folder(folderin, folderout):
    """
    Function to convert matlab datenum to day, month, year and append as 
    columns to original file. For a folder of files in shp format
    
    Parameters
    ----------
    
    folderin: string
            Filepath for folder containing .shp files with dates in matlab 
            format
                          
    folderout: string
           Filepath for folder for results files ending '.shp'
   
    """   
    fileList = glob.glob(folderin + '*.shp')
    
    for file in fileList:  
        hd, tl = path.split(file)
        name = tl.replace(".shp", "")
        df = gpd.read_file(file)
        date = []
        year = []
        month = []
        
        if df.empty:
            continue
        matlab_datenum = df['i_acqdate']#.to_numpy()  
        datenum = matlab_datenum.astype(int)  
        print(name)
        
        for i in datenum:
            python_datetime = datetime.date.fromordinal(int(i) - 366) + timedelta(days=i%1)
            year1 = python_datetime.year
            month1 = python_datetime.month
            test = python_datetime.strftime('%Y-%m')
            date1 = test
            date.append(date1)
            year.append(year1)
            month.append(month1)
    
        df['date'] = date
        df['year'] = year
        df['month'] = month
               
        df.to_file(folderout + '{}.shp'.format(name))