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
import geopandas as gpd

gediin = '/Users/heatherkay/q_res/gedi/results/grid_eco_05.23/wwf_grid.csv'
gedi10in = '/Users/heatherkay/q_res/gedi/results/grid_eco_05.23/wwf_grid_10m.csv'
gedi12in = '/Users/heatherkay/q_res/gedi/results/grid_eco_05.23/wwf_grid_12m.csv'


df = pd.read_csv(gediin)
df10 = pd.read_csv(gedi10in) 
df12 = pd.read_csv(gedi12in) 

cols = ['qout_gedi', 'deg_free_g', 'mse_g', 'mean_h_g',
       'mean_cd_g', 'max_h_g']

for col in cols:
    df = df.rename(columns={col:col + '_0m'})
    df10 = df10.rename(columns={col:col + '_10m'})
    df12 = df12.rename(columns={col:col + '_12m'})
    
# new_id = 'gedi_' + df['Grid'].astype(str) + '_' + df['eco'].astype(str)
# df = df.assign(poly_id = new_id)

# new_id = 'gedi_' + df10['Grid'].astype(str) + '_' + df10['eco'].astype(str)
# df10 = df10.assign(poly_id = new_id)

new_id = 'gedi_' + df12['Grid'].astype(str) + '_' + df12['eco'].astype(str)
df12 = df12.assign(poly_id = new_id)



df1_join = df.merge(df10, how='inner', on = 'poly_id')
df_join = df1_join.merge(df12, how='inner', on = 'poly_id')
df_join = df_join.drop_duplicates('poly_id')


fq = df_join['qout_gedi_0m'] = df_join.qout_gedi_0m.astype(str)
fq10 = df_join['qout_gedi_10m'] = df_join.qout_gedi_10m.astype(str)
fq12 = df_join['qout_gedi_12m'] = df_join.qout_gedi_12m.astype(str)

q = fq.str.strip('[]').astype(float)
q10 = fq10.str.strip('[]').astype(float)
q12 = fq12.str.strip('[]').astype(float)

df_join = df_join.assign(qout_0m = q)
df_join = df_join.assign(qout_10m = q10)
df_join = df_join.assign(qout_12m = q12)

z=[0, 0.05, 0.1]

x = df_join['qout_0m']
y = df_join['qout_10m']
fileout = '/Users/heatherkay/q_res/gedi/results/grid_eco_05.23/scatter_10m.png'

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



#and the icesat data

df_glas = gpd.read_file('/Users/heatherkay/q_res/icesat_glas/Final_q/final_q_gridded.gpkg')

name_comp = df_glas['join']

eco=[]
for i in name_comp: 
    join = i.split('_')
    name = join[0] 
    eco.append(name)
    
grid = df_glas['tile_name']    
poly_id_glas = grid + '_' + eco

df_glas_new = df_glas.assign(poly_id = poly_id_glas)
df_glas_new = df_glas_new.drop_duplicates('poly_id')

all_data = df_join.merge(df_glas_new, how='inner', on = 'poly_id')

y = all_data['q']
x = all_data['qout_10m']
fileout = '/Users/heatherkay/q_res/gedi/results/grid_eco_05.23/scatter_10mvglas.png'

fig, ax = plt.subplots()
ax.scatter(x, y, s=10)
ax.plot(z,z, color='red')
ax.set_xlim([0,0.1])
ax.set_ylim([0,0.1])
ax.set_title('GLAS v GEDI 10m')
ax.set_xlabel('GEDI q values with footprints with rh100<10m removed')
ax.set_ylabel('GLAS q values')
plt.savefig(fileout)
plt.close

