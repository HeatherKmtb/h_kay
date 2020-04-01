#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 08:18:23 2020

@author: heatherkay
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 10:34:54 2020

@author: heatherkay
"""

import ogr, gdal, osr
from tqdm import tqdm
import numpy as np

gdal.UseExceptions()

ogr.UseExceptions()



def getshit(inFolder, inRas, field='id'):
    """
    Collect training as an np array for use with create model function
    
    Parameters
    --------------
        
    inFolder : string
              the input point shapefile of gla14 data
              load before hand with glob.glob(string)
              for example inFolder = glob.glob('/Users/heather/phd/test/*.shp')
             
    inRas : string
            the input raster 
        
    bands : int
            no of bands
        
    field : string
            the attribute field containing the training labels
    

    Returns
    ---------------------
    
    A tuple containing:
    -np array of training data
    -list of polygons with invalid geometry that were not collected 
    
    """   
    for inShape in inFolder:
    
        # Open files
        raster = gdal.Open(inRas)    
        shp = ogr.Open(inShape, update=1)
        
        lyr = shp.GetLayer()
        
        labels = np.arange(lyr.GetFeatureCount())
    
        rb = raster.GetRasterBand(1)
        rgt = raster.GetGeoTransform()
    
        #mem_drv = ogr.GetDriverByName('Memory')
        #driver = gdal.GetDriverByName('MEM')  
    
        lyr.CreateField(ogr.FieldDefn('Grid', ogr.OFTInteger))
        rejects = []

        inArray = rb.ReadAsArray()     
    
    
        for label in tqdm(labels):

            feat = lyr.GetFeature(label)
            if feat == None:
                print('no geometry for feature '+str(label))
                rejects.append(label)
                continue
            geom = feat.GetGeometryRef()
        
            # Get raster georeference info
        
            mx,my =geom.GetX(), geom.GetY()
            
            px = int((mx - rgt[0]) / rgt[1]) #x pixel
            py = int((my - rgt[3]) / rgt[5])
        
            if px >= rb.XSize:
                px = rb.XSize-1
            if py >= rb.YSize:
                py = rb.YSize-1
        
            outVal = inArray[py, px]
        
            feat.SetField('Grid', int(outVal))
            lyr.SetFeature(feat)
            feat = None
    
        lyr.SyncToDisk()
        lyr = None
        
        
        
        
        
        
        
            


           
