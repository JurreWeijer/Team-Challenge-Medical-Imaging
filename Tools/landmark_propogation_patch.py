# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 12:53:12 2023

@author: 20182371
"""

import numpy as np
import cv2
import SimpleITK as sitk
import matplotlib.pyplot as plt


image = sitk.ReadImage(r"C:\Users\20182371\Documents\TUe\TeamChallenge_Data\Scoliose\1postop.nii")
image_array = sitk.GetArrayFromImage(image)
print(image_array.shape)

#load the template and new img
template_img = image_array[200, :, :]
new_img = image_array[201,:,:]

#input the landmarks
plt.imshow(template_img)
template_landmarks = [] 
template_landmarks = np.asarray(plt.ginput(3, timeout=-1))
plt.close()

template_landmarks = template_landmarks.astype(int)
#template_landmarks = [(int(x[0]), int(x[1])) for x in template_landmarks]
print(template_landmarks)


#template_landmarks = [(100, 200), (150, 250), (200, 300)]

# Define the size of the template patch to use for matching
patch_size = (2,2)

# Define the maximum distance between matching points
max_distance = 5

# Iterate over the template landmarks and find matching landmarks in the new image
new_landmarks = []
for landmark in template_landmarks:
    # Extract the template patch around the landmark
    template_patch = template_img[landmark[1]-patch_size[1]//2:landmark[1]+patch_size[1]//2,
                                  landmark[0]-patch_size[0]//2:landmark[0]+patch_size[0]//2]

    # Search for a matching patch in the new image
    result = cv2.matchTemplate(new_img, template_patch, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # If the minimum distance between the matching point and the template point is less than max_distance, add the new landmark
    if min_val < max_distance:
        new_landmark = [landmark[0]+min_loc[0]+patch_size[0]//2, landmark[1]+min_loc[1]+patch_size[1]//2]
        new_landmarks.append(new_landmark)

new_landmarks = np.array(new_landmarks)

# Display the new landmarks on the new image
fig = plt.figure(figsize=(4,4),dpi=100)
fig.set_facecolor(color = "white")
subplot = fig.add_subplot()
subplot.set_facecolor(color = "white")
subplot.imshow(new_img)
subplot.scatter(new_landmarks[:,0],new_landmarks[:,1], c="red", marker = "x")
fig.show()
