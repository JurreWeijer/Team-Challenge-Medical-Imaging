# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
import SimpleITK as sitk


#datapath to map with Scoliotic and Nonscoliotic data, assumed to be in the same folder as your code
datapath = Path("./Data")

scoliosis_path = datapath / "Scoliose"
nonscoliotic_path = datapath / "Nonscoliotic"

def OpenNonscoliotic(path, name):

    patient_path = path/name
    if os.path.exists(patient_path):
        image = sitk.ReadImage(str(patient_path))

    else:
        raise Exception("File does not exist at " + str(patient_path))

    return image

def OpenScoliosis(path, name):
    
    patient_path = path / name
    if os.path.exists(patient_path):
        image = sitk.ReadImage(str(patient_path))

    else:
        raise Exception("File does not exist at " + str(patient_path))

    return image

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    img_nonscoliotic = OpenNonscoliotic(nonscoliotic_path, 'Control1a.tif')
    
    img_scoliosis = OpenScoliosis(scoliosis_path, "1preop.nii")

    image_array = sitk.GetArrayFromImage(img_scoliosis)

    VoxelSize = img_scoliosis.GetSpacing()
    print(np.shape(image_array))
    slice_num = 200
    plt.imshow(image_array[slice_num,:,:], cmap = "gray")
    plt.show()
    
   
    
# See PyCharm help at https://www.jetbrains.com/help/pycharm/


# The functions for the different parameters we selected
# The point guesses 
point1 = (480,200,200)
point2 = (20,200,200)
point3 = (340,105,200)
point4 = (100,80,200)
point5 = (410,380,200)
point6 = (340,110,200)
point7 = (180,375,200)
point8 = (100,90,200)
point9 = (490,250,200)
point10 = (20,200,200)
point11 = (300,400,200)
point12 = (150,200,200)
point13 = (175,125,200)

# Angle of trunk rotation = angle between line 1 -> 2 and line 3 -> 4
# angle = cos(aanliggend/schuin) = cos(deltax/dis(3,4)) 
angle_trunk = np.cos((point3[0]-point4[0])/np.sqrt((point3[0]-point4[0])^2+(point3[1]-point4[1]))) # add calculation 

# Assymetry index = 1-(dis(5,6)/dis(7,8))
assymetry_index = 1 - (np.sqrt((point5[0]-point6[0])^2+(point5[1]-point6[1]))/np.sqrt((point7[0]-point8[0])^2+(point7[1]-point8[1])))
# Pectus index = dis(9,10)/dis(11,12)
pectus_index = np.sqrt((point9[0]-point10[0])^2+(point9[1]-point10[1]))/np.sqrt((point11[0]-point12[0])^2+(point11[1]-point12[1]))
# Sagital diameter = dis(11,13)
sagital_diameter = np.sqrt((point11[0]-point13[0])^2+(point11[1]-point13[1]))
# Steep vertebral distance = dis(11,12)
steep_vertebral = np.sqrt((point11[0]-point12[0])^2+(point11[1]-point12[1]))
