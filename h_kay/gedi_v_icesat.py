#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 12:34:20 2021

@author: heatherkay
"""
import pandas as pd
import matplotlib.pyplot as plt

#plot ICESat v GEDI results

def compare(gediin, icesatin, fileout):
    """
    A function which removes [] from string and converts number inside to a float. 
    For a columnn in a dataframe.
    
    Parameters
    ----------
    
    gediin: string
             path to input csv file with gedi data
             
    icesatin: string
            path for input csv file with ICESat data
            
    fileout: string
           path to save figure
    """
  
    df1 = pd.read_csv(gediin)
    df2 = pd.read_csv(icesatin)

    res = df1.merge(df2, how='inner', on='join')
    x= res['q_x']
    y= res['q_y']
    
    fig, ax = plt.subplots()
    ax.scatter(x, y, s=10, edgecolor='')
    ax.set_xlim([0,0.1])
    ax.set_ylim([0,0.1])
    ax.set_ylabel('ICESat q values')
    ax.set_xlabel('GEDI q values')
    plt.savefig(fileout)
    plt.close