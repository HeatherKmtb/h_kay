#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 11:32:46 2020

@author: heatherkay
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 10:32:19 2019

@author: heatherkay
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 10:41:03 2019

@author: heatherkay
"""


#import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from pandas import DataFrame
from scipy.optimize import curve_fit
import geopandas as gpd
#import glob
#from os import path



def full_scatter(filein, name, fileout):
    """
    A function to plot all the points and the regression
    
    Parameters
    ----------
    filein: string
          filepath for shapefile to analyse
 
    name: string
          plot title
          
    fileout: string
           filepath for folder to save plot (filename is plot title)
    """

    df = gpd.read_file(filein)

    #name2 = eco_ID[name] 
    #remove data with H_100 >= 0 prior to logging
    test2 = df[df['i_h100']>=0] 
    
    #means x is just the h100 data - needs logging to normalise (not skewed) 
    x = test2['i_h100']
    
    #create new column in df with log of H_100 
    y = np.log(x)
    test2a = test2.assign(log_i_h100 = y)

    #get quantiles
    a = np.quantile(test2a['log_i_h100'],0.99)
    b = np.quantile(test2a['log_i_h100'],0.01)

    #remove data outside of 5% quantiles
    test3 = test2a[test2a.log_i_h100 >b]
    final = test3[test3.log_i_h100 <a]

    del a, b, x, y, test2, test2a, test3
            
    #regression 
    def f(x,q):
        return 1- np.exp(-q * x)
    
    x = final['i_h100'].to_numpy()
    y = final['i_cd'].to_numpy() 
        
    qout, qcov = curve_fit(f, x, y, 0.04)
    qout = qout.round(decimals=4)
    #calculating r2
    residuals = y - f(x, qout)
    res_ss = np.sum(residuals**2)
    tot_ss = np.sum((y-np.mean(y))**2)
    r_sq = 1- (res_ss/tot_ss)
    deg_free = (len(x)-1)
    r_sq = round(r_sq, 2)
#    y_predict = f(x, qout)

    fig = plt.figure(); ax = fig.add_subplot(1,1,1)
    plt.rcParams.update({'font.size':12})
    #plots H_100 on x with I_CD on y
    ax.scatter(x,y,marker='.')
    #plots IQR
    #ax.bar(plot['median'],plot['mean'],width=0, yerr=plot['iqr'])
    #sets title and axis labels
    ax.set_title(name)
    ax.set_ylabel('Canopy Density')
    ax.set_xlabel('Height - h100')
    ax.set_xlim([0, 60])
    ax.set_ylim([0,1])
    #plotting regression
    #putting x data in an order, cause that's what the code needs
    xdata = np.linspace(min(x), max(x))
    #for each value of x calculating the corresponding y value
    ycurve = [f(t, qout) for t in xdata]
    #plotting the curve
    ax.plot(xdata, ycurve, linestyle='-', c='red')
    #adding qout, r_sq and deg_free to plot
    ax.annotate('q = ' + str(qout[0]), xy=(0.975,0.15), xycoords='axes fraction', fontsize=9, horizontalalignment='right', verticalalignment='bottom')
    ax.annotate('r2 = ' + str(r_sq), xy=(0.975,0.10), xycoords='axes fraction', fontsize=9, horizontalalignment='right', verticalalignment='bottom')
    ax.annotate('degrees of freedom = ' + str(deg_free),xy=(0.975,0.05), xycoords='axes fraction', fontsize=9, horizontalalignment='right', verticalalignment='bottom')   
    plt.savefig(fileout + name + '.pdf')
    plt.close
