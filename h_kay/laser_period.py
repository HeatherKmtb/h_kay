#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 16:19:22 2020

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

folderin = '/scratch/a.hek4/eco/forest_vcf_lc_files/'
folderout = '/scratch/a.hek4/eco/ready/'

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
        name = tl.replace('.shp', "")
        
        #year = list(np.unique(df1['year']))
        #datestr = df1['i_acqdate']
        #date=[]
               
        #test3 = test2a[test2a.log_i_h100 >b]
        #final = test3[test3.log_i_h100 <a]       
 
        ph1 = df[df.i_acqdate < 733720]
        
        if ph1.empty == False:          
            ph1.to_file(folderout + '{}.shp'.format(name))
        else:
            print('ph_' + name)