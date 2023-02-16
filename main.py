# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
import SimpleITK as sitk


#datapath to map with Scoliotic and Nonscoliotic data, assumed to be in the same folder as your code
datapath = Path(r"C:\Users\20182371\Documents\TUe\TeamChallenge_Data")

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
    print(np.shape(image_array)[0])
    slice_num = 200
    plt.imshow(image_array[slice_num,:,:], cmap = "gray")
    plt.show()
    
   
    
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
