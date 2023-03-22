# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 16:17:30 2023

@author: 20182371
"""

import matplotlib.pyplot as plt
import SimpleITK as sitk
import numpy as np 

file_path = r"C:\Users\20182371\Documents\TUe\TeamChallenge_Data\Scoliose\1postop.nii"

image = sitk.ReadImage(file_path)
image_array = sitk.GetArrayFromImage(image)
print(image_array.shape)

#image_array = np.rot90(image_array, 2)
#image_array = np.fliplr(image_array)

transverse_slice = 420
coronal_slice = 140
# Create a figure with two subplots
fig, axs = plt.subplots(1, 2, figsize=(10, 5))

# Display the image array in each subplot
axs[0].imshow(image_array[:,coronal_slice,:], cmap="gray")
axs[0].set_title("Coronal Plane")
axs[0].axhline(y=transverse_slice, color='r', linewidth=1)
axs[0].invert_yaxis()

# Set titles for each subplot
axs[1].imshow(image_array[transverse_slice,:,:], cmap="gray")
axs[1].set_title("Transverse Plane")
axs[1].axhline(y=coronal_slice, color='r', linewidth=1)
axs[1].invert_yaxis()
axs[1].set_ylim(0, image_array.shape[0])

# Show the figure
plt.show()




