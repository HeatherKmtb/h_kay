#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 14:04:38 2020

@author: heatherkay
"""


import pandas as pd
import numpy as np
import glob
from os import path

import matplotlib.pyplot as plt
import seaborn

import scipy.stats as stats

def biomes_and_realms(filein, folderout):

    df = pd.read_csv(filein)

    df['join']=df['join'].astype(str)
    realm=df['join'].str[:1]
    biome=df['join'].str[1:3]
    df['realm'] = realm
    df['biome'] = biome
    

    biomes = list(np.unique(df['biome']))
    realms = list(np.unique(df['realm']))

    
    for b in biomes:
        new = df.loc[df['biome']==b] 
        
        new.to_csv(folderout + 'biome_{}.csv'.format(b))

    for r in realms:
        new = df.loc[df['realm']==r]    
        new.to_csv(folderout + 'realm_{}.csv'.format(r))
        
def anova(filein):
    df = pd.read_csv(filein)

    df['join']=df['join'].astype(str)
    realm=df['join'].str[:1]
    biome=df['join'].str[1:3]
    df['realm'] = realm
    df['biome'] = biome
    df.drop_duplicates(subset ='join', 
                     keep = False, inplace = True)    
    #biomes = list(np.unique(df['biome']))
         
    stats.f_oneway(df['q'][df['realm'] == '1'],df['q'][df['realm'] == '8'])      
    

def hist_seaborn_realm(filein, folderout, column, xlab, ylab, title):
    """
    Function to plot histogram with seaborn
    
    Parameters
    ----------
    filein: string
          Filepath for dataframe to use for plotting
          
    fileout: string
           Filepath to save plot
           
    column: string
          Name of column with data for histogram
          
    xlab: string
        x axis label
        
    ylab: string
        y axis label  
        
    title: string    
         title for plot
    """
    filein = '/Users/heatherkay/q_res/biomes/with_b&r_noduplicates.csv'
    folderout = '/Users/heatherkay/q_res/biomes/plots/'
    df = pd.read_csv(filein)
    df['join']=df['join'].astype(str)
    realm=df['join'].str[:1]
    biome=df['join'].str[1:3]
    df['realm'] = realm
    df['biome'] = biome
    df.drop_duplicates(subset ='join', 
                     keep = False, inplace = True) 
    
    df['realm']=df['realm'].astype(str)
    #biomes = list(np.unique(df['biome']))
    #realms = list(np.unique(df['realm']))    
    
    df01 = df.loc[df['realm']== '1']
    df02 = df.loc[df['realm']== '2']
    df03 = df.loc[df['realm']== '3']
    df04 = df.loc[df['realm']== '4']
    df05 = df.loc[df['realm']== '5']
    df06 = df.loc[df['realm']== '6']    
    df07 = df.loc[df['realm']== '7']
    df08 = df.loc[df['realm']== '8']


    plot01 = df01[column]
    plot02 = df02[column]
    plot03 = df03[column]
    plot04 = df04[column]
    plot05 = df05[column]
    plot06 = df06[column]
    plot07 = df07[column]
    plot08 = df08[column]


    
    fig1 = seaborn.distplot(plot01, label='Australasia') 
    fig1 = seaborn.distplot(plot02, label = 'Trop & Sub Trop Dry broadleaf')
    fig1 = seaborn.distplot(plot03, label = 'Afrotropics')
    fig1 = seaborn.distplot(plot04, label='Indo-Malay') 
    fig1 = seaborn.distplot(plot05, label = 'Nearctic')
    fig1 = seaborn.distplot(plot06, label = 'Neotropical')
    fig1 = seaborn.distplot(plot07, label='Trop & Sub Trop Savanna') 
    fig1 = seaborn.distplot(plot08, label = 'Pelearctic')


    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.legend()
    plt.title(title)
    
    fig1 = fig1.get_figure()
    fig1.savefig(folderout + title + '.png')

def hist_seaborn_biomes(filein, folderout, title, column = 'r_sq'):
    """
    Function to plot histogram with seaborn
    
    Parameters
    ----------
    filein: string
          Filepath for dataframe to use for plotting
          
    folderout: string
          Filepath to save plot
           
    title: string
          Name for file to save plot       

    """
    df = pd.read_csv(filein)
    df['join']=df['join'].astype(str)
    realm=df['join'].str[:1]
    biome=df['join'].str[1:3]
    df['realm'] = realm
    df['biome'] = biome
    df.drop_duplicates(subset ='join', 
                     inplace = True) 
    
    df['biome']=df['biome'].astype(int)
    #biomes = list(np.unique(df['biome']))
    #realms = list(np.unique(df['realm']))    
    
    df01 = df.loc[df['biome']== 1]
    df02 = df.loc[df['biome']== 2]
    df03 = df.loc[df['biome']== 3]
    df04 = df.loc[df['biome']== 4]
    df05 = df.loc[df['biome']== 5]
    df06 = df.loc[df['biome']== 6]    
    df07 = df.loc[df['biome']== 7]
    df08 = df.loc[df['biome']== 8]
    df09 = df.loc[df['biome']== 9]
    df10 = df.loc[df['biome']== 10]
    df11 = df.loc[df['biome']== 11]
    df12 = df.loc[df['biome']== 12]
    df13 = df.loc[df['biome']== 13]
    df14 = df.loc[df['biome']== 14]

    plot01 = df01[column]
    plot02 = df02[column]
    plot03 = df03[column]
    plot04 = df04[column]
    plot05 = df05[column]
    plot06 = df06[column]
    plot07 = df07[column]
    plot08 = df08[column]
    plot09 = df09[column]
    plot10 = df10[column]
    plot11 = df11[column]
    plot12 = df12[column]
    plot13 = df13[column]
    plot14 = df14[column]
    
    fig1 = seaborn.distplot(plot01, label='TST Moist broadleaf') 
    #fig1 = seaborn.distplot(plot02, label = 'TST Dry broadleaf')
    #fig1 = seaborn.distplot(plot03, label = 'TST Conifer')
    fig1 = seaborn.distplot(plot04, label='Temperate Broadleaf') 
    fig1 = seaborn.distplot(plot05, label = 'Temperate Conifer')
   # fig1 = seaborn.distplot(plot06, label = 'Boreal/Taiga')
    fig1 = seaborn.distplot(plot07, label='TST Savanna') 
    fig1 = seaborn.distplot(plot08, label = 'Temperate Savanna')
    #fig1 = seaborn.distplot(plot09, label = 'Flooded Savanna')
    #fig1 = seaborn.distplot(plot10, label='Montane Shrublands') 
    #fig1 = seaborn.distplot(plot11, label = 'Tundra')
    #fig1 = seaborn.distplot(plot12, label = 'Mediterranean')
    #fig1 = seaborn.distplot(plot13, label='Deserts') 
    fig1 = seaborn.distplot(plot14, label = 'Mangroves')

    plt.xlabel('maxCD')
    plt.ylabel('frequency')
    plt.legend()
    #plt.title('Savanna')
    
    fig1 = fig1.get_figure()
    fig1.savefig(folderout + title + '.png')
        
def biomes_plus_realms(folderin, folderout):

    filelist = glob.glob(folderin + 'biome*.csv')
    
    for file in filelist:
        df = pd.read_csv(file)
        hd, tl = path.split(file)
        name = tl.replace('biome_', "")
        b = name.replace('.csv', "")
        realms = list(np.unique(df['realm']))


        for r in realms:
            new = df.loc[df['realm']==r]    
            new.to_csv(folderout + 'biome_{}_realm_{}.csv'.format(b,r))   

def obtain_means(filein, fileout, col):
    #filein = '/Users/heatherkay/q_res/biomes/final_q.csv'
    df = pd.read_csv(filein)

    df['join']=df['join'].astype(str)
    realm=df['join'].str[:1]
    biome=df['join'].str[1:3]
    df['realm'] = realm
    df['biome'] = biome
    
    df.drop_duplicates(subset ='join', 
                     inplace = True) 
    
    biomes = list(np.unique(df['biome']))
    realms = list(np.unique(df['realm']))
    
    results = pd.DataFrame(columns = ['b','r','min','max','mean'])
    
    for b in biomes:
        new = df.loc[df['biome']==b] 
        for r in realms:
            new_r = new.loc[new['realm']==r]
            q = new_r[col]
            low = q.min()
            high = q.max()
            mean = q.mean()
            results = results.append({'b':b, 'r':r, 'min':low, 'max':high, 
                                      'mean':mean}, ignore_index=True)
            
    results.to_csv(fileout)        
        
def descriptive_stats(filein, fileout):
    """
    Function to output descriptive stats per biome and realm
    
    Parameters
    ----------
    filein: string
          Filepath for dataframe to use for plotting
          
    fileout: string
           Filepath to save plot    
    """
    #filein = '/Users/heatherkay/q_res/biomes/final_q.csv'
    #fileout =  '/Users/heatherkay/q_res/biomes/decriptive_stats3.csv'

    df = pd.read_csv(filein)
    df['join']=df['join'].astype(str)
    realm=df['join'].str[:1]
    biome=df['join'].str[1:3]
    df['realm'] = realm
    df['biome'] = biome
    df.drop_duplicates(subset ='join', 
                     inplace = True) 
    
    df['biome']=df['biome'].astype(int)
    df = df[df.realm != '-']
    df['realm']=df['realm'].astype(int) 
           
    biomes = list(np.unique(df['biome']))
    realms = list(np.unique(df['realm']))
    
    results=pd.DataFrame(columns=['category', 'df', 'q_mean', 'q_median','var_q','q_shap','mse_mean',
                                  'mse_median','var_mse','mse_shap'])
    
    for b in biomes:
        dfb = df.loc[df['biome']==b]
        deg_free = len(dfb['mse'])
        q = dfb['q']
        r2 = dfb['mse']
        meanq = q.mean()
        meanr2 = r2.mean()
        medianq = q.median()
        medianr2 = r2.median()
        varq = q.var()
        varr2 = r2.var()
        stdq = q.std()
        stdr2 = r2.std()
        
        length = len(r2)
        if length <4:
            continue

        results = results.append({'category': b, 'df':deg_free, 'q_mean':meanq, 
                                  'q_median':medianq, 'var_q':varq, 'std_q':stdq,
                                  'mse_mean':meanr2, 'mse_median':medianr2, 
                                  'var_mse':varr2, 'std_mse':stdr2}, ignore_index=True)
        
    for r in realms:    
        dfb = df.loc[df['realm']==r]
        deg_free = len(dfb['mse'])
        q = dfb['q']
        r2 = dfb['mse']
        meanq = q.mean()
        meanr2 = r2.mean()
        medianr2 = r2.median()
        medianq = q.median()
        varq = q.var()
        varr2 = r2.var()
        stdq = q.std()
        stdr2 = r2.std()
       
        length = len(r2)
        if length <4:
            continue

        results = results.append({'category': r, 'df':deg_free, 'q_mean':meanq,
                                  'q_median':medianq, 'var_q':varq, 'std_q':stdq, 
                                  'mse_mean':meanr2, 'mse_median':medianr2, 
                                  'var_mse':varr2, 'std_mse':stdr2}, ignore_index=True)     

    results.to_csv(fileout)


def std_dev(filein, fileout):
    """
    Function to obtain standard deviation for each polygon
    
    Parameters
    ----------
    filein: string
          Filepath for dataframe to use for plotting
          
    fileout: string
           Filepath to save plot    
    """
    filein = '/Users/heatherkay/q_res/biomes/final_q.csv'
    fileout =  '/Users/heatherkay/q_res/biomes/decriptive_stats3.csv'

    df = pd.read_csv(filein)
    df['join']=df['join'].astype(str)
    #realm=df['join'].str[:1]
    #biome=df['join'].str[1:3]
    #df['realm'] = realm
    #df['biome'] = biome
    df.drop_duplicates(subset ='join', 
                     inplace = True) 
    
    

import numpy as np
import matplotlib.pyplot as plt

def matplotlib_hist(filein, folderout)
    df01 = df.loc[df['biome']== 1]
    df02 = df.loc[df['biome']== 2]
    df03 = df.loc[df['biome']== 3]
    df04 = df.loc[df['biome']== 4]
    df05 = df.loc[df['biome']== 5]
    df06 = df.loc[df['biome']== 6]    
    df07 = df.loc[df['biome']== 7]
    df08 = df.loc[df['biome']== 8]
    df09 = df.loc[df['biome']== 9]
    df10 = df.loc[df['biome']== 10]
    df11 = df.loc[df['biome']== 11]
    df12 = df.loc[df['biome']== 12]
    df13 = df.loc[df['biome']== 13]
    df14 = df.loc[df['biome']== 14]

    plot01 = df01['r_sq']
    plot02 = df02['r_sq']
    plot03 = df03['r_sq']
    plot04 = df04['r_sq']
    plot05 = df05['r_sq']
    plot06 = df06['r_sq']
    plot07 = df07['r_sq']
    plot08 = df08['r_sq']
    plot09 = df09['r_sq']
    plot10 = df10['r_sq']
    plot11 = df11['r_sq']
    plot12 = df12['r_sq']
    plot13 = df13['r_sq']
    plot14 = df14['r_sq']
    
    #fig1 = seaborn.distplot(plot01, label='TST Moist broadleaf') 
    #fig1 = seaborn.distplot(plot02, label = 'TST Dry broadleaf')
    #fig1 = seaborn.distplot(plot03, label = 'TST Conifer')
    #fig1 = seaborn.distplot(plot04, label='Temperate Broadleaf') 
    #fig1 = seaborn.distplot(plot05, label = 'Temperate Conifer')
    #fig1 = seaborn.distplot(plot06, label = 'Boreal/Taiga')
    #fig1 = seaborn.distplot(plot07, label='TST Savanna') 
    #fig1 = seaborn.distplot(plot08, label = 'Temperate Savanna')
    #fig1 = seaborn.distplot(plot09, label = 'Flooded Savanna')
    #fig1 = seaborn.distplot(plot10, label='Montane Shrublands') 
    #fig1 = seaborn.distplot(plot11, label = 'Tundra')
    #fig1 = seaborn.distplot(plot12, label = 'Mediterranean')
    #fig1 = seaborn.distplot(plot13, label='Deserts') 
    #fig1 = seaborn.distplot(plot14, label = 'Mangroves')


    # Create two overlayed histograms
    plt.hist(plot10, label='Montane Shrublands')
    plt.hist(plot14, label = 'Mangroves')
    #plt.hist(plot09, label = 'Flooded Savanna')

    plt.legend()
    plt.ylabel("Quantity")
    plt.xlabel("Value")
    plt.show()

import glob
import os.path

def create_combo_csvs(folderin, folderout):
    filelist = glob.glob(folderin + 'biome*.csv')
    for file in filelist:
        name = os.path.splitext(os.path.basename(file))[0]
        df = pd.read_csv(file)
        realms = list(np.unique(df['realm']))
        for r in realms:
            new = df.loc[df['realm']==r]  
            if new.empty:
                continue
            new.to_csv(folderout + name + '_realm_{}.csv'.format(r))
        
def max_and_mins(filein, fileout):
    """
    Function to output descriptive stats per biome and realm
    
    Parameters
    ----------
    filein: string
          Filepath for dataframe to use for plotting
          
    fileout: string
           Filepath to save plot    
    """
    #filein = '/Users/heatherkay/q_res/biomes/final_q.csv'
    #fileout =  '/Users/heatherkay/q_res/biomes/decriptive_stats3.csv'

    df = pd.read_csv(filein)
    df['join']=df['join'].astype(str)
    realm=df['join'].str[:1]
    biome=df['join'].str[1:3]
    df['realm'] = realm
    df['biome'] = biome
    df.drop_duplicates(subset ='join', 
                     inplace = True) 
    
    df['biome']=df['biome'].astype(int)
    df = df[df.realm != '-']
    df['realm']=df['realm'].astype(int) 
           
    biomes = list(np.unique(df['biome']))
    realms = list(np.unique(df['realm']))
    
    results=pd.DataFrame(columns=['category', 'df', 'cd_max', 'cd_min','h_max','h_min'])
    
    for b in biomes:
        dfb = df.loc[df['biome']==b]
        deg_free = len(dfb['cd'])
        q = dfb['cd']
        r2 = dfb['height']
        maxcd = q.max()
        maxh = r2.max()
        mincd = q.min()
        minh = r2.min()
        
        length = len(r2)
        if length <4:
            continue

        results = results.append({'category': b, 'df':deg_free, 'cd_max':maxcd,
                                  'cd_min':mincd, 'h_max':maxh, 'h_min': minh}, ignore_index=True)
        
    for r in realms:    
        dfb = df.loc[df['realm']==r]
        deg_free = len(dfb['cd'])
        q = dfb['cd']
        r2 = dfb['height']
        maxcd = q.max()
        maxh = r2.max()
        mincd = q.min()
        minh = r2.min()
       
        length = len(r2)
        if length <4:
            continue

        results = results.append({'category': r, 'df':deg_free, 'cd_max':maxcd,
                                  'cd_min':mincd, 'h_max':maxh, 'h_min': minh}, ignore_index=True)     

    results.to_csv(fileout)    

"""            
not a function, manual plotting of histograms for investigation
"""
#Q & R2
#folderin = '/Users/heatherkay/q_res/biomes/2021_investigation/combo/'
#folderout = '/Users/heatherkay/q_res/biomes/2021_investigation/combo/figs/biomes_standardised/'
#folderout2 = '/Users/heatherkay/q_res/biomes/2021_investigation/combo/figs/R2/'

#MSE
folderin = '/Users/heatherkay/q_res/MSE/biomes/combo/'
folderout = '/Users/heatherkay/q_res/MSE/figs/'
#folderout2 = '/Users/heatherkay/q_res/biomes/2021_investigation/combo/figs/R2/'

#df_biome_realm
b = '14'
r = '1'
df_b_r = pd.read_csv(folderin + 'biome_' + b + '_realm_' + r + '.csv')           

df_b_r.drop_duplicates(subset ='join', keep = False, inplace = True) 

#read in file above and then get plot data for each file
"""
plot01 = df_b_r['q']
#plot02 = df_b_r['q']
plot03 = df_b_r['q']
plot04 = df_b_r['q']
plot05 = df_b_r['q']
plot06 = df_b_r['q']
#plot07 = df_b_r['q']
plot08 = df_b_r['q']
plot09 = df_b_r['q']
plot10 = df_b_r['q']
plot11 = df_b_r['q']
plot12 = df_b_r['q']
plot13 = df_b_r['q']
#plot14 = df_b_r['q']
"""

#rsq01 = df_b_r['mse']
rsq03 = df_b_r['mse']
rsq04 = df_b_r['mse']
#rsq05 = df_b_r['mse']
rsq06 = df_b_r['mse']
#rsq08 = df_b_r['mse']
    
#fig1 = seaborn.distplot(plot01, label='TST Moist broadleaf') 
#fig1 = seaborn.distplot(plot02, label = 'TST Dry broadleaf')
#fig1 = seaborn.distplot(plot03, label = 'TST Conifer')
#fig1 = seaborn.distplot(plot04, label='Temperate Broadleaf') 
#fig1 = seaborn.distplot(plot05, label = 'Temperate Conifer')
#fig1 = seaborn.distplot(plot06, label = 'Boreal/Taiga')
#fig1 = seaborn.distplot(plot07, label='TST Savanna') 
#fig1 = seaborn.distplot(plot08, label = 'Temperate Savanna')
#fig1 = seaborn.distplot(plot09, label = 'Flooded Savanna')
#fig1 = seaborn.distplot(plot10, label='Montane Shrublands') 
#fig1 = seaborn.distplot(plot11, label = 'Tundra')
#fig1 = seaborn.distplot(plot12, label = 'Mediterranean')
#fig1 = seaborn.distplot(plot13, label='Deserts') 
#fig1 = seaborn.distplot(plot14, label = 'Mangroves')
"""
fig1 = seaborn.distplot(plot01, label='Australasia') 
fig1 = seaborn.distplot(plot03, label = 'Afrotropics')
fig1 = seaborn.distplot(plot04, label='Indo Malay') 
#fig1 = seaborn.distplot(plot05, label = 'Nearctic')
fig1 = seaborn.distplot(plot06, label = 'Neotropical')
#fig1 = seaborn.distplot(plot08, label = 'Pelearctic')



