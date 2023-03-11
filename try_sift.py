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
import numpy as np
import cv2 as cv

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
img_scoliosis = OpenScoliosis(scoliosis_path,"2preop.nii")

slice_0 = 200
img = img_scoliosis[slice_0,:,:].astype('uint8')
image8bit = cv.normalize(img, None, 0, 255, cv.NORM_MINMAX).astype('uint8')

cv.imshow('og', image8bit)
cv.waitKey(0)

#img = cv.imread('home.jpg')
#gray= cv.cvtColor(img,cv.COLOR_BGR2GRAY)
sift = cv.SIFT_create()
#sift = cv.xfeatures2d.SIFT_create()
kp = sift.detect(img, None)

#kp, des = sift.detectAndCompute(img,None)

img=cv.drawKeypoints(img ,
                      kp ,
                      img ,
                      flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
#img=cv.drawKeypoints(img,kp,img)
#cv.imwrite('sift_keypoints.jpg',img)
cv.imshow('2', img)
cv.waitKey(0)