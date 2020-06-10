#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 16:17:54 2020

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

df = gpd.read_file('/Users/heatherkay/q_research/test/help.shp')
w = weights.KNN.from_dataframe(df)
df['w_q'] = weights.lag_spatial(w,df['q'])

#can I remove rows that have no neighbours?
#new = df[df['w_q'].notna()]

#weights relationship based on distance
w_kernel = weights.distance.Kernel.from_dataframe(df)


#the kernel varies depending on the distance between sentre of polygons
w_adaptive = weights.distance.Kernel.from_dataframe(df, fixed=False, k=15)
w_adaptive.bandwidth

#but need to take curvature of the eart into account
radius = geometry.sphere.RADIUS_EARTH_MILES
w_radius_knn = weights.distance.KNN.from_dataframe(df, k=4, radius=radius)

#gives each polygon 16 weighted neighbours
w_adaptive = weights.distance.Kernel.from_dataframe(df, fixed=False, k=15, radius=radius)  

y = df['q']
moran = Moran(y,w)
print(moran.I)

#generating your own plot
#standardizing q and w_lag

df['q_std'] = (df['q'] - df['q'].mean())/df['q'].std()
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

