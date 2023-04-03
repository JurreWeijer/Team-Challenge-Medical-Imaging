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
        angle_trunk = 180 - (np.arccos((points["point_3"][0]-points["point_4"][0])/math.dist(points["point_3"], points["point_4"]))) * 180/math.pi
        return angle_trunk
    elif parameter == "Assymetry index":
        # Assymetry index = 1-(dis(5,6)/dis(7,8))
        assymetry_index = 1 - (np.sqrt((points["point_5"][0]-points["point_6"][0])**2+(points["point_5"][1]-points["point_6"][1])**2)/np.sqrt((points["point_7"][0]-points["point_8"][0])**2+(points["point_7"][1]-points["point_8"][1])**2))
        return assymetry_index
    elif parameter == "Pectus index":
        # Pectus index = dis(9,10)/dis(11,12)
        pectus_index = np.sqrt((points["point_9"][0]-points["point_10"][0])**2+(points["point_9"][1]-points["point_10"][1])**2)/np.sqrt((points["point_11"][0]-points["point_12"][0])**2+(points["point_11"][1]-points["point_12"][1])**2)
        return pectus_index
    elif parameter == "Sagittal diameter":
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
    
