#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 14:28:09 2021

@author: heatherkay
"""

import matplotlib.pyplot as plt
from scipy.optimize import fsolve
import numpy as np
import pandas as pd

filein = '/Users/heatherkay/q_res/sensitivity/grid_squares_s1_20200704.csv'

df = pd.read_csv(filein)

def func(x, args):
    sgr = args[0]#0.04114
    q = args[1]#0.077673
    p1= args[2]#4.79914
    p2= args[3]#1.0158
    sveg = args[4]#0.052059
    sfor = args[5]#0.0509 #can vary between sveg and sgr
    alpha = args[6]#0.46
    return sgr*(np.exp(-q*(x/p1)**(1/p2))+np.exp(-alpha*(x/p1)**(1/p2))-np.exp(-(q+alpha)*(x/p1)**(1/p2)))+sveg*(1-np.exp(-q*(x/p1)**(1/p2)))-sfor

for i, row in df.iterrows():
    E = row['Easting']
    N = row['Northing']
    sgr = row['Sigma_ground']
    sveg = row['Sigma_veg']
    p1 = row['p1']
    p2 = row['p2']
    alpha = 0.46
    q= row['my_q']
    sdq = row['std']
    q_min = q - (sdq*2)
    q_max = q + (sdq*2)
    qs=[q_min, q, q_max]
    
    fig = plt.figure()
    #z is sfor: between sveg and sgr
    z = np.arange(sgr, sveg, 0.0002)
    plot = np.zeros_like(z)
    
    for q in qs:
        idx=0
        for sfor in z:
            params = [sgr, q, p1, p2, sveg, sfor, alpha]
            agb = fsolve(func, 10, params)[0]
            plot[idx]=agb
            idx+=1
        x = plot
        y = z
    
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlim([0,1000])
        ax.set_xlabel = 'AGB'
        ax.set_ylabel = 'Sigma_for'
        plt.plot(x,y)
    
        plt.savefig('/Users/heatherkay/q_res/sensitivity/figs/E{}_N{}.pdf'.format(E,N))
        plt.close
   
