#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 08:33:57 2023

@author: heatherkay
"""

from scipy import stats as st
import pandas as pd
from statistics import mean, stdev
from math import sqrt

gediin = '/home/heather/q_res/results/all_gedi.csv'
glasin = '/home/heather/q_res/results/glas_23/icesat_results_1deg_23.02.28.csv'

gdf=pd.read_csv(gediin)
idf=pd.read_csv(glasin)

grid = idf['ID']
idf = idf.assign(Grid=grid)

res = gdf.merge(idf, how='inner', on='Grid')
gcd = res['mean_h_g']
icd = res['mean_h']


ttest = st.ttest_ind(a=gcd, b=icd, equal_var=True)

cohens_d = (mean(gcd) - mean(icd)) / (sqrt((stdev(gcd) ** 2 + stdev(icd) ** 2) / 2))
print(cohens_d)

#pearsons r
st.pearsonr(gcd,icd)

import matplotlib.pyplot as plt

plt.hist(gcd, bins = 50)
plt.hist(icd, bins = 50)
