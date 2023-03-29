# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 19:52:02 2023

@author: 20182371
"""
import warnings

import numpy as np
from matplotlib import pyplot as plt
import math


def calculate_parameter(dict_landmarks, parameter, n_slice):
    
    points = dict_landmarks[f"slice_{n_slice}"]
    
    if parameter == "Angle trunk rotation":
        # Angle of trunk rotation = angle between line 1 -> 2 and line 3 -> 4
        # angle = cos(aanliggend/schuin) = cos(deltax/dis(3,4))
        #angle_trunk = np.arccos((points["point_3"][0]-points["point_4"][0])/np.sqrt((points["point_3"][0]-points["point_4"][0])**2+(points["point_3"][1]-points["point_4"][1])**2)) # add calculation
        angle_trunk = (np.arccos((points["point_3"][0]-points["point_4"][0])/math.dist(points["point_3"], points["point_4"]))) * 180/math.pi
        return angle_trunk
    elif parameter == "Assymetry index":
        # Assymetry index = 1-(dis(5,6)/dis(7,8))
        assymetry_index = 1 - (np.sqrt((points["point_5"][0]-points["point_6"][0])**2+(points["point_5"][1]-points["point_6"][1])**2)/np.sqrt((points["point_7"][0]-points["point_8"][0])**2+(points["point_7"][1]-points["point_8"][1])**2))
        return assymetry_index
    elif parameter == "Pectus index":
        # Pectus index = dis(9,10)/dis(11,12)
        pectus_index = np.sqrt((points["point_9"][0]-points["point_10"][0])**2+(points["point_9"][1]-points["point_10"][1])**2)/np.sqrt((points["point_11"][0]-points["point_12"][0])**2+(points["point_11"][1]-points["point_12"][1])**2)
        return pectus_index
    elif parameter == "Sagital diameter":
        # Sagital diameter = dis(11,13)
        sagital_diameter = np.sqrt((points["point_11"][0]-points["point_13"][0])**2+(points["point_11"][1]-points["point_13"][1])**2)
        return sagital_diameter
    elif parameter == "Steep vertebral":
        # Steep vertebral distance = dis(11,12)
        steep_vertebral = np.sqrt((points["point_11"][0]-points["point_12"][0])**2+(points["point_11"][1]-points["point_12"][1])**2)
        return steep_vertebral
    else:
        #Should never happen, unless there is a problem in the code
        warnings.warn("Invalid parameter selected in calculate_parameter: " + str(parameter))
    
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

def Find_Longest(Points1, Points2, c = 0):
    #Helper function to find longest distance on two contours given by Points1 and Points2
    # c = 0 for longest in x direction, c = 1 for longest in y direction
    max1 = True
    maxdist = 0
    for i, coords in enumerate(Points1):
        # Find the two points that are the farthest apart
        idx = (np.abs(Points2[:, c-1] - coords[c-1]).argmin())
        dist = np.abs(coords[c] - Points2[idx, c])
        if dist > maxdist:
            maxdist = dist
            max1idx = i
            max2idx = idx

    for i, coords in enumerate(Points2):
        # Find the two points that are the farthest apart, but reverse in case there are more points in 2 than in 1
        idx = (np.abs(Points1[:, c-1] - coords[c-1]).argmin())
        dist = np.abs(coords[c] - Points1[idx, c])
        if dist > maxdist:
            maxdist = dist
            max1idx = idx
            max2idx = i
            max1 = False

    maxPoints1 = Points1[max1idx]
    maxPoints2 = Points2[max2idx]

    #INTERPOLATION CODE, NOT WORKING YET
    # if max1:
    #     Pointsnew = np.take(Points2, np.where(Points2!=Points2[max2idx])[0][::2], axis = 0)
    #     secondidx = (np.abs(Pointsnew[:,c-1]) - Points1[max1idx,c-1]).argmin()
    #     m = (Points2[secondidx,c] - Points2[max2idx,c]) / (Points2[secondidx,c-1]-Points2[max2idx,c-1])
    #     newc = (Points1[max1idx,c] - Points2[max2idx,c]) * m + Points2[max2idx,c-1]
    #
    #     plt.figure()
    #     plt.scatter(newc,Points1[max1idx,c-1], c = 'r')
    #     plt.scatter(Points2[secondidx,c], Points2[secondidx,c-1], c = 'b')
    #     plt.scatter(Points2[max2idx,c], Points2[max2idx,c-1], c = 'g')
    #     maxPoints1 = Points1[max1idx,:]
    #     if c == 0:
    #         maxPoints2 = [newc, Points1[max1idx, c - 1]]
    #     else:
    #         maxPoints2 = [Points1[max1idx, c], newc]
    # else:
    #     Pointsnew = np.take(Points1, np.where(Points1 != Points1[max1idx])[0][::2], axis=0)
    #     secondidx = (np.abs(Pointsnew[:,c-1]) - Points2[max2idx,c-1]).argmin()
    #     newc = np.interp(Points2[max2idx,c], [Points1[max1idx,c],Points1[secondidx,c]], [Points1[max1idx,c-1], Points1[secondidx,c-1]])
    #     maxPoints2 = Points2[max2idx,:]
    #     if c == 0:
    #         maxPoints1 = [newc, Points2[max2idx, c - 1]]
    #     else:
    #         maxPoints1 = [Points2[max2idx, c], newc]

    return dist, maxPoints1, maxPoints2