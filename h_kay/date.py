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

def date_file(filein, fileout):
    """
    Function to compute q and provide results (csv) and figures (pdf)
    
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

def date_folder(folderin, folderout):
    """
    Function to compute q and provide results (csv) and figures (pdf)
    
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
        