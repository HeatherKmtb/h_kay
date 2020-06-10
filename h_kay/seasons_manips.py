#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 11:18:07 2020

@author: heatherkay
"""

import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
from scipy.optimize import curve_fit
import geopandas as gpd
import glob
from os import path
import pandas as pd


def get_realms_rmv_brackets(filein, folderout, q_col='qout', realm_col='eco', 
                            colNms=['eco','ID','date','qout','r_sq','deg_free',
                                    'rmse','q']):
    #remove brackets and convert to float
    df3 = pd.read_csv(filein)

    df1 = df3[q_col] = df3.q_col.astype(str)
    df2 = df1.str.strip('[]').astype(float)

    df = df3.assign(q = df2)
    #get realms
    df[realm_col]=df[realm_col].astype(str)
    realm=df[realm_col].str[:1]
    #biome=df['ECO_ID'].str[1:3]
    df['realm'] = realm
    #df['biome'] = biome
    
    dfrealm = df[[colNms]].copy()
    #dfbiome = df[['biome','q_summer','q_winter','eco_x','ID','deg_free_x','deg_free_y']].copy()

    #biomes = list(np.unique(dfbiome['biome']))
    realms = list(np.unique(dfrealm['realm']))

    #for b in biomes:
        #new = dfbiome.loc[dfbiome['biome']==b]
        #new.to_csv('/Users/heatherkay/Desktop/MPhil/ecoregions/seasonality/exploration_csvs/biome/{}.csv'.format(b))
    
    for r in realms:
        new = dfrealm.loc[dfrealm['realm']==r]    
        new.to_csv(folderout + '{}.csv'.format(r))
        
def obtain_means(folderin, fileout, cols=['realm', 'month', 'q', 'r_sq']):
    #using 'file' to title plot  
    fileList = glob.glob(folderin + '*.csv')
    
    #create df for results
    means = pd.DataFrame(columns = cols)

    for file in fileList:
        #split file path into start and end, use tl to get end
        hd, tl = path.split(file)
        realm = tl.replace('.csv',"")

        df = gpd.read_file(file)
    
        months = list(np.unique(df['date']))
        for m in months:
            meanq = df['q'].mean()
            meanr2 = df['r_sq'].mean()
    
            means = means.append({'realm': realm , 'month': m, 'q': meanq, 'r_sq': meanr2}, ignore_index=True)
            #export to excel
        
    means.to_csv(fileout)
    
def plot_means(filein, fileout):
    df = pd.read_csv(filein)


    y1 = df['q'].where(df['realm']=='1')
    x1 = df['month'].where(df['realm']=='1')
    y2 = df['q'].where(df['realm']=='5')
    x2 = df['month'].where(df['realm']=='5')
    y3 = df['q'].where(df['realm']=='6')
    x3 = df['month'].where(df['realm']=='6')
    y4 = df['q'].where(df['realm']=='8')
    x4 = df['month'].where(df['realm']=='8')        


    fig = plt.figure(); ax = fig.add_subplot(1,1,1)
    plt.rcParams.update({'font.size':12})
    #plots H_100 on x with I_CD on y
    ax.scatter(x1,y1,marker='.', c='green')
    ax.scatter(x2,y2,marker='.',c='red')  
    ax.scatter(x3,y3,marker='.',c='blue')
    ax.scatter(x4,y4,marker='.',c='black')
    ax.plot(x1,y1,c='green')
    ax.plot(x2,y2,c='red')  
    ax.plot(x3,y3,c='blue')
    ax.plot(x4,y4,c='black')
    #plots IQR
    #ax.bar(plot['median'],plot['mean'],width=0, yerr=plot['iqr'])
    #sets title and axis labels
    ax.set_title('monthly mean q values per realm')
    ax.set_ylabel('q_value')
    ax.set_xlabel('month')
    #plt.legend(loc=2, fontsize='x-small')
    #ax.set_xlim([0, 60])
    #ax.set_ylim([0,1])
    #plotting regression
    #putting x data in an order, cause that's what the code needs
    #xdata = np.linspace(min(x), max(x))
    #for each value of x calculating the corresponding y value
    #ycurve = [f(t, qout) for t in xdata]
    #plotting the curve
    #ax.plot(xdata, ycurve, linestyle='-', c='green')
    #adding qout, r_sq and deg_free to plot
    #ax.annotate('q = ' + str(qout[0]), xy=(0.975,0.15), xycoords='axes fraction', fontsize=9, horizontalalignment='right', verticalalignment='bottom')
    #ax.annotate('r2 = ' + str(r_sq), xy=(0.975,0.10), xycoords='axes fraction', fontsize=9, horizontalalignment='right', verticalalignment='bottom')
    #ax.annotate('degrees of freedom = ' + str(deg_free),xy=(0.975,0.05), xycoords='axes fraction', fontsize=9, horizontalalignment='right', verticalalignment='bottom')   
    plt.savefig(fileout + '.pdf')
    plt.close
    