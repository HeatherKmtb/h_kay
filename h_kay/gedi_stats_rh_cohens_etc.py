#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 13:48:13 2023

@author: heather
"""

import os.path
import geopandas as gpd
import pandas
import matplotlib.pyplot as plt
from statistics import mean, stdev
from math import sqrt
from scipy import stats as st
import numpy as np
from scipy.stats import gaussian_kde

out_dir = '/home/heather/q_res/gedi/test/'
gedi_file = '/home/heather/q_res/gedi/7_NA.gpkg'
df = gpd.read_file(gedi_file)

df_quality = df[df.quality_flag != 0]

rh98 = df_quality['rh_98']
rh100 = df_quality['rh_100']

hd, tl = os.path.split(gedi_file)
shp_lyr_name = os.path.splitext(tl)[0]
name_comp = shp_lyr_name.split('_')
biome = name_comp[0] 
realm = name_comp[1]


results2 = pandas.DataFrame(columns = ['height', 'cohens', 'diff_means'])

x = [10, 12, 14, 15, 16, 18, 20, 30, 40, 50, 100]

for i in x:
    height = i
    df_10 = df_quality[df_quality['rh_100']>=i]
    rh98 = df_10['rh_98']
    rh100 = df_10['rh_100']

    m_rh100 = mean(rh100)
    m_rh98 = mean(rh98)
    diff_means = m_rh100- m_rh98
    #cohens d
    cohens_d = (mean(rh100) - mean(rh98)) / (sqrt((stdev(rh100) ** 2 + stdev(rh98) ** 2) / 2))
      
    res2 = pandas.Series([height, cohens_d, diff_means], index = ['height', 'cohens', 'diff_means'])
    results2 = pandas.concat([results2, res2.to_frame().T], ignore_index=True)

    results2.to_csv(out_dir + 'cohens_greater_than.csv')  





xy = np.vstack([rh98,rh100])
z = gaussian_kde(xy)(xy)

fig, ax = plt.subplots()
ax.scatter(rh98, rh100, c=z, s=10)
plt.rcParams.update({'font.size':12}) 

ax.set_title('RH98 v RH100 in ' + biome + ' ' + realm)
ax.set_ylabel('RH100 (m)')
ax.set_xlabel('RH98 (m)')
#ax.set_xlim([0, 60])
#ax.set_ylim([0,1])
plt.savefig(out_dir + '{}_{}_scatter.png'.format(biome, realm))
plt.close 

df_20 = df_quality[df_quality['rh_98']<=20]
rh98 = df_20['rh_98']
rh100 = df_20['rh_100']

xy = np.vstack([rh98,rh100])
z = gaussian_kde(xy)(xy)


#boxplot
box_df = df_20[['rh_98','rh_100']]
plt.boxplot(box_df)
plt.xticks([1,2], ['RH98','RH100'])
plt.savefig(out_dir + '{}_{}_20m_box.png'.format(biome, realm))
plt.close

ttest = st.ttest_ind(a=rh98, b=rh100, equal_var=True)

#cohens d
cohens_d = (mean(rh100) - mean(rh98)) / (sqrt((stdev(rh100) ** 2 + stdev(rh98) ** 2) / 2))
        
#pearsons r
pearson = st.pearsonr(rh100,rh98)
    
results = pandas.DataFrame(columns = ['biome', 'realm', 'ttest', 'cohens', 'pearson'])
res = pandas.Series([biome, realm, ttest, cohens_d, pearson], index = ['biome', 'realm', 'ttest', 'cohens', 'pearson'])
results = pandas.concat([results, res.to_frame().T], ignore_index=True)

results.to_csv(out_dir + '{}_{}_10m.csv'.format(biome, realm))        

fig, ax = plt.subplots()
ax.scatter(rh98, rh100, c=z, s=10)
plt.rcParams.update({'font.size':12}) 

ax.set_title('RH98 v RH100 in ' + biome + ' ' + realm)
ax.set_ylabel('RH100 (m)')
ax.set_xlabel('RH98 (m)')
#ax.set_xlim([0, 60])
#ax.set_ylim([0,1])
plt.savefig(out_dir + '{}_{}_10m_scatter.png'.format(biome, realm))
plt.close 



#histogram

bins = 30

plt.hist(rh98, bins, alpha=0.5, label='rh98')
plt.hist(rh100, bins, alpha=0.5, label='rh100')
plt.legend(loc='upper right')
plt.show()


#get quantiles
a = np.quantile(df_20['rh_100'],0.95)
        #b = np.quantile(test2a['log_i_h100'],0.05)

#remove data outside of 5% quantiles
df_20q95= df_20[df_20.rh_100 <a]
        #final = test3[test3.log_i_h100 <a]

#boxplot
box_df = df_20q95[['rh_98','rh_100']]
plt.boxplot(box_df)
plt.xticks([1,2], ['RH98','RH100'])
plt.savefig(out_dir + '{}_{}_20m_q95_box.png'.format(biome, realm))
plt.close

ttest = st.ttest_ind(a=rh98, b=rh100, equal_var=True)

#cohens d
cohens_d = (mean(rh100) - mean(rh98)) / (sqrt((stdev(rh100) ** 2 + stdev(rh98) ** 2) / 2))
        
#pearsons r
pearson = st.pearsonr(rh100,rh98)
    
results = pandas.DataFrame(columns = ['biome', 'realm', 'ttest', 'cohens', 'pearson'])
res = pandas.Series([biome, realm, ttest, cohens_d, pearson], index = ['biome', 'realm', 'ttest', 'cohens', 'pearson'])
results = pandas.concat([results, res.to_frame().T], ignore_index=True)

results.to_csv(out_dir + '{}_{}_20m_q95.csv'.format(biome, realm))        

fig, ax = plt.subplots()
ax.scatter(rh98, rh100, c=z, s=10)
plt.rcParams.update({'font.size':12}) 

ax.set_title('RH98 v RH100 in ' + biome + ' ' + realm)
ax.set_ylabel('RH100 (m)')
ax.set_xlabel('RH98 (m)')
#ax.set_xlim([0, 60])
#ax.set_ylim([0,1])
plt.savefig(out_dir + '{}_{}_20m_q95_scatter.png'.format(biome, realm))
plt.close 





