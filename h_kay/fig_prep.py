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

gediin = '/Users/heatherkay/q_res/gedi/all_gedi.csv'
glasin = '/Users/heatherkay/q_res/icesat_glas/results_1deg_22.11.18.csv'

gdf=pd.read_csv(gediin)
idf=pd.read_csv(glasin)

res = gdf.merge(idf, how='inner', on='Grid')
gcd = res['mean_cd_g']
icd = res['mean_cd']


ttest = st.ttest_ind(a=gcd, b=icd, equal_var=True)

cohens_d = (mean(gcd) - mean(icd)) / (sqrt((stdev(gcd) ** 2 + stdev(icd) ** 2) / 2))
print(cohens_d)

#pearsons r
st.pearsonr(gcd,icd)