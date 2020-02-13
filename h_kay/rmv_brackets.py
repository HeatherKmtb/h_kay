#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 10:26:21 2019

@author: heatherkay
"""

import pandas as pd


def rmv_brackets(filepath, fileout, column='qout'):
    """
    A function which removes [] from string and converts number inside to a float. 
    For a columnn in a dataframe.
    
    Parameters
    ----------
    
    filepath: string
             path to input csv file
             
    fileout: string
            path for output csv file
            
    column: string
           title of column.
           default ('qout')
    """
    
    
    df = pd.read_csv(filepath)

    df1 = df[column] = df.qout.astype(str)
    df2 = df1.str.strip('[]').astype(float)

    df3 = df.assign(q = df2)

    df3.to_csv(fileout)
    
    #return df3 


# filepath = ('/Users/heatherkay/Desktop/MPhil/final_results_19.12/w.csv')
# fileout = ('/Users/heatherkay/Desktop/MPhil/final_results_19.12/w.csv')