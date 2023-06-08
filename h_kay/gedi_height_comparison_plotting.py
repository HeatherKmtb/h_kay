#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 13:46:37 2023

@author: heather
"""

import pandas as pd
import matplotlib.pyplot as plt
from os import path
import numpy as np

gediin = '/home/heather/q_res/results/gedi_eco/wwf_grid.csv'
gedi10in = '/home/heather/q_res/results/gedi_eco/wwf_grid_10m.csv'
gedi12in = '/home/heather/q_res/results/gedi_eco/wwf_grid_12m.csv'


df = pd.read_csv(gediin)
df10 = pd.read_csv(gedi10in) 
df12 = pd.read_csv(gedi12in) 

df10 = df10.rename(columns={'qout_gedi':'qout_10m'})
df12 = df12.rename(columns={'qout_gedi':'qout_12m'})

df1_join = df.merge(df10, how='inner', on = 'Grid')
df_join = df1_join.merge(df12, how='inner', on = 'Grid')
df_join = df_join.drop_duplicates('Grid')


fq = df_join['qout_gedi'] = df_join.qout_gedi.astype(str)
fq10 = df_join['qout_10m'] = df_join.qout_gedi.astype(str)
fq12 = df_join['qout_12m'] = df_join.qout_gedi.astype(str)

q = fq.str.strip('[]').astype(float)
q10 = fq10.str.strip('[]').astype(float)
q12 = fq12.str.strip('[]').astype(float)

df_join = df_join.assign(qout_gedi = q)
df_join = df_join.assign(qout_10m = q10)
df_join = df_join.assign(qout_12m = q12)

z=[0, 0.05, 0.1]

x = df_join['qout_gedi']
y = df_join['qout_10m']
fileout = '/home/heather/q_res/results/gedi_eco/scatter_10m.png'

fig, ax = plt.subplots()
ax.scatter(x, y, s=10)
ax.plot(z,z, color='red')
ax.set_xlim([0,0.1])
ax.set_ylim([0,0.1])
ax.set_title('GEDI v GEDI 10m')
ax.set_ylabel('GEDI q values with footprints with rh100<10m removed')
ax.set_xlabel('GEDI q values')
plt.savefig(fileout)
plt.close