plt.xlim([0, 0.16])
plt.xlabel('q value')
plt.ylabel('frequency')
plt.legend()
plt.title('TST Moist Broadleaf')
    
fig1 = fig1.get_figure()
fig1.savefig(folderout + 'TST Moist Broadleaf.png')
"""

#fig2 = seaborn.distplot(rsq01, label='Australasia')   
fig2 = seaborn.distplot(rsq03, label = 'Afrotropics')
fig2 = seaborn.distplot(rsq04, label='Indo-Malay') 
#fig2 = seaborn.distplot(rsq05, label = 'Nearctic')
fig2 = seaborn.distplot(rsq06, label = 'Neotropical') 
#fig2 = seaborn.distplot(rsq08, label = 'Pelearctic')

plt.xlim([0, 0.08])
plt.xlabel('mean squared error')
plt.ylabel('frequency')
plt.legend()
plt.title('Mangrove')
    
fig2 = fig2.get_figure()
fig2.savefig(folderout + 'Mangrove.png')


"""
Manual version of hist_seaborn
"""
filein = '/Users/heatherkay/q_res/biomes/with_b&r_noduplicates.csv'
folderout = '/Users/heatherkay/q_res/biomes/plots/'
df = pd.read_csv(filein)
df['join']=df['join'].astype(str)
realm=df['join'].str[:1]
biome=df['join'].str[1:3]
df['realm'] = realm
df['biome'] = biome
df.drop_duplicates(subset ='join', 
                 keep = False, inplace = True) 
    
df['realm']=df['realm'].astype(str)
#biomes = list(np.unique(df['biome']))
#realms = list(np.unique(df['realm']))    
    
df01 = df.loc[df['realm']== '1']
#df02 = df.loc[df['realm']== '2']
df03 = df.loc[df['realm']== '3']
df04 = df.loc[df['realm']== '4']
df05 = df.loc[df['realm']== '5']
df06 = df.loc[df['realm']== '6']    
#df07 = df.loc[df['realm']== '7']
df08 = df.loc[df['realm']== '8']

plot01 = df01['q']
#plot02 = df02['q']
plot03 = df03['q']
plot04 = df04['q']
plot05 = df05['q']
plot06 = df06['q']
#plot07 = df07['q']
plot08 = df08['q']

fig1 = seaborn.distplot(plot01, label='Australasia') 
#fig1 = seaborn.distplot(plot02, label = 'Trop & Sub Trop Dry broadleaf')
fig1 = seaborn.distplot(plot03, label = 'Afrotropics')
fig1 = seaborn.distplot(plot04, label='Indo-Malay') 
fig1 = seaborn.distplot(plot05, label = 'Nearctic')
fig1 = seaborn.distplot(plot06, label = 'Neotropical')
#fig1 = seaborn.distplot(plot07, label='Trop & Sub Trop Savanna') 
fig1 = seaborn.distplot(plot08, label = 'Pelearctic')

plt.xlabel('q value')
plt.ylabel('frequency')
plt.legend()
#plt.title(title)
    
fig1 = fig1.get_figure()
fig1.savefig(folderout + 'All_realm.png')

"""
finding degrees of freedom/polygon in each biome and realm
"""
for b in biomes2:
    dfb = df.loc[df['biome']==b]
    deg_free = dfb['deg_free']
    mean = deg_free.mean()
    std = deg_free.std()
    results = results.append({'cat':b,'mean':mean,'std':std},ignore_index=True)
    fig1 = seaborn.distplot(deg_free) 
    fig1 = fig1.get_figure()
    fig1 = fig1.clf
    
for b in realms:
    dfb = df.loc[df['realm']==b]
    deg_free = dfb['deg_free']
    mean = deg_free.mean()
    std = deg_free.std()
    results = results.append({'cat':b,'mean':mean,'std':std},ignore_index=True)

