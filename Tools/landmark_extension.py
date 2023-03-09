# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 17:58:51 2023

@author: 20182371
"""
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 16:46:46 2023
@author: Sejin
"""


#from PIL import Image
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
datapath = Path(r"C:\Users\20182371\Documents\TUe\TeamChallenge_Data")

scoliosis_path = datapath / "Scoliose"
nonscoliotic_path = datapath / "Nonscoliotic"

#def OpenNonscoliotic(path, name):
#    img = Image.open(path / name)
#    return img

def OpenScoliosis(path, name):
    
    patient_path = path / name
    if os.path.exists(patient_path):
        image = sitk.ReadImage(patient_path)
        image_array = sitk.GetArrayFromImage(image)
        return image_array 
    else:
        print(f"File {patient_path} does not exist")
    
   

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

# =============================================================================
#     seedx, seedy = GetSeed(img)  
#     plt.switch_backend('module://ipykernel.pylab.backend_inline')
#     
#     next_seed = GetNextSeed(img, seedx, seedy)
#     prev_seed = (seedx, seedy)
#     next_seed = (seedx, seedy)
#     
#     for i in range(70):
#         plt.figure()
#         plt.plot(prev_seed[0], prev_seed[1], marker='*', color="red")
#         plt.imshow(img_scoliosis[slice_0+i,:,:], cmap = "gray")
#         
#         next_seed = GetNextSeed(img_scoliosis[slice_0+i+1,:,:], prev_seed[0], prev_seed[1])
#         prev_seed = next_seed
# 
# =============================================================================

    og_seeds = []
    seeds = np.zeros((img_scoliosis.shape[0], 2))
    
    #for some reason it is showing slice 0 twice 
    for i in range(0,464, 50):
        img = img_scoliosis[i,:,:]
        seedx, seedy = GetSeed(img)  
        og_seeds.append((seedx, seedy))
        seeds[i,0] = seedx
        seeds[i,1] = seedy
        print(i)
    
    plt.switch_backend('module://ipykernel.pylab.backend_inline')
# =============================================================================
#     for i in range(0,464, 50):
#         img = img_scoliosis[i,:,:]
#         plt.figure()
#         plt.imshow(img)
#         plt.show()
#     print(len(og_seeds))
#     plt.switch_backend('module://ipykernel.pylab.backend_inline')
#     j = 1
#     for i in range(0,464, 50):
#         plt.figure()
#         plt.imshow(img_scoliosis[i,:,:], cmap = 'gray')
#         plt.plot(og_seeds[j][0], og_seeds[j][1], marker = '*', color = "red")
#         plt.show()
#         j += 1
# =============================================================================
        
    og_seeds = og_seeds[1:]
    prev_seed = (og_seeds[0])
    next_seed = (og_seeds[0])
    

    #first propagate seed down
    slice_0 = 0
    n_seed = 0
    seeds = np.zeros((img_scoliosis.shape[0], 2))
    seeds[0,:] = og_seeds[0]
    for i in range(25):
        next_seed = GetNextSeed(img_scoliosis[slice_0+i+1,:,:], prev_seed[0], prev_seed[1])
        seeds[i+1, :] = next_seed
        prev_seed = next_seed
    #after first 25 propagate from next seed up
    for i in range(50,464, 50):
        if i <= 400:
            slice_0 = i
            n_seed += 1
            seeds[slice_0,:] = og_seeds[n_seed]
            prev_seed = (og_seeds[n_seed])
            next_seed = (og_seeds[n_seed])
            for j in range(25):
                next_seed = GetNextSeed(img_scoliosis[slice_0-j-1,:,:], prev_seed[0], prev_seed[1])
                seeds[slice_0-j-1,:] = next_seed
                prev_seed = next_seed
            prev_seed = og_seeds[n_seed]
            for k in range(25):
                next_seed = GetNextSeed(img_scoliosis[slice_0+k+1,:,:], prev_seed[0], prev_seed[1])
                seeds[slice_0+k+1, :] = next_seed
                prev_seed = next_seed
    for i in range(0,450):
        plt.figure()
        plt.imshow(img_scoliosis[i,:,:], cmap = 'gray')
        plt.plot(seeds[i,0], seeds[i,1], marker = '*', color = "red")