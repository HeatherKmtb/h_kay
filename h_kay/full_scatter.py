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
    a = np.quantile(test2a['log_i_h100'],0.95)
    b = np.quantile(test2a['log_i_h100'],0.05)

    #remove data outside of 5% quantiles
    test3 = test2a[test2a.log_i_h100 >b]
    final = test3[test3.log_i_h100 <a]

    del a, b, x, y, test2, test2a, test3
    #NEXT STEP. Bin remaining data in order to get mean and IQR of each bin

    #add column with bins 
    final['H_bins']=pd.cut(x=final['i_h100'], bins=np.arange(0, 120+2, 2))

    #now something along the lines of:
    #for bin in HBins find the mean and IQR...
    #first create lists to append mean and IQRs to
    cd_mean = []
    cd_iqr = []
    #Hbin = []

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
    residuals = y - f(x, qout)
    res_ss = np.sum(residuals**2)
    tot_ss = np.sum((y-np.mean(y))**2)
    r_sq = 1- (res_ss/tot_ss)
    deg_free = len(x)
    r_sq = round(r_sq, 2)
#    y_predict = f(x, qout)

    #calculating adjusted r2
    stage1 = (deg_free - 1)/(deg_free - 3)
    stage2 = 1-(1-r_sq)
    adj_r2= stage1 * stage2
    adj_r2 = round(adj_r2, 2)

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
    ax.annotate('q = ' + str(qout[0]), xy=(0.975,0.15), xycoords='axes fraction', fontsize=12, horizontalalignment='right', verticalalignment='bottom')
    ax.annotate(u'R\u0305'u'\u00b2 = ' + str(adj_r2), xy=(0.975,0.10), xycoords='axes fraction', fontsize=12, horizontalalignment='right', verticalalignment='bottom')
    #ax.annotate('r2 = ' + str(r_sq), xy=(0.975,0.10), xycoords='axes fraction', fontsize=9, horizontalalignment='right', verticalalignment='bottom')
    ax.annotate('No of footprints = ' + str(deg_free),xy=(0.975,0.05), xycoords='axes fraction', fontsize=12, horizontalalignment='right', verticalalignment='bottom')   
    plt.savefig(fileout + name + '.pdf')
    plt.close
