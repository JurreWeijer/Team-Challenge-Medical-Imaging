# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 10:22:08 2023

@author: 20182371
"""
import math 
from scipy.ndimage import gaussian_filter 
from skimage import feature

def GetNextSeed(work_slice, seed):
    
    seedx = seed[0]
    seedy = seed[1]
    
    gaussian = gaussian_filter(work_slice, sigma=3)
    edges1 = feature.canny(gaussian, sigma = 3)
    #window = edges1[seedy-100:seedy+100,seedx-100:seedx+100]
    
    #find closest gradient points within an increading radius i 
    i = 1
    near_points = []
    looking = True
    while(looking):
        for k in range((seedx-i),(seedx+i+1)):
            for j in range(seedy-i,seedy+i+1):
                if edges1[k,j]:
                    near_points.append((k,j))
        i += 1
        if len(near_points) != 0:
            looking = False
        #stops looking when we find the first gradient points 
        
    # now we need to determine which one is the closest
    #get the euclidean distance from all and decide on the new seed
    min_distance = math.dist((seedx,seedy), (near_points[0]))
    next_seed = near_points[0]
    for point in near_points:
        if math.dist((seedx,seedy), point) < min_distance:
            min_distance = math.dist((seedx,seedy), point)
            next_seed = point
            
    return next_seed