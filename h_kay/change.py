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
#from scipy.optimize import curve_fit
import geopandas as gpd
import glob
from os import path
#import matplotlib.pyplot as plt
import seaborn
import datetime


def eco_per_annum(filein, folderin, fileout):
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
    df_id2 = pd.read_csv(filein)
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
        ecoID = name_comp[2]
        year = name_comp[4]
        ecoreg = eco_ID[ecoID] 
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
        
        resultsa = resultsa.append({'eco': ecoreg, 'ID': ecoID, 'year': year,
                                    'height': mean_h, 'cd': mean_cd, 
                                    'deg_free': footprints}, ignore_index=True)

    resultsa.to_csv(fileout)

def sort_data(filein, fileout):
    """
    Function to remove 2006 & 2009 data (too few footprints) and find variation
    in average cd and height
    
    Parameters
    ----------
    
    filein: string
            Filepath for .csv with original results

    fileout: string
           Filepath for output results file ending '.csv'         
    """    
    df = pd.read_csv(filein)
    
    df1 = df[df['year'] != 2006]
    df3 = df1[df1['year'] != 2009]
    df2 = df3[df3['deg_free']>=100]
    
    results = pd.DataFrame(columns = ['ID', 'max_cd', 'min_cd', 'var_cd',
                           'max_h', 'min_h', 'var_h','2003', '2004', '2005',
                           '2007','2008'])
    ID = list(np.unique(df2['grid']))
    for eco in ID:
        new = df2.loc[df2['grid']==eco]
        max_cd = new['cd'].max()
        min_cd = new['cd'].min()
        max_h = new['height'].max()
        min_h = new['height'].min()
        var_cd = np.subtract(max_cd,min_cd)
        var_h = np.subtract(max_h,min_h)
        y2003 = new.query('year==2003')['height']
        if y2003.empty == False:
            y2003 = y2003.iloc[0]
        else:
            y2003 = float('NaN')
        y2004 = new.query('year==2004')['height']
        if y2004.empty == False:
            y2004 = y2004.iloc[0]
        else:
            y2004 = float('NaN')
        y2005 = new.query('year==2005')['height']
        if y2005.empty == False:
            y2005 = y2005.iloc[0]
        else:
            y2005 = float('NaN')
        y2007 = new.query('year==2007')['height']
        if y2007.empty == False:
            y2007 = y2007.iloc[0]
        else:
            y2007 = float('NaN')
        y2008 = new.query('year==2008')['height']
        if y2008.empty == False:
            y2008 = y2008.iloc[0]
        else:
            y2008 = float('NaN')
            
        results = results.append({'ID':eco, 'max_cd':max_cd, 'min_cd':min_cd,
                                 'var_cd':var_cd, 'max_h':max_h, 'min_h':min_h,
                                 'var_h':var_h,'2003':y2003, '2004':y2004, 
                                 '2005':y2005, '2007': y2007, '2008':y2008},
                                 ignore_index=True)
    
    c2004 = np.subtract(results['2004'],results['2003'])
    results['2003-04'] = c2004
    c2005 = np.subtract(results['2005'],results['2004'])
    results['2004-05'] = c2005    
    c2007 = np.subtract(results['2007'],results['2005'])
    results['2005-07'] = c2007    
    c2008 = np.subtract(results['2008'],results['2007'])
    results['2007-08'] = c2008
    
    results.to_csv(fileout)
    
def plot_mean_iqr(filein, fileout):
    """
    Function to remove
    
    Parameters
    ----------
    
    filein: string
            Filepath for .csv with original results

    fileout: string
           Filepath for output results file ending '.csv'         
    """   
    df = pd.read_csv(filein)
    
    colNms = ['2003','2004','2005','2007','2008']    
    results = pd.DataFrame(columns = ['year','mean','iqr'])
    #calculate means and iqrs
    for col in colNms:
        name = col
        data = df[col]
        new = data.dropna()
        mean = new.mean()
        q75, q25 = np.percentile(new, [75, 25])
        iqr = q75 - q25
        results = results.append({'year':name,'mean':mean,'iqr':iqr}, ignore_index=True)

    #plot the result
    fig = plt.figure(); ax = fig.add_subplot(1,1,1)
    plt.rcParams.update({'font.size':12})
    #define x and y
    x = results['year']
    y = results['mean']
    iqr = results['iqr']
    #plt.plot(x,y)
    #plots IQR
    plt.errorbar(x,y, yerr=iqr,)
    #sets title and axis labels
    ax.set_title('interannual height variation')
    ax.set_ylabel('Mean height (m)')
    ax.set_xlabel('Year')
    #ax.set_xlim([0, 60])
    #ax.set_ylim([0,1])
    plt.savefig('/Users/heatherkay/q_research/change/fig.pdf')
    
