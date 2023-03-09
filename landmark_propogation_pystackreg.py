# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 12:53:12 2023

@author: 20182371
"""

import numpy as np
import cv2
import SimpleITK as sitk
import matplotlib.pyplot as plt
from pystackreg import StackReg
from scipy.ndimage import affine_transform



image = sitk.ReadImage(r"C:\Users\20182371\Documents\TUe\TeamChallenge_Data\Scoliose\1postop.nii")
image_array = sitk.GetArrayFromImage(image)
print(image_array.shape)

#load the template and new img
template_img = image_array[200, :, :]
moving_img = image_array[201,:,:]

#input the landmarks
plt.imshow(template_img)
template_landmarks = [] 
template_landmarks = np.asarray(plt.ginput(3, timeout=-1))
plt.close()

template_landmarks = template_landmarks.astype(int)
#template_landmarks = [(int(x[0]), int(x[1])) for x in template_landmarks]
print(template_landmarks)

#Bilinear transformation
sr = StackReg(StackReg.BILINEAR)
out_bil = sr.register_transform(template_img, moving_img)

# Obtain the transformation matrix from the StackReg object
transform_matrix = sr.get_matrix()

landmark_label = np.zeros((512,512))
for landmark in template_landmarks: 
    landmark_label[landmark[0],landmark[1]] = 1

landmark_image = sitk.GetImageFromArray(landmark_label)
new_landmarks = sr.transform(template_landmarks, tmat=transform_matrix)

#plt.imshow(transformed_landmark_label)

print(new_landmarks)



# Display the new landmarks on the new image
fig = plt.figure(figsize=(4,4),dpi=100)
fig.set_facecolor(color = "white")
subplot = fig.add_subplot()
subplot.set_facecolor(color = "white")
subplot.imshow(moving_img)
subplot.scatter(new_landmarks[:,0],new_landmarks[:,1], c="red", marker = "x")
fig.show()
