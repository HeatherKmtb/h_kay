#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 15:24:15 2020

@author: heatherkay
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn

def hist_seaborn(filein, fileout, column, xlab, ylab, title):
    """
    Function to plot histogram with seaborn
    
    Parameters
    ----------
    filein: string
          Filepath for dataframe to use for plotting
          
    fileout: string
           Filepath to save plot
           
    column: string
          Name of column with data for histogram
          
    xlab: string
        x axis label
        
    ylab: string
        y axis label  
        
    title: string    
         title for plot
    """
    df = pd.read_csv(filein)
    plot = df[column]
    
    fig1 = seaborn.distplot(plot)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.title(title)
    
    fig1 = fig1.get_figure()
    fig1.savefig(fileout)


def scatter_seaborn(filein, fileout, xdata, ydata, xlab, ylab, title):
    """
    Function to plot scatterplot with seaborn
    
    Parameters
    ----------
    filein: string
          Filepath for dataframe to use for plotting
          
    fileout: string
           Filepath to save plot
           
    xdata: string
          Name of column with data for x axis of scatterplot

    ydata: string
          Name of column with data for y axis of scatterplot
          
    xlab: string
        x axis label
        
    ylab: string
        y axis label  
        
    title: string    
         title for plot
    """
    df = pd.read_csv(filein)
    x = df[xdata]    
    y = df[ydata]    
    fig =seaborn.scatterplot(x=x, y=y)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.title(title)

    fig = fig.get_figure()
    fig.savefig(fileout)

def scatter_logx_seaborn(filein, fileout, xdata, ydata, xlab, ylab, title):
    """
    Function to plot scatterplot with seaborn (x axis data logged)
    
    Parameters
    ----------
    filein: string
          Filepath for dataframe to use for plotting (.csv)
          
    fileout: string
           Filepath to save plot (.pdf)
           
    xdata: string
          Name of column with data for x axis of scatterplot

    ydata: string
          Name of column with data for y axis of scatterplot
          
    xlab: string
        x axis label
        
    ylab: string
        y axis label  
        
    title: string    
         title for plot
    """
    df = pd.read_csv(filein)
    x1 = df[xdata]    
    y = df[ydata]  
    x = np.log(x1)
    fig =seaborn.scatterplot(x=x, y=y)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.title(title)

    fig = fig.get_figure()
    fig.savefig(fileout)