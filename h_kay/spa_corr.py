#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 14:10:19 2020

@author: heatherkay
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn
from libpysal import weights
from esda import Moran, Moran_Local
from shapely.geometry import Polygon
from pysal.lib import cg as geometry
#import splot
#from splot.esda import moran_scatterplot, plot_moran, lisa_cluster

df = gpd.read_file('/Users/heatherkay/q_research/spa_corr/eurasia.shp')

#allow for curvature of the earth in distances
radius = geometry.sphere.RADIUS_EARTH_MILES

#the kernel varies depending on the distance between sentre of polygons
w = weights.distance.Kernel.from_dataframe(df, fixed=False, k=10, radius=radius)

#row standardizes the weights
w.transform ='R'

#can be used to calculate lag and plot your own morans I
#df['w_q'] = weights.lag_spatial(w,df['q'])
y = df['q']
moran = Moran(y,w)
print(moran.I)
print(moran.p_sim)

r2 = df['r_sq']
mor_r2 = Moran(r2,w)
print(mor_r2.I)
print(mor_r2.p_sim)



#get localised
lisa = Moran_Local(y,w)
df['lisa_10']=lisa.Is

lisa_r2 = Moran_Local(r2,w)
df['lisa_r2']=lisa_r2.Is
df.to_file('/Users/heatherkay/q_research/spa_corr/eurasia_10.shp')



#generating your own plot
#standardizing q and w_lag
df['q_std'] = (df['q'] - df['q'].mean())/df['q'].std()
df['w_q'] = weights.lag_spatial(w,df['q'])
df['w_q_std'] = (df['w_q'] - df['w_q'].mean())/df['w_q'].std()

f, ax = plt.subplots(1, figsize=(6, 6))
seaborn.regplot(x='q_std', y='w_q_std', 
                ci=None, data=df, line_kws={'color':'r'})
ax.axvline(0, c='k', alpha=0.5)
ax.axhline(0, c='k', alpha=0.5)
ax.set_title('Moran Plot - % Leave')
plt.show()


#generating weights plot
ax = df.plot(edgecolor='k', facecolor='w')
w.plot(df, ax=ax, 
        edge_kws=dict(color='r', linestyle=':', linewidth=1),
        node_kws=dict(marker=''))
ax.set_axis_off()


#significance of lisa
    #this creates column with true if p<0.05 indicated by a 1
sig = 1 * (lisa.p_sim < 0.05)
df['p-sim_q'] = lisa.p_sim
df['sig'] = sig

df[['sig','p-sim_q']].tail()

    #creating 4 quadrats high hgih, low low etc. from lisa q value
hotspot = 1 * (sig * lisa.q==1)
coldspot = 3 * (sig * lisa.q==3)
doughnut = 2 * (sig * lisa.q==2)
diamond = 4 * (sig * lisa.q==4)
spots = hotspot + coldspot + doughnut + diamond
spot_labels = [ '0 ns', '1 hot spot', '2 doughnut', '3 cold spot', '4 diamond']
labels = [spot_labels[i] for i in spots]
df['labels'] = labels
[(spot_label, (df['labels']==spot_label).sum()) for spot_label in spot_labels]



del df
del w
del y
#del r2
del moran
#del mor_r2
del lisa
del lisa_r2


del coldspot, diamond, doughnut, hotspot, labels, sig, spot_labels, spots
