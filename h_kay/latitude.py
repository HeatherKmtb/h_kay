#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 13:21:43 2020

@author: heatherkay
"""

import numpy as np
import mpl_scatter_density
import matplotlib.pyplot as plt
import pandas as pd

filein = '/Users/heatherkay/q_res/biomes/with_b&r_noduplicates.csv'

df = pd.read_csv(filein)

#get grid square nubers   
df['join']=df['join'].astype(str)
grid=df['join'].str[6:11]
grid.astype(str).astype(float)

grid2=int(grid)
df['grid']=grid

#divide into rows of grid squares and get mean and IQR
df['grid_bins']=pd.cut(x=df['grid'], bins=np.arange(0, 53500, 350))
q_mean = []
q_iqr = []

GBins = list(np.unique(df['grid_bins']))
for bins in GBins:
    #for each one make a df with just that bin
    new = final.loc[final['H_bins']==bins]
    #get mean and IQR of each bin
    data = df['q'].to_numpy()
    mean = data.mean()
    q_mean.append(mean)
    q75, q25 = np.percentile (data, [75, 25])
    iqr = q75 - q25
    q_iqr.append(iqr)
    
