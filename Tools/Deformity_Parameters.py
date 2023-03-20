# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 19:52:02 2023

@author: 20182371
"""

import numpy as np 

def calculate_parameter(dict_landmarks, parameter, n_slice):
    
    points = dict_landmarks[f"slice_{n_slice}"]
    
    if parameter == "Angle Trunk Rotation":
        # Angle of trunk rotation = angle between line 1 -> 2 and line 3 -> 4
        # angle = cos(aanliggend/schuin) = cos(deltax/dis(3,4))
        angle_trunk = np.arccos((points["point_3"][0]-points["point_4"][0])/np.sqrt((points["point_3"][0]-points["point_4"][0])**2+(points["point_3"][1]-points["point_4"][1])**2)) # add calculation
        return angle_trunk
    elif parameter == "Assymetry Index":
        # Assymetry index = 1-(dis(5,6)/dis(7,8))
        assymetry_index = 1 - (np.sqrt((points["point_5"][0]-points["point_6"][0])**2+(points["point_5"][1]-points["point_6"][1])**2)/np.sqrt((points["point_7"][0]-points["point_8"][0])**2+(points["point_7"][1]-points["point_8"][1])**2))
        return assymetry_index
    elif parameter == "Pectus Index":
        # Pectus index = dis(9,10)/dis(11,12)
        pectus_index = np.sqrt((points["point_9"][0]-points["point_10"][0])**2+(points["point_9"][1]-points["point_10"][1])**2)/np.sqrt((points["point_11"][0]-points["point_12"][0])**2+(points["point_11"][1]-points["point_12"][1])**2)
        return pectus_index
    elif parameter == "Sagital Diameter":
        # Sagital diameter = dis(11,13)
        sagital_diameter = np.sqrt((points["point_11"][0]-points["point_13"][0])**2+(points["point_11"][1]-points["point_13"][1])**2)
        return sagital_diameter
    elif parameter == "Steep Vertebral":
        # Steep vertebral distance = dis(11,12)
        steep_vertebral = np.sqrt((points["point_11"][0]-points["point_12"][0])**2+(points["point_11"][1]-points["point_12"][1])**2)
        return steep_vertebral
    
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