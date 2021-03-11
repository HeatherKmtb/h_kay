#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 11:09:48 2020

@author: heatherkay
"""

import numpy as np
#import mpl_scatter_density
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame
from scipy.optimize import curve_fit
import geopandas as gpd
import glob
from os import path
#from matplotlib.colors import LinearSegmentedColormap
from scipy.stats import gaussian_kde

      

def grid2(folderin, fileout, folderout, naming=4, eco_loc=2):
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
    resultsa = pd.DataFrame(columns = ['eco', 'ID', 'qout', 'r_sq', 'deg_free', 'mse','r_sq_mean', 'adj_r2'])
    #resultsb = pd.DataFrame(columns = ['eco', 'ID', 'qout', 'r_sq', 'deg_free', 'rmse'])

    for file in fileList:
        df = gpd.read_file(file)
        if df.empty:
            continue 
        hd, tl = path.split(file)
        shp_lyr_name = path.splitext(tl)[0]
        name_comp = shp_lyr_name.split('_')
        name = name_comp[naming] 
        eco = name_comp[eco_loc]
        print(name)
        print(eco)
        #remove data with H_100 >= 0 prior to logging
        test2 = df[df['i_h100']>=0] 
        
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

        footprints = len(final['i_h100'])
        
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
        print(eco)
        HBins = list(np.unique(final['H_bins']))
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
        
        #calculating adjusted r2
        stage1 = (footprints - 1)/(footprints - 3)
        stage2 = 1-(1-r_sq)
        adj_r2= stage1 * stage2
        adj_r2 = round(adj_r2, 2)
            
        from sklearn.metrics import mean_squared_error
        from math import sqrt
        mse = mean_squared_error(y, y_predict)
        mse = round(mse, 3)
        rms = sqrt(mse)
        rms = round(rms, 4)
        
        #fig1 = plt.figure(); ax =fig1.add_subplot(1,1,1)
        #ax.scatter(plot['y'],plot['y_predict'])
        #plt.savefig1('./eco/results/figs/values{}.pdf'.format(name))
        #plt.close
        
        #extract info: eco, qout, r_sq, deg_free (only gets one eco in data)
        resultsa = resultsa.append({'eco': eco, 'ID': name, 'qout': qout, 
                                    'r_sq': r_sq, 'deg_free': footprints, 
                                    'mse': mse, 'r_sq_mean': r_sq_mean, 
                                    'adj_r2': adj_r2}, ignore_index=True)
        #if deg_free>=60:
            #resultsb = resultsb.append({'eco': name2, 'ID': name, 'qout': qout, 'r_sq': r_sq, 'deg_free': deg_free, 'rmse': rms}, ignore_index=True)        
            #export to excel
        resultsa.to_csv(fileout)
            #resultsb.to_csv('./eco/new/results/results_over60.csv')
#fig = plt.figure()
#ax = fig.add_subplot(1, 1, 1, projection='scatter_density')
#ax.scatter_density(x, y)
#ax.set_xlim(-5, 10)
#ax.set_ylim(-5, 10)
#fig.savefig('gaussian.png')

        #plot the result
        #fig = plt.figure(); ax = fig.add_subplot(1,1,1, projection='scatter_density')
        
        #plots H_100 on x with I_CD on y
        xy = np.vstack([x,y])
        z = gaussian_kde(xy)(xy)

        fig, ax = plt.subplots()
        ax.scatter(x, y, c=z, s=10, edgecolor='')
        plt.rcParams.update({'font.size':12}) 
        #plt.colorbar()
        #plots IQR
        #ax.bar(plot['median'],plot['mean'],width=0, yerr=plot['iqr'])
        #sets title and axis labels
        ax.set_title('Grid ' + name + ' in ecoregion ' + eco)
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
        ax.plot(xdata, ycurve, linestyle='-', color='red')
        #adding qout, r_sq and deg_free to plot
        #ax.annotate('adj_r2 = ' + str(adj_r2[0]), xy=(0.975,0.10), xycoords='axes fraction', fontsize=12, horizontalalignment='right', verticalalignment='bottom')
        ax.annotate('q = ' + str(qout[0]), xy=(0.975,0.15), xycoords='axes fraction', fontsize=12, horizontalalignment='right', verticalalignment='bottom')
        ax.annotate('MSE = ' + str(mse), xy=(0.975,0.10), xycoords='axes fraction', fontsize=12, horizontalalignment='right', verticalalignment='bottom')
        #ax.annotate(u'R\u0305'u'\u00b2 of the mean = ' + str(r_sq_mean),xy=(0.975,0.10), xycoords='axes fraction', fontsize=12, horizontalalignment='right', verticalalignment='bottom')   
        ax.annotate('No of footprints = ' + str(footprints),xy=(0.975,0.05), xycoords='axes fraction', fontsize=12, horizontalalignment='right', verticalalignment='bottom')
        plt.savefig(folderout + 'fig{}_{}.pdf'.format(eco, name))
        plt.close     
        

      

def grid_test(folderin, fileout, folderout, naming=4, eco_loc=2):
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
    df_id2 = pd.read_csv('./eco/final_ID.csv')
    df_id = df_id2.astype({'ECO_ID': 'str'})
    eco_ID = df_id.set_index('ECO_ID')['ECO_NAME'].to_dict()

    #using 'file' to title plot  
    fileList = glob.glob(folderin + '*.shp')

    #create df for results
    resultsa = pd.DataFrame(columns = ['eco', 'ID', 'qout', 'deg_free', 'mse', 'join', 'q'])
    #resultsb = pd.DataFrame(columns = ['eco', 'ID', 'qout', 'r_sq', 'deg_free', 'rmse'])

    for file in fileList:
        df = gpd.read_file(file)
        if df.empty:
            continue 
        hd, tl = path.split(file)
        shp_lyr_name = path.splitext(tl)[0]
        name_comp = shp_lyr_name.split('_')
        name = name_comp[naming] 
        eco = name_comp[eco_loc]
        eco_name = eco_ID[eco]
        print(name)
        print(eco)
        #remove data with H_100 >= 0 prior to logging
        test2 = df[df['i_h100']>=0] 
        
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


        footprints = len(final['i_h100'])
        
        if footprints < 100:
            continue
            
        #regression 
        def f(x,q):
            return 1- np.exp(-q * x)
    
        x = final['i_h100'].to_numpy()
        y = final['i_cd'].to_numpy() 
        x = np.append(x, [0])
        y = np.append(y, [0])
    
        qout, qcov = curve_fit(f, x, y, 0.04)
        qout = qout.round(decimals=4)
        
        y_predict = f(x, qout)
            
        from sklearn.metrics import mean_squared_error

        mse = mean_squared_error(y, y_predict)
        mse = round(mse, 3)
        
        #j_e = eco.astype(str)
        #j_g = name.astype(str)
        join = eco + '_' + name
        
        q1 = qout.astype(str)
        q = q1.str.strip('[]').astype(float)
        
        resultsa = resultsa.append({'eco': eco, 'ID': name, 'qout': qout, 
                                    'deg_free': footprints, 
                                    'mse': mse, 'join': join, 'q': q}, 
                                    ignore_index=True)

        resultsa.to_csv(fileout)

        xy = np.vstack([x,y])
        z = gaussian_kde(xy)(xy)

        fig, ax = plt.subplots()
        ax.scatter(x, y, c=z, s=10, edgecolor='')
        plt.rcParams.update({'font.size':12}) 

        ax.set_title('Grid square within ' + eco_name)
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
        ax.plot(xdata, ycurve, linestyle='-', color='red')
        #adding qout, mse and deg_free to plot
        #ax.annotate('adj_r2 = ' + str(adj_r2[0]), xy=(0.975,0.10), xycoords='axes fraction', fontsize=12, horizontalalignment='right', verticalalignment='bottom')
        ax.annotate('q = ' + str(qout[0]), xy=(0.975,0.15), xycoords='axes fraction', fontsize=12, horizontalalignment='right', verticalalignment='bottom')
        ax.annotate('MSE = ' + str(mse), xy=(0.975,0.10), xycoords='axes fraction', fontsize=12, horizontalalignment='right', verticalalignment='bottom')
        ax.annotate('No of footprints = ' + str(footprints),xy=(0.975,0.05), xycoords='axes fraction', fontsize=12, horizontalalignment='right', verticalalignment='bottom')
        plt.savefig(folderout + 'fig{}_{}.pdf'.format(eco, name))
        plt.close     
          