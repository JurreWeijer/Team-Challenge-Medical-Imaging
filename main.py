# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
import SimpleITK as sitk


#datapath to map with Scoliotic and Nonscoliotic data
datapath = Path(r"C:\Users\20182371\Documents\TUe\TeamChallenge_Data")

scoliosis_path = datapath / "Scoliose"
nonscoliotic_path = datapath / "Nonscoliotic"

def OpenNonscoliotic(path, name):
    img = Image.open(path / name)
    return img

def OpenScoliosis(path, name, slice_num):
    
    patient_path = path / name
    if os.path.exists(patient_path):
        image = sitk.ReadImage(patient_path)
        image_array = sitk.GetArrayFromImage(image)
    else:
        print("File does not exist")
    
    print(image_array.size())
    img_slice = image_array[slice_num,:,:]
    
    return img_slice

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    #img_nonscoliotic = OpenNonscoliotic(nonscoliotic_path, 'Control1a.tif')
    #print(img_nonscoliotic.size)
    #print(img_nonscoliotic.n_frames)
    #img_nonscoliotic.show()
    
    img_scoliosis = OpenScoliosis(scoliosis_path, "1preop.nii", 200)
    plt.imshow(img_scoliosis)
    
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