#short section of code to obtain annual mean of height data
#filein = '/Users/heatherkay/q_research/change/test_year/2007.shp'
df = gpd.read_file(filein)
height = df['i_h100']
mean = height.mean()
deg_free = len(height)
print(mean)
print(deg_free)


def plot_grid_per_annum(folderin, folderout):
    """
    Function to generate histogram of height values for each year within a grid cell
    
    Parameters
    ----------
    
    folderin: string
            Filepath for folder with files ready for analysis

    fileout: string
           Filepath for results file ending '.csv'         
    """

    #using 'file' to title plot  
    fileList = glob.glob(folderin + '*.shp')

    #create df for results
    #resultsa = pd.DataFrame(columns = ['eco', 'ID', 'year', 'height', 'cd', 'deg_free'])
    #resultsb = pd.DataFrame(columns = ['eco', 'ID', 'qout', 'r_sq', 'deg_free', 'rmse'])

    for file in fileList:
        df1 = gpd.read_file(file)
        hd, tl = path.split(file)
        shp_lyr_name = path.splitext(tl)[0]
        name_comp = shp_lyr_name.split('_')
        grid = name_comp[2]
        year = list(np.unique(df1['year']))
        if year[-1]==2009:
            year.remove(2009)
        else:
            continue
                
        
        for annum in year:
            
            df = df1.loc[df1['year']==annum]
            #remove data with H_100 >= 0 prior to logging
            test2 = df[df['i_h100']>=0] 
            #footprints = len(df['i_h100'])
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
            
            
            bins= np.arange(0, 55+5, 5)
            plot = final['i_h100']
            xlab = 'height (m)'
            ylab = 'distribution frequency'
            yr = str(annum)

            title = ('histogram for grid ' + grid)
            fig1 = seaborn.distplot(plot, bins=bins, label=yr)
            
  
            plt.legend()
            plt.xlabel(xlab)
            plt.ylabel(ylab)
            plt.title(title)
    
            fig1 = fig1.get_figure()
            fig1.savefig(folderout + 'fig{}.pdf'.format(grid))
        
        fig1.clf()
                   

def grid_per_annum(folderin, fileout):
    """
    Function to obtain average height and average cd per year and per grid
    
    Parameters
    ----------
    
    folderin: string
            Filepath for folder with files ready for analysis

    fileout: string
           Filepath for results file ending '.csv'         
    """
    #using 'file' to title plot  
    fileList = glob.glob(folderin + '*.shp')

    #create df for results
    resultsa = pd.DataFrame(columns = ['grid', 'year', 'height', 'cd', 'deg_free'])
    #resultsb = pd.DataFrame(columns = ['eco', 'ID', 'qout', 'r_sq', 'deg_free', 'rmse'])

    for file in fileList:
        df1 = gpd.read_file(file)
        hd, tl = path.split(file)
        shp_lyr_name = path.splitext(tl)[0]
        name_comp = shp_lyr_name.split('_')
        grid = name_comp[2]
        year = list(np.unique(df1['year']))
             
       
        for annum in year:        
            df = df1.loc[df1['year']==annum]
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

            resultsa = resultsa.append({'grid':grid, 'year': annum,
                                    'height': mean_h, 'cd': mean_cd, 
                                    'deg_free': footprints}, ignore_index=True)

    resultsa.to_csv(fileout)    
    
def get_laser_period(folderin, folderout):
    """
    Function to generate new shapefiles split per laser period 
        
    Parameters
    ----------
    
    folderin: string
            Filepath for folder with files ready for analysis

    folderout: string
           Filepath for output shapefile folder        
    """
        
    fileList = glob.glob(folderin + '*.shp')


    for file in fileList:
        df = gpd.read_file(file)
        hd, tl = path.split(file)
        shp_lyr_name = path.splitext(tl)[0]
        name_comp = shp_lyr_name.split('_')
        grid = name_comp[2]
        #year = list(np.unique(df1['year']))
        #datestr = df1['i_acqdate']
        #date=[]
               
        #test3 = test2a[test2a.log_i_h100 >b]
        #final = test3[test3.log_i_h100 <a]       
        ph1 = df[df.i_acqdate < 731699]        
        ph2a1 = df[df.i_acqdate < 732150]
        ph2a = ph2a1[ph2a1.i_acqdate > 731825]
        ph31 = df[df.i_acqdate < 733710]
        ph3 = ph31[ph31.i_acqdate > 732190]
        ph2b1 = df[df.i_acqdate < 734100]
        ph2b = ph2b1[ph2b1.i_acqdate > 733720]

        if ph1.empty == False:          
            ph1.to_file(folderout + 'ph1_{}.shp'.format(grid))
        else:
            print('ph1_' + grid)
        if ph2a.empty == False:        
            ph2a.to_file(folderout + 'ph2a_{}.shp'.format(grid))
        else:
            print('ph2a_' + grid)
        if ph2b.empty == False:
            ph2b.to_file(folderout + 'ph2b_{}.shp'.format(grid))
        else:
            print('ph2b_' + grid)       
        if ph3.empty == False:
            ph3.to_file(folderout + 'ph3_{}.shp'.format(grid))
        else:
            print('ph3_' + grid)        
        
           

