#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 18 08:33:58 2023

@author: heatherkay
"""


import rsgislib.vectorutils

rsgislib.vectorutils.check_validate_geometries('/Users/heatherkay/q_res/Layers/wwf_eco/wwf_terr_ecos.shp', 'wwf_terr_ecos', 
                                               '/Users/heatherkay/q_res/Layers/wwf_eco/wwf_terr_ecos.gpkg', 'wwf_terr_ecos', 
                                               out_format= 'GPKG', print_err_geoms= True, del_exist_vec= False)



import geopandas

df = geopandas.read_file('/Users/heatherkay/q_res/Layers/wwf_grid.gpkg')

df['eco']=df.index.astype(str).str[:5]

df['id'] = df['tile_name'].astype(str) + '_' + df['eco'].astype(str)


df.to_file('/Users/heatherkay/q_res/Layers/wwf_grid_plus_id.gpkg', driver='GPKG')