#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 15:48:18 2020

@author: heatherkay
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 10:30:30 2019

@author: heatherkay
"""


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import numpy as np
import numpy.polynomial.polynomial as poly
import glob


def lin_regress(filein, fileout, xdata, ydata, xax, yax, title, point_style='.', point_col='blue', line_col='black'):
    """
    Function to plot linear regression with r2 value
    
    Parameters
    ----------
    filein: string
          Filepath for csv with data to plot
          
    fileout: string
           Filepath for location to save plot   
           
    xdata: string
         Title of column containing data on x axis   
         
    ydata: string
         Title of column containing data on y axis   
         
    xax: string
       X axis label
       
    yax: string
       Y axis label  
       
    title: string
         Plot title
         
    point_style: string
               Style of plotted points see matplotlib for options.
               Defaut = '.'
               
    point_col: string           
             Colour of plotted points.
             Default = 'blue'
             
    line_col: string           
             Colour of regression line.
             Default = 'black'             
    """
    df = pd.read_csv(filein)

    #defining x and y data
    x1 = df[xdata]
    y1 = df[ydata]
 
    #getting regression and plotting data and lines
    r1_z = np.polyfit(x1,y1,1)
    r1_p = np.poly1d(r1_z)  
  
    #obtaining r2 values
    y1hat = r1_p(x1)
    y1bar = np.sum(y1)/len(y1)
    ssreg1 = np.sum((y1hat-y1bar)**2)
    sstot1 = np.sum((y1-y1bar)**2)
    r1_r2 = ssreg1/sstot1


    fig = pylab.plot(x1,y1,point_style,c=point_col)
    fig = pylab.plot(x1,r1_p(x1),c=line_col)


    plt.title(title)
    plt.ylabel(xax)
    plt.xlabel(yax)

    plt.legend(loc=2, fontsize='x-small')

    plt.annotate('y=0.93x + 0.0015  r2='+str(r1_r2.round(2)), xy=(0.975,0.05), xycoords='axes fraction', fontsize=7, horizontalalignment='right', verticalalignment='bottom')

    plt.savefig(fileout)
    plt.close


