# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 16:46:46 2023

@author: Sejin
"""


from PIL import Image
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import math
import os
from pathlib import Path
import SimpleITK as sitk
from scipy import ndimage
from skimage import feature
from scipy.ndimage import gaussian_filter

#datapath to map with Scoliotic and Nonscoliotic data
datapath = Path(r"C:\Users\Sejin\Downloads\Team challenge_scoliosis\Team_challenge_scoliosis")

scoliosis_path = datapath / "Scoliose"
nonscoliotic_path = datapath / "Nonscoliotic"

def OpenNonscoliotic(path, name):
    img = Image.open(path / name)
    return img

def OpenScoliosis(path, name):
    
    patient_path = path / name
    if os.path.exists(patient_path):
        image = sitk.ReadImage(patient_path)
        image_array = sitk.GetArrayFromImage(image)
    else:
        print("File does not exist")
    
    return image_array 

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def GetSeed(img):
       
    plt.imshow(img,cmap='gray')
    seed_0 = plt.ginput(1)
    seedx = seed_0[0][0]
    seedy = seed_0[0][1]
    seedy = int(round(seedy))
    seedx = int(round(seedx))
   
    print(seedy, ",", seedx)
    
    return seedx, seedy


#input the slice and the seed we start from 
def GetNextSeed(work_slice, seedx, seedy):
    gaussian = gaussian_filter(work_slice, sigma=3)

    edges1 = feature.canny(gaussian, sigma = 3)

    window = edges1[seedy-100:seedy+100,seedx-100:seedx+100]
    
    
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
    
    
    
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    #img_nonscoliotic = OpenNonscoliotic(nonscoliotic_path, 'Control1a.tif')
# =============================================================================
    img_scoliosis = OpenScoliosis(scoliosis_path,"4preop.nii")
    slice_0 = 100
    img = img_scoliosis[slice_0,:,:]

    seedx, seedy = GetSeed(img)  
    plt.switch_backend('module://ipykernel.pylab.backend_inline')
    
    next_seed = GetNextSeed(img, seedx, seedy)
    prev_seed = (seedx, seedy)
    next_seed = (seedx, seedy)
    
    for i in range(70):
        plt.figure()
        plt.plot(prev_seed[0], prev_seed[1], marker='*', color="red")
        plt.imshow(img_scoliosis[slice_0+i,:,:], cmap = "gray")
        
        next_seed = GetNextSeed(img_scoliosis[slice_0+i+1,:,:], prev_seed[0], prev_seed[1])
        prev_seed = next_seed
        
    
    
# See PyCharm help at https://www.jetbrains.com/help/pycharm/