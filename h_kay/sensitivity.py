#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 11:19:11 2020

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




sgr = 0.029249
#q = 0.03
sveg = 0.051003
p1 = 1.55513
p2 = 1.414

#sfor = 0.0509 #can vary between sveg and sgr
alpha = 0.46

#for just a few values of sig_for
fig = plt.figure()
z = np.arange(0.0197, 0.1531, 0.002)
plot = np.zeros_like(z)
sfor_vals = (0.0292, 0.036, 0.044, 0.050)
for sfor in sfor_vals:
    idx=0
    for q in z:
        params = [sgr, q, p1, p2, sveg, sfor, alpha]
        agb = fsolve(func, 10, params)[0]
        plot[idx]=agb
        idx+=1
    x = z
    y = plot
    
    ax = fig.add_subplot(1, 1, 1)
    plt.plot(x,y, label = sfor)

plt.xlabel('q value')
plt.ylabel('AGB')
plt.title('Boreal \nE44, N42')
    
plt.legend()
plt.savefig('/Users/heatherkay/q_res/sensitivity/figs/Boreal_E44_N42_test')
plt.close

#plotting q v AGB - need to plot AGB v sig for - see below...
#for just a few values of sig_for
#with q in biome range
fig = plt.figure()
z = np.arange(0.0197, 0.1531, 0.002)
plot = np.zeros_like(z)
sfor_vals = (0.0292, 0.036, 0.044, 0.050)
for sfor in sfor_vals:
    idx=0
    for q in z:
        params = [sgr, q, p1, p2, sveg, sfor, alpha]
        agb = fsolve(func, 10, params)[0]
        plot[idx]=agb
        idx+=1
    x = z
    y = plot
    
    ax = fig.add_subplot(1, 1, 1)
    plt.plot(x,y, label = sfor)

plt.xlabel('q value')
plt.ylabel('AGB')
plt.title('Boreal \nE44, N42')
    
plt.legend()
plt.savefig('/Users/heatherkay/q_res/sensitivity/figs/Boreal_E44_N42_test')
plt.close
"""
Plot WCM
"""

import matplotlib.pyplot as plt
import numpy as np

# 100 linearly spaced numbers
x = np.linspace(0,500,100)

# the function, which is y = x^2 here
y = sgr*(numpy.exp(-q*(x/p1)**(1/p2))+numpy.exp(-alpha*(x/p1)**(1/p2))-numpy.exp(-(q+alpha)*(x/p1)**(1/p2)))+sveg*(1-numpy.exp(-q*(x/p1)**(1/p2)))

# setting the axes at the centre
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)


# plot the function
plt.plot(x,y)

# show the plot
plt.show()

"""
Other workings
"""
params = [sgr, q, p1, p2, sveg, sfor, alpha]
print("With default parameters:")
print(fsolve(func, 100, params)[0])
print("")

print("Testing q (1):")
print("q: AGB")
for q in [0.071, 0.072, 0.073, 0.074, 0.075, 0.076, 0.077, 0.078, 0.079, 0.080, 0.081, 0.082, 0.083, 0.084]:
    params = [sgr, q, p1, p2, sveg, sfor, alpha]
    agb = fsolve(func, 100, params)[0]
    print("{}: {}".format(q, agb))
print("")

print("Testing q (2):")
print("q: AGB")
for q in [0.0770, 0.0771, 0.0772, 0.0773, 0.0774, 0.0775, 0.0776, 0.0777, 0.0778, 0.0779, 0.0780, 0.0781, 0.0782, 0.0783, 0.0784]:
    params = [sgr, q, p1, p2, sveg, sfor, alpha]
    agb = fsolve(func, 100, params)[0]
    print("{}: {}".format(q, agb))
print("")

#works but not what I want (large df)
results = pd.DataFrame(columns=['sfor','q','AGB'])
for sfor in np.arange(0.0411,0.0509,0.0002):
    
    for q in np.arange(0.0197, 0.1531, 0.002):
        params = [sgr, q, p1, p2, sveg, sfor, alpha]
        agb = fsolve(func, 100, params)[0]
        results = results.append({'sfor':sfor,'q':q,'AGB':agb},ignore_index=True)

results.to_csv('/Users/heatherkay/q_res/test.csv')


#so try plotting direct
fig = plt.figure()
z = np.arange(0.0197, 0.1531, 0.002)
plot = np.zeros_like(z)

for sfor in np.arange(0.0411,0.0509,0.0002):
    idx=0
    for q in z:
        params = [sgr, q, p1, p2, sveg, sfor, alpha]
        agb = fsolve(func, 10, params)[0]
        plot[idx]=agb
        idx+=1
    x = z
    y = plot
    
    ax = fig.add_subplot(1, 1, 1)
    plt.plot(x,y)
    

plt.show()


#so try plotting direct
#this is now plotting AGB v sigma forest with varying q
fig = plt.figure()
z = np.arange(0.0221, 0.0584, 0.0002)
plot = np.zeros_like(z)

for q in np.arange(0.0197,0.1531,0.02):
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
    

plt.show()




