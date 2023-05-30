#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 08:17:18 2023

@author: heatherkay
"""

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean, stdev
from math import sqrt
import scipy.stats

df1 = gpd.read_file('/Users/heatherkay/q_res/GEDI02_A_2020181231348_O08768_03_T05029_02_003_01_V002.gpkg',layer = 'BEAM0101')
df2 = gpd.read_file('/Users/heatherkay/q_res/GEDI02_A_2020181231348_O08768_03_T05029_02_003_01_V002.gpkg',layer = 'BEAM0110')
df3 = gpd.read_file('/Users/heatherkay/q_res/GEDI02_A_2020181231348_O08768_03_T05029_02_003_01_V002.gpkg',layer = 'BEAM1000')
df4 = gpd.read_file('/Users/heatherkay/q_res/GEDI02_A_2020181231348_O08768_03_T05029_02_003_01_V002.gpkg',layer = 'BEAM1011')

dfList = [df1, df2, df3, df4]

df = pd.concat(dfList) 

df_quality = df[df.quality_flag != 0]

rh98 = df_quality['rh_98']
rh100 = df_quality['rh_100']

#t test (unpaired)
from scipy import stats as st
st.ttest_ind(a=rh98, b=rh100, equal_var=True)

#cohens d
cohens_d = (mean(rh98) - mean(rh100)) / (sqrt((stdev(rh98) ** 2 + stdev(rh100) ** 2) / 2))
print(cohens_d)

#pearsons r
scipy.stats.pearsonr(rh98,rh100)

#scatterplot
fig, ax = plt.subplots()
ax.scatter(rh98, rh100, s=10)

#ax.set_xlim([0,40])
#ax.set_ylim([0,40])
ax.set_title('RH98 v RH100')
ax.set_ylabel('RH100 (m)')
ax.set_xlabel('RH98 (m)')
plt.savefig('/Users/heatherkay/q_res/gedi/results/rh98_investigation/test_rh.png')
plt.close

#densityplot
import numpy as np
from scipy.stats import gaussian_kde

xy = np.vstack([rh98,rh100])
z = gaussian_kde(xy)(xy)

fig, ax = plt.subplots()
ax.scatter(rh98, rh100, c=z, s=10)
plt.rcParams.update({'font.size':12}) 

ax.set_title('RH98 v RH100')
ax.set_ylabel('RH100 (m)')
ax.set_xlabel('RH98 (m)')
        #ax.set_xlim([0, 60])
        #ax.set_ylim([0,1])
plt.savefig('/Users/heatherkay/q_res/gedi/results/rh98_investigation/test_rh_density.png')
plt.close 



#boxplot
box_df = df_quality[['rh_98','rh_100']]
plt.boxplot(box_df)
plt.xticks([1,2], ['RH98','RH100'])
plt.savefig('/Users/heatherkay/q_res/test_rh_box.png')

#boxplots per height range
fig = plt.figure()
box5df= box_df[box_df['rh_98']>=5]
box5to10df = box5df[box5df['rh_98']<=10]
plt.boxplot(box5to10df)
plt.xticks([1,2], ['RH98','RH100'])
plt.title('Height range 5-10m')
plt.savefig('/Users/heatherkay/q_res/gedi/results/rh98_investigation/test_rh_box_5-10.png')
plt.close

fig = plt.figure()
box10df= box_df[box_df['rh_98']>=10]
box10to15df = box10df[box10df['rh_98']<=15]
plt.boxplot(box10to15df)
plt.xticks([1,2], ['RH98','RH100'])
plt.title('Height range 10-15m')
plt.savefig('/Users/heatherkay/q_res/gedi/results/rh98_investigation/test_rh_box_10-15.png')
plt.close

fig = plt.figure()
box15df= box_df[box_df['rh_98']>=15]
box15to20df = box15df[box15df['rh_98']<=20]
plt.boxplot(box15to20df)
plt.xticks([1,2], ['RH98','RH100'])
plt.title('Height range 15-20m')
plt.savefig('/Users/heatherkay/q_res/gedi/results/rh98_investigation/test_rh_box_15-20.png')
plt.close

fig = plt.figure()
box20df= box_df[box_df['rh_98']>=20]
box20to30df = box20df[box20df['rh_98']<=30]
plt.boxplot(box5to10df)
plt.xticks([1,2], ['RH98','RH100'])
plt.title('Height range 20-30m')
plt.savefig('/Users/heatherkay/q_res/gedi/results/rh98_investigation/test_rh_box_20-30.png')
plt.close

fig = plt.figure()
box30df= box_df[box_df['rh_98']>=30]
box30to40df = box30df[box30df['rh_98']<=40]
plt.boxplot(box30to40df)
plt.xticks([1,2], ['RH98','RH100'])
plt.title('Height range 30-40m')
plt.savefig('/Users/heatherkay/q_res/gedi/results/rh98_investigation/test_rh_box_30-40.png')
plt.close

fig = plt.figure()
box5df= box_df[box_df['rh_98']<=5]
plt.boxplot(box5df)
plt.xticks([1,2], ['RH98','RH100'])
plt.title('Height range <5m')
plt.savefig('/Users/heatherkay/q_res/gedi/results/rh98_investigation/test_rh_box_under_5.png')
plt.close

fig = plt.figure()
box40df= box_df[box_df['rh_98']>=40]
plt.boxplot(box40df)
plt.xticks([1,2], ['RH98','RH100'])
plt.title('Height range >40m')
plt.savefig('/Users/heatherkay/q_res/gedi/results/rh98_investigation/test_rh_box_over_40.png')
plt.close
