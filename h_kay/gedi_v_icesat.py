#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 12:34:20 2021

@author: heatherkay
"""
import pandas as pd
import matplotlib.pyplot as plt
from os import path
import numpy as np

#plot ICESat v GEDI results

def compare(gediin, icesatin, fileout, csv_out):
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

    res = df1.merge(df2, how='inner', on='Grid')
    df1 = res['qout'] = res.qout.astype(str)
    df2 = df1.str.strip('[]').astype(float)
    df3 = res.assign(q_glas = df2)
    df4 = df3['qout_gedi'] = df3.qout_gedi.astype(str)
    df5 = df4.str.strip('[]').astype(float)
    df6 = df3.assign(q_gedi = df5)    
    x= df6['q_gedi']
    y= df6['q_glas']
    z=[0, 0.05, 0.1]
    
    diff = x - y
    
    df7 = df6[df6['deg_free_g']>=100] 
    df8 = df7[df7['deg_free']>=100] 
    new_df = df8.assign(difference = diff)
    
    grid = 'gedi_' + new_df['Grid']
    out_df = new_df.assign(Gedi_Grid = grid)
    out_df.to_csv(csv_out)
    
    fig, ax = plt.subplots()
    ax.scatter(x, y, s=10)
    ax.plot(z,z, color='red')
    ax.set_xlim([0,0.1])
    ax.set_ylim([0,0.1])
    ax.set_title('GEDI v ICESat Q3 2020')
    ax.set_ylabel('ICESat q values')
    ax.set_xlabel('GEDI q values')
    plt.savefig(fileout)
    plt.close
    
def compare_gedis(gedi1in, gedi2in, fig_out, csv_out):
    """
    A function which prepares 2 of the results dataframes, and produces a new
    combined csv and a figure comparing q values.
    
    Parameters
    ----------
    
    gedi1in: string
             path to input csv file with gedi data
             
    gedi2in: string
            path for another input csv file with gedi data
            
    fig_out: string
           path to save figure
           
    parquet_out: string
           path to save df as parquet       
    """
  
    df1 = pd.read_csv(gedi1in)
    df2 = pd.read_csv(gedi2in) 
    
    g1 = path.basename(gedi1in)[0:7]
    g2 = path.basename(gedi2in)[0:7]
    
    res = df1.merge(df2, how='inner', on='Grid')
    df1 = res['qout_gedi_x'] = res.qout_gedi_x.astype(str)
    df2 = df1.str.strip('[]').astype(float)
    df3 = res.assign(q_gedi_x = df2)
    df4 = df3['qout_gedi_y'] = df3.qout_gedi_y.astype(str)
    df5 = df4.str.strip('[]').astype(float)
    df6 = df3.assign(q_gedi_y = df5)    
    x= df6['q_gedi_x']
    y= df6['q_gedi_y']
    z=[0, 0.05, 0.1]
    
    diff = x - y
    
    df7 = df6[df6['deg_free_g_x']>=100] 
    df8 = df7[df7['deg_free_g_y']>=100] 
    new_df = df8.assign(difference = diff)
    
    grid = 'gedi_' + new_df['Grid']
    out_df = new_df.assign(Gedi_Grid = grid)
    out_df.to_csv(csv_out)
    
    fig, ax = plt.subplots()
    ax.scatter(x, y, s=10)
    ax.plot(z,z, color='red')
    ax.set_xlim([0,0.1])
    ax.set_ylim([0,0.1])
    ax.set_title(g1 + ' v ' + g2)
    ax.set_ylabel(g2 + ' q values')
    ax.set_xlabel(g1 + ' q values')
    plt.savefig(fig_out)
    plt.close

def compare_cd_and_h(gediin, figs_out):
    """
    A function which prepares 2 of the results dataframes, and produces a new
    combined csv and a figure comparing q values.
    
    Parameters
    ----------
    
    gediin: string
             path to input csv file with gedi data already joined with 
             compare_gedis above
                   
    figs_out: string
           path for folder to save figure with cd data
           
         
    """
    
    df = pd.read_csv(gediin)
    g1 = path.basename(gediin)[0:10]
    q1 = g1[5:7]
    q2 = g1[8:10]
    
    cd_fig_out = figs_out + g1 + 'cd.png'
    h_fig_out = figs_out + g1 + 'h.png'
    
    x= df['mean_cd_g_x']
    y= df['mean_cd_g_y']
    z=[0, 1]
    
    fig, ax = plt.subplots()
    ax.scatter(x, y, s=10)
    ax.plot(z,z, color='red')
    ax.set_xlim([0,1])
    ax.set_ylim([0,1])
    ax.set_title(g1)
    ax.set_ylabel(q2 + ' cd values')
    ax.set_xlabel(q1 + ' cd values')
    plt.savefig(cd_fig_out)
    plt.close
    
    x= df['mean_h_g_x']
    y= df['mean_h_g_y']
    z=[0, 60]
    
    fig, ax = plt.subplots()
    ax.scatter(x, y, s=10)
    ax.plot(z,z, color='red')
    ax.set_xlim([0,60])
    ax.set_ylim([0,60])
    ax.set_title(g1)
    ax.set_ylabel(q2 + ' h values')
    ax.set_xlabel(q1 + ' h values')
    plt.savefig(h_fig_out)
    plt.close
    
    
def compare_cd_and_h_icesat(gediin, figs_out):
        """
        A function which prepares 2 of the results dataframes, and produces a new
        combined csv and a figure comparing q values.
        
        Parameters
        ----------
        
        gediin: string
                 path to input csv file with gedi data already joined with 
                 compare_gedis above
                       
        figs_out: string
               path for folder to save figure with cd data
               
             
        """
        
        df = pd.read_csv(gediin)
        g1 = 'ICESat v GEDI 2020 Q3' 
        q1 = 'GEDI'
        q2 = 'ICESat GLAS'
        
        cd_fig_out = figs_out + g1 + 'cd.png'
        h_fig_out = figs_out + g1 + 'h.png'
        
        x= df['mean_cd_g']
        y= df['mean_cd']
        z=[0, 1]
        
        diff = x - y

        new_df = df.assign(difference_cd = diff)
        
        fig, ax = plt.subplots()
        ax.scatter(x, y, s=10)
        ax.plot(z,z, color='red')
        ax.set_xlim([0,1])
        ax.set_ylim([0,1])

        m, b = np.polyfit(x, y, 1)
        plt.plot(x, m*x+b, color='black')
        ax.set_title(g1)
        ax.set_ylabel(q2 + ' cd values')
        ax.set_xlabel(q1 + ' cd values')
        plt.savefig(cd_fig_out)
        plt.close
        
        x= df['mean_h_g']
        y= df['mean_h']
        z=[0, 60]
        
        diff = x - y

        out_df = new_df.assign(difference_h = diff)
        out_df.to_csv(figs_out + g1 + ' cd_and_h.csv')
        
        fig, ax = plt.subplots()
        ax.scatter(x, y, s=10)
        ax.plot(z,z, color='red')
        ax.set_xlim([0,60])
        ax.set_ylim([0,60])
        m, b = np.polyfit(x, y, 1)
        plt.plot(x, m*x+b, color='black')
        ax.set_title(g1)
        ax.set_ylabel(q2 + ' h values')
        ax.set_xlabel(q1 + ' h values')
        plt.savefig(h_fig_out)
        plt.close
        
        
#Random code
high_cd = df[df['mean_cd_g']>=0.6] 
low_cd = df[df['mean_cd_g']<0.5] 

x= high_cd['mean_cd_g']
y= high_cd['mean_cd']
z=[0, 1]


fig, ax = plt.subplots()
ax.scatter(x, y, s=10)
ax.plot(z,z, color='red')
ax.set_xlim([0,1])
ax.set_ylim([0,1])

m, b = np.polyfit(x, y, 1)
plt.plot(x, m*x+b, color='black')
ax.set_title('mean cd values ICEsat v GEDI 2020 Q3')
ax.set_ylabel('ICESat mean cd values')
ax.set_xlabel('GEDI mean cd values')
plt.savefig(figout)
plt.close
        
        