def mean_per_phase(folderin, fileout):
    """
    Function to obtain average height and average cd per Laser period
    
    Parameters
    ----------
    
    folderin: string
            Filepath for folder with files ready for analysis

    fileout: string
           Filepath for results file ending '.csv'         
    """
    #using 'file' to title plot  
    fileList = glob.glob(folderin + '*.shp')

    #create df for results
    resultsa = pd.DataFrame(columns = ['Laser', 'year', 'height', 'cd', 'deg_free'])
    #resultsb = pd.DataFrame(columns = ['eco', 'ID', 'qout', 'r_sq', 'deg_free', 'rmse'])

    for file in fileList:
        df = gpd.read_file(file)
        hd, tl = path.split(file)
        name = tl.replace('.shp', "")
        

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

        resultsa = resultsa.append({'Laser':name, 'height': mean_h, 'cd': mean_cd, 
                                    'deg_free': footprints}, ignore_index=True)

    resultsa.to_csv(fileout)    
        

def mean_per_intact(folderin, fileout):
    """
    Function to obtain average height and average cd per year 
    
    Parameters
    ----------
    
    folderin: string
            Filepath for folder with files ready for analysis

    fileout: string
           Filepath for results file ending '.csv'         
    """
    #using 'file' to title plot  
    fileList = glob.glob(folderin + '*.shp')

    #create df for results
    resultsa = pd.DataFrame(columns = ['location', 'year', 'height', 'cd', 'deg_free'])
    #resultsb = pd.DataFrame(columns = ['eco', 'ID', 'qout', 'r_sq', 'deg_free', 'rmse'])

    for file in fileList:
        df1 = gpd.read_file(file)
        hd, tl = path.split(file)
        shp_lyr_name = path.splitext(tl)[0]
        name_comp = shp_lyr_name.split('_')
        name = name_comp[1]
        year = list(np.unique(df1['year']))
             
       
        for annum in year:        
            df = df1.loc[df1['year']==annum]
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

            resultsa = resultsa.append({'location':name, 'year': annum,
                                    'height': mean_h, 'cd': mean_cd, 
                                    'deg_free': footprints}, ignore_index=True)

    resultsa.to_csv(fileout)    
            
def plot_intact(folderin, folderout):
    """
    Function to generate histogram of height values for each year within a grid cell
    
    Parameters
    ----------
    
    folderin: string
            Filepath for folder with files ready for analysis

    fileout: string
           Filepath for results file ending '.csv'         
    """

    #using 'file' to title plot  
    fileList = glob.glob(folderin + '*.shp')

    #create df for results
    #resultsa = pd.DataFrame(columns = ['eco', 'ID', 'year', 'height', 'cd', 'deg_free'])
    #resultsb = pd.DataFrame(columns = ['eco', 'ID', 'qout', 'r_sq', 'deg_free', 'rmse'])

    for file in fileList:
        df1 = gpd.read_file(file)
        hd, tl = path.split(file)
        shp_lyr_name = path.splitext(tl)[0]
        name_comp = shp_lyr_name.split('_')
        region = name_comp[1]
        year = list(np.unique(df1['year']))
        if year[-1]==2009:
            year.remove(2009)
        else:
            continue
                
        
        for annum in year:
            
            df = df1.loc[df1['year']==annum]
            #remove data with H_100 >= 0 prior to logging
            test2 = df[df['i_h100']>=0] 
            #footprints = len(df['i_h100'])
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
            
            
            bins= np.arange(0, 55+5, 5)
            plot = final['i_h100']
            xlab = 'height (m)'
            ylab = 'distribution frequency'
            yr = str(annum)

            title = ('histogram for ' + region)
            fig1 = seaborn.distplot(plot, bins=bins, label=yr)
            
  
            plt.legend()
            plt.xlabel(xlab)
            plt.ylabel(ylab)
            plt.title(title)
    
            fig1 = fig1.get_figure()
            fig1.savefig(folderout + 'fig{}.pdf'.format(region))
        
        fig1.clf()
                      