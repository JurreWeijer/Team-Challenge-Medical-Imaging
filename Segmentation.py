# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
import SimpleITK as sitk

# datapath to map with Scoliotic and Nonscoliotic data, assumed to be in the same folder as your code
datapath = Path("./Data")

scoliosis_path = datapath / "Scoliose"

def OpenScoliosis(path, name):
    patient_path = path / name
    if os.path.exists(patient_path):
        image = sitk.ReadImage(str(patient_path))

    else:
        raise Exception("File does not exist at " + str(patient_path))

    return image

ThresholdFilter = sitk.BinaryThresholdImageFilter()
OpeningFilter = sitk.BinaryMorphologicalOpeningImageFilter()
ClosingFilter = sitk.BinaryMorphologicalClosingImageFilter()
ThinningFilter = sitk.BinaryThinningImageFilter()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    img_scoliosis = OpenScoliosis(scoliosis_path, "1preop.nii")
    image_array = sitk.GetArrayFromImage(img_scoliosis) #Image array has values based on Houndsfield units
    print("Maximal values " + str(np.max(image_array)) + " Minimal values " + str(np.min(image_array)))

    #Segmentation based on the paper by Banik et al.
    #Automatic Segmentation of the Ribs, the Vertebral Column, and the Spinal Canal in Pediatric Computed Tomographic Images  https://doi.org/10.1007/s10278-009-9176-x

    #Steps described:
    # RIBS:
    # Binarize by thresholding @ 200 HU
    # Morphologically open with radius of 3 pixels
    # Find central line along the medial sagittal plane based on the inner contour of fat
    # Measure Euclidian Distance between:
    #   (a) Edge of region and inner contour of fat
    #   (b) Centroid of region and inner contour of fat
    #   (c) Edge of region and central line
    #   (d) Centroid of region and central line
    # Divide CT image in Upper and lower area:
    #   Lower area
    #   Keep region if a <= 3.5 cm AND b <= 1.8 cm AND c >= 1.5cm AND d >=1.5cm
    #   Upper area
    #   Keep region if a <= 4.5 cm AND b <= 3 cm AND c >= 1cm AND d >=1cm

    ThresholdFilter.SetLowerThreshold(-10) #Original paper gave 100, but this gives better results
    ThresholdFilter.SetUpperThreshold(int(np.max(image_array)))
    OpeningFilter.SetKernelRadius(3)

    img_processed = ThresholdFilter.Execute(img_scoliosis)

    img_processed = OpeningFilter.Execute(img_processed)



    VoxelSize = img_scoliosis.GetSpacing()
    segmentation_array = sitk.GetArrayFromImage(img_processed)

    slice_num = 200
    plt.imshow(image_array[slice_num, :, :], cmap="gray")
    plt.title("Original Image")
    plt.figure()
    plt.imshow(segmentation_array[slice_num,:,:], cmap="gray")
    plt.title("Segmented Image")
    plt.show()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
