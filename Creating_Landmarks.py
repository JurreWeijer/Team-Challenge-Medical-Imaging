# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 18:39:27 2023

@author: 20182371
"""
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
import SimpleITK as sitk

datapath = Path(r"C:\Users\20182371\Documents\TUe\TeamChallenge_Data")

scoliosis_path = datapath / "Scoliose"
nonscoliotic_path = datapath / "Nonscoliotic"

def OpenScoliosis(path, name):
    
    patient_path = path / name
    if os.path.exists(patient_path):
        image = sitk.ReadImage(str(patient_path))

    else:
        raise Exception("File does not exist at " + str(patient_path))

    return image

img_scoliosis = OpenScoliosis(scoliosis_path, "1preop.nii")

image_array = sitk.GetArrayFromImage(img_scoliosis)
print(np.shape(image_array))
slice_num = 200
plt.imshow(image_array[slice_num,:,:], cmap = "gray")
plt.show()

pts = []
pts = np.asarray(plt.ginput(3, timeout=-1))
print(pts)
print(pts[:,0])
print(pts[1,0])

plt.scatter(pts[:,0],pts[:,1])
 