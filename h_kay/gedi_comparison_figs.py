#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 15:25:45 2023

@author: heatherkay
"""
    res = df1.merge(df2, how='inner', on='Grid')
    df1 = res['qout_gedi_x'] = res.qout_gedi_x.astype(str)
    df2 = df1.str.strip('[]').astype(float)
    df3 = res.assign(q_glas = df2)
    df4 = df3['qout_gedi_y'] = df3.qout_gedi_y.astype(str)
    df5 = df4.str.strip('[]').astype(float)
    df6 = df3.assign(q_gedi = df5)    
    x= df6['q_gedi']
    y= df6['q_glas']
    z=[0, 0.05, 0.1]
    
    fig, ax = plt.subplots()
    ax.scatter(x, y, s=10)
    ax.plot(z,z, color='red')
    ax.set_xlim([0,0.1])
    ax.set_ylim([0,0.1])
    ax.set_title('GEDI Q1 2020 v GEDI Q3 2020')
    ax.set_ylabel('2020 Q3 q values')
    ax.set_xlabel('2020 Q1 q values')
    plt.savefig(fileout)
    plt.close