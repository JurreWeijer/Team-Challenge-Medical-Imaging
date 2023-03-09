# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 12:53:12 2023

@author: 20182371
"""

import numpy as np
import SimpleITK as sitk
import matplotlib.pyplot as plt
import elastix



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
print(template_landmarks)

# Define the registration method
registration_method = sitk.ImageRegistrationMethod()

# Use normalized mutual information as the similarity metric
registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
registration_method.SetMetricSamplingStrategy(registration_method.RANDOM)
registration_method.SetMetricSamplingPercentage(0.01)

# Use affine transformation with gradient descent optimizer
registration_method.SetOptimizerAsGradientDescent(learningRate=1.0,
                                                  numberOfIterations=100,
                                                  convergenceMinimumValue=1e-6,
                                                  convergenceWindowSize=10)
registration_method.SetOptimizerScalesFromPhysicalShift()

registration_method.SetInitialTransform(sitk.AffineTransform(3))

# Execute the registration
final_transform = registration_method.Execute(template_img, moving_img)

landmarks_np = np.array(template_landmarks)

# Create a SimpleITK point set from the numpy array
landmarks_sitk = sitk.PointSet(2)
for landmark in landmarks_np:
    landmarks_sitk.SetPoint(int(landmark[0]), int(landmark[1]))

# Apply the final transform to the landmarks
landmarks_transformed_sitk = sitk.TransformPoints(landmarks_sitk, final_transform)

# Get the transformed landmarks as a numpy array
landmarks_transformed_np = np.zeros((len(template_landmarks), 2))
for i in range(len(template_landmarks)):
    landmarks_transformed_np[i] = landmarks_transformed_sitk.GetPoint(i)

# Print the transformed landmarks
print(landmarks_transformed_np)






# Display the new landmarks on the new image
#fig = plt.figure(figsize=(4,4),dpi=100)
#fig.set_facecolor(color = "white")
#subplot = fig.add_subplot()
#subplot.set_facecolor(color = "white")
#subplot.imshow(moving_img)
#subplot.scatter(new_landmarks[:,0],new_landmarks[:,1], c="red", marker = "x")
#fig.show()
