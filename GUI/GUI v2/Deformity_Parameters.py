# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 19:52:02 2023

@author: 20182371
"""

import math
import numpy as np 

def assymetry_index(pts):
    #pts = self.pts
    Ax = int(pts[0,0])
    Ay = int(pts[0,1])
    Bx = int(pts[1,0])
    By = int(pts[1,1])
    Cx = int(pts[2,0])
    Cy = int(pts[2,1])
    Dx = int(pts[3,0])
    Dy = int(pts[3,1])
    
    Dist_AB = np.sqrt((Bx-Ax)^2 + (By-Ay)^2)
    Dist_CD = np.sqrt((Dx-Cx)^2 + (Dy-Cy)^2)
    
    assymetry_ind = abs(1 - (Dist_AB/Dist_CD))
    
    return assymetry_ind

def angle_trunk_rotation(pts):
    
    Ax = int(pts[0,0])
    Ay = int(pts[0,1])
    Bx = int(pts[1,0])
    By = int(pts[1,1])
    
    Dist_AB = np.sqrt((Bx-Ax)^2 + (By-Ay)^2)
    
    angle_trunk = np.cos((Ax-Bx)/Dist_AB)
    
    return angle_trunk

def pectus_index(pts):
    
    Ax = int(pts[0,0])
    Ay = int(pts[0,1])
    Bx = int(pts[1,0])
    By = int(pts[1,1])
    Cx = int(pts[2,0])
    Cy = int(pts[2,1])
    Dx = int(pts[3,0])
    Dy = int(pts[3,1])
    
    Dist_AB = np.sqrt((Bx-Ax)^2 + (By-Ay)^2)
    Dist_CD = np.sqrt((Dx-Cx)^2 + (Dy-Cy)^2)
    
    pectus_index = Dist_AB/Dist_CD
    
    return pectus_index

def sagital_diameter(pts):
    
    Ax = int(pts[0,0])
    Ay = int(pts[0,1])
    Bx = int(pts[1,0])
    By = int(pts[1,1])
    
    sagital_diameter = np.sqrt((Bx-Ax)^2 + (By-Ay)^2)
    
    return sagital_diameter

def steep_vertebral(pts):
    
    Ax = int(pts[0,0])
    Ay = int(pts[0,1])
    Bx = int(pts[1,0])
    By = int(pts[1,1])
    
    steep_vertebral = np.sqrt((Bx-Ax)^2 + (By-Ay)^2)
    
    return steep_vertebral