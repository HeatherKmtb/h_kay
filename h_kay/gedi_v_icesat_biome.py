#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 31 11:36:34 2023

@author: heather
"""
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import numpy as np
import geopandas

from scipy import stats as st
from statistics import mean, stdev
from math import sqrt
import pandas


join2 = geopandas.read_file('/home/heather/q_res/join_glas_gedi_q.gpkg')

gedi = join2['wwf_grid_id_q'].astype(float)
glas = join2['q'].astype(float)

diff = gedi - glas
new_df = join2.assign(diff = diff)
z=[0, 0.05, 0.1]

fileout = '/home/heather/q_res/results/grid_eco_q_scatter.png'

xy = np.vstack([gedi,glas])
d = gaussian_kde(xy)(xy)

fig, ax = plt.subplots()
ax.scatter(gedi, glas, c=d, s=10)
plt.rcParams.update({'font.size':12}) 
ax.plot(z,z, color='red')
ax.set_xlim([0,0.1])
ax.set_ylim([0,0.1])
ax.set_title('GEDI v ICESat')
ax.set_ylabel('ICESat q values')
ax.set_xlabel('GEDI q values')
plt.savefig(fileout)
plt.close

#q per biome
biomes = list(np.unique(join2['BIOME']))

for biome in biomes:
    df = join2.loc[join2['BIOME']==biome] 
    gedi = df['wwf_grid_id_q'].astype(float)
    glas = df['q'].astype(float)
    fileout = ('/home/heather/q_res/results/gedi_eco/biomes/{}.png'.format(biome))
    xy = np.vstack([gedi,glas])
    d = gaussian_kde(xy)(xy)
    fig, ax = plt.subplots()
    ax.scatter(gedi, glas, c=d, s=10)
    plt.rcParams.update({'font.size':12}) 
    ax.plot(z,z, color='red')
    ax.set_xlim([0,0.1])
    ax.set_ylim([0,0.1])
    ax.set_title('GEDI v ICESat in biome {}'.format(biome))
    ax.set_ylabel('ICESat q values')
    ax.set_xlabel('GEDI q values')
    plt.savefig(fileout)
    plt.close

results = pandas.DataFrame(columns = ['biome', 'ttest', 'cohens', 'pearson'])

for biome in biomes:
    df = join2.loc[join2['BIOME']==biome] 
    gedi = df['wwf_grid_id_q'].astype(float)
    glas = df['q'].astype(float)
    
    #t test (unpaired)
    
    ttest = st.ttest_ind(a=gedi, b=glas, equal_var=True)

    #cohens d
    cohens_d = (mean(gedi) - mean(glas)) / (sqrt((stdev(gedi) ** 2 + stdev(glas) ** 2) / 2))

    #pearsons r
    pearson = st.pearsonr(gedi,glas)
    
    res = pandas.Series([biome, ttest, cohens_d, pearson], index = ['biome', 'ttest', 'cohens', 'pearson'])
    results = pandas.concat([results, res.to_frame().T], ignore_index=True)

    results.to_csv('/home/heather/q_res/results/gedi_eco/biomes/stats.csv')
    
#mse values
rmse = new_df['rmse']
mse = rmse * rmse

new_df2 = new_df.assign(mse = mse)
gedi_mse = new_df2['wwf_grid_id_mse_g'].astype(float)
glas_mse = mse
diff_mse = gedi_mse - glas_mse
new_df3 = new_df2.assign(diff_mse = diff_mse)

fileout = '/home/heather/q_res/results/grid_eco_mse_scatter.png'

xy = np.vstack([gedi_mse,glas_mse])
d = gaussian_kde(xy)(xy)

fig, ax = plt.subplots()
ax.scatter(gedi_mse, glas_mse, c=d, s=10)
plt.rcParams.update({'font.size':12}) 
ax.plot(z,z, color='red')
ax.set_xlim([0,0.1])
ax.set_ylim([0,0.1])
ax.set_title('GEDI v ICESat')
ax.set_ylabel('ICESat mse values')
ax.set_xlabel('GEDI mse values')
plt.savefig(fileout)
plt.close


#mse per biome
biomes = list(np.unique(new_df3['BIOME']))

for biome in biomes:
    df = new_df3.loc[new_df3['BIOME']==biome] 
    gedi = df['wwf_grid_id_mse_g'].astype(float)
    glas = df['mse'].astype(float)
    fileout = ('/home/heather/q_res/results/gedi_eco/biomes/mse/{}.png'.format(biome))
    xy = np.vstack([gedi,glas])
    d = gaussian_kde(xy)(xy)
    fig, ax = plt.subplots()
    ax.scatter(gedi, glas, c=d, s=10)
    plt.rcParams.update({'font.size':12}) 
    ax.plot(z,z, color='red')
    ax.set_xlim([0,0.1])
    ax.set_ylim([0,0.1])
    ax.set_title('GEDI v ICESat in biome {}'.format(biome))
    ax.set_ylabel('ICESat mse values')
    ax.set_xlabel('GEDI mse values')
    plt.savefig(fileout)
    plt.close

results = pandas.DataFrame(columns = ['biome', 'ttest', 'cohens', 'pearson'])

for biome in biomes:
    df = new_df3.loc[new_df3['BIOME']==biome] 
    gedi = df['wwf_grid_id_mse_g'].astype(float)
    glas = df['mse'].astype(float)
    
    #t test (unpaired)
    
    ttest = st.ttest_ind(a=gedi, b=glas, equal_var=True)

    #cohens d
    cohens_d = (mean(gedi) - mean(glas)) / (sqrt((stdev(gedi) ** 2 + stdev(glas) ** 2) / 2))

    #pearsons r
    pearson = st.pearsonr(gedi,glas)
    
    res = pandas.Series([biome, ttest, cohens_d, pearson], index = ['biome', 'ttest', 'cohens', 'pearson'])
    results = pandas.concat([results, res.to_frame().T], ignore_index=True)

    results.to_csv('/home/heather/q_res/results/gedi_eco/biomes/mse/stats.csv')
