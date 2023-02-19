#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 14:30:11 2022

@author: heatherkay
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
from scipy.optimize import curve_fit
import geopandas as gpd
import glob
from os import path


def grid_only(folderin, fileout, folderout, naming=3):
    """
    Function to compute q and provide results (csv) and figures (pdf)
    
    Parameters
    ----------
    
    folderin: string
            Filepath for folder with files ready for analysis
                
    naming: int
          Section of filename to obtain ID (here grid number). Obtained
          by splitting filename by '_' and indexing
          Default = 3

    eco_loc: int
          Section of filename to obtain ecoregion (if applicable). 
          Obtained as with naming
          Default = 2
          
    fileout: string
           Filepath for results file ending '.csv'
           
    folderout: string
             Filepath for folder to save the figures            
    """

    #using 'file' to title plot  
    fileList = glob.glob(folderin + '*.shp')

    #create df for results
    resultsa = pd.DataFrame(columns = ['ID', 'qout', 'r_sq', 'deg_free', 'rmse','mean_h', 'mean_cd', 'max_h'])
    #resultsb = pd.DataFrame(columns = ['eco', 'ID', 'qout', 'r_sq', 'deg_free', 'rmse'])

    for file in fileList:
        df = gpd.read_file(file)
        if df.empty:
            continue 
        hd, tl = path.split(file)
        shp_lyr_name = path.splitext(tl)[0]
        name_comp = shp_lyr_name.split('_')
        name = name_comp[naming] 
        #eco = name_comp[eco_loc]
        print(name)
        #print(eco)
        #remove data with H_100 >= 0 prior to logging
        df2 = df.dropna(subset=['i_h100'])
        final = df2[df2['i_h100']>=0] 
        footprints = len(df['i_h100'])
        #means x is just the h100 data - needs logging to normalise (not skewed) 


        if footprints < 100:
            continue
        
        #NEXT STEP. Bin remaining data in order to get mean and IQR of each bin

        #add column with bins 
        final['H_bins']=pd.cut(x=final['i_h100'], bins=np.arange(0, 120+2, 2))

        #now something along the lines of:
        #for bin in HBins find the mean and IQR...
        #first create lists to append mean and IQRs to
        cd_mean = []
        cd_iqr = []
        #Hbin = []
        print(name)
        #print(eco)
        HBins = list(np.unique(final['H_bins']))
        print(HBins)
        for bins in HBins:
            #for each one make a df with just that bin
            new = final.loc[final['H_bins']==bins]
            #get mean and IQR of each bin
            data = new['i_cd'].to_numpy()
            mean = data.mean()
            cd_mean.append(mean)
            q75, q25 = np.percentile (data, [75, 25])
            iqr = q75 - q25
            cd_iqr.append(iqr)
    
        #getting median of bins for mean r2 calculation
        greats = []
        for index,i in final.iterrows():
            great = [i['H_bins'].left + 1] 
            greats.append(great)

    
        final['H_bin'] = greats 
        new1 = final['H_bin'] = final.H_bin.astype(str)
        new2 = new1.str.strip('[]').astype(int)
        final['H_bin1'] = new2
        
        del new, data, q75, q25, new1 
    
        #get median of bins for plotting
        med = [binn.left + 1 for binn in HBins]
        plot = pd.DataFrame({'mean': cd_mean, 'iqr': iqr, 'bins': HBins, 'median': med})
        bin_dict = plot.set_index('median')['mean'].to_dict()
    
        plot_y = []
        for i in final['H_bin1']:
            y = bin_dict[i]
            plot_y.append(y)
            del y
        
        final['plot_y'] = plot_y
     
        #regression 
        def f(x,q):
            return 1- np.exp(-q * x)
    
        x = final['i_h100'].to_numpy()
        y = final['i_cd'].to_numpy() 
        x = np.append(x, [0])
        y = np.append(y, [0])
    
        qout, qcov = curve_fit(f, x, y, 0.04)
        qout = qout.round(decimals=4)
        #calculating mean r2
        residuals = plot_y - f(new2, qout)
        res_ss = np.sum(residuals**2)
        tot_ss = np.sum((plot_y-np.mean(plot_y))**2)
        r_sq_mean = 1 - (res_ss/tot_ss)
        #deg_free = (len(x)-1)
        r_sq_mean = round(r_sq_mean, 2)
        y_predict = f(x, qout)
        
        #calculating r2
        residuals2 = y - f(x, qout)
        res_ss2 = np.sum(residuals2**2)
        tot_ss2 = np.sum((y-np.mean(y))**2)
        r_sq = 1- (res_ss2/tot_ss2)
        r_sq = round(r_sq, 2)
            
        from sklearn.metrics import mean_squared_error
        from math import sqrt
        mse = mean_squared_error(y, y_predict)
        rms = sqrt(mse)
        rms = round(rms, 4)
        
        meanh = np.mean(x)
        meancd = np.mean(y)
        maxh = np.max(x)

        #fig1 = plt.figure(); ax =fig1.add_subplot(1,1,1)
        #ax.scatter(plot['y'],plot['y_predict'])
        #plt.savefig1('./eco/results/figs/values{}.pdf'.format(name))
        #plt.close
        
        #extract info: eco, qout, r_sq, deg_free (only gets one eco in data)
        resultsa = resultsa.append({'ID': name, 'qout': qout, 'r_sq': r_sq, 'deg_free': footprints, 'rmse': rms, 'mean_h': meanh, 'mean_cd': meancd, 'max_h': maxh}, ignore_index=True)
        #if deg_free>=60:
            #resultsb = resultsb.append({'eco': name2, 'ID': name, 'qout': qout, 'r_sq': r_sq, 'deg_free': deg_free, 'rmse': rms}, ignore_index=True)        
            #export to excel
        resultsa.to_csv(fileout)
            #resultsb.to_csv('./eco/new/results/results_over60.csv')

        #plot the result
        fig = plt.figure(); ax = fig.add_subplot(1,1,1)
        plt.rcParams.update({'font.size':12})
        #plots H_100 on x with I_CD on y
        ax.scatter(plot['median'],plot['mean'])
        #plots IQR
        ax.bar(plot['median'],plot['mean'],width=0, yerr=plot['iqr'])
        #sets title and axis labels
        ax.set_title('Grid no.' + name)
        ax.set_ylabel('Canopy Density')
        ax.set_xlabel('Height - h100 (m)')
        ax.set_xlim([0, 60])
        ax.set_ylim([0,1])
        #plotting regression
        #putting x data in an order, cause that's what the code needs
        xdata = np.linspace(0, 60)
        #for each value of x calculating the corresponding y value
        ycurve = [f(t, qout) for t in xdata]
        #plotting the curve
        ax.plot(xdata, ycurve, linestyle='-')
        #adding qout, r_sq and deg_free to plot
        ax.annotate('q = ' + str(qout[0]), xy=(0.975,0.20), xycoords='axes fraction', fontsize=12, horizontalalignment='right', verticalalignment='bottom')
        ax.annotate('r2 = ' + str(r_sq), xy=(0.975,0.15), xycoords='axes fraction', fontsize=12, horizontalalignment='right', verticalalignment='bottom')
        ax.annotate('RMSE = ' + str(rms),xy=(0.975,0.10), xycoords='axes fraction', fontsize=12, horizontalalignment='right', verticalalignment='bottom')   
        ax.annotate('No of footprints = ' + str(footprints),xy=(0.975,0.05), xycoords='axes fraction', fontsize=12, horizontalalignment='right', verticalalignment='bottom')
        plt.savefig(folderout + 'fig{}.pdf'.format(name))
        plt.close
        