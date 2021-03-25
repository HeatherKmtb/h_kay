#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 09:01:44 2021

@author: heatherkay
"""

import matplotlib.pyplot as plt
from scipy.optimize import fsolve
import numpy as np
import pandas as pd

#solution for mutliplots can be found at bottom of this script, all the rest 
#is just working things out but worth maybe keeping for now. 



def func(x, args):
    sgr = args[0]#0.04114
    q = args[1]#0.077673
    p1= args[2]#4.79914
    p2= args[3]#1.0158
    sveg = args[4]#0.052059
    sfor = args[5]#0.0509 #can vary between sveg and sgr
    alpha = args[6]#0.46
    return sgr*(np.exp(-q*(x/p1)**(1/p2))+np.exp(-alpha*(x/p1)**(1/p2))-np.exp(-(q+alpha)*(x/p1)**(1/p2)))+sveg*(1-np.exp(-q*(x/p1)**(1/p2)))-sfor

sgr = 0.0221
#q = 0.03
sveg = 0.0583
p1 = 3.7941
p2 = 1.6272
#alpha remains constant
alpha = 0.46

fig = plt.figure()
#z is sfor: between sveg and sgr
z = np.arange(0.0221, 0.0583, 0.0002)
plot = np.zeros_like(z)

#calculating q value range
q_orig = 0.084
sdq = 0.0010
q_min = q_orig - (sdq*2)
q_max = q_orig + (sdq*2)

qs=[q_min, q_orig, q_max]

#plotting
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
    #ax.set_xlim([0,1000])
    ax.set_xlabel = 'AGB'
    ax.set_ylabel = 'Sigma_for'
    plt.plot(x,y)
    

plt.show()
plt.savefig('/Users/heatherkay/q_res/sensitivity/figs/E-70_N-5')
