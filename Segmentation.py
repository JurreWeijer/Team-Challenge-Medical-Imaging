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

def SimpleSegmentation(image):
    threshold = 150
    OpeningSize = 1
    ClosingSize = 2

    ThresholdFilter.SetLowerThreshold(threshold)
    ThresholdFilter.SetUpperThreshold(int(np.max(image_array)))
    OpeningFilter.SetKernelRadius(OpeningSize)
    ClosingFilter.SetKernelRadius(ClosingSize)

    print("Starting SimpleSegmentation sequence")

    img_processed = ThresholdFilter.Execute(image)

    print("Thresholding completed with a threshold of " + str(threshold))

    img_processed = OpeningFilter.Execute(img_processed)

    print("Binary Morphological opening completed with a kernel size of " + str(OpeningSize))

    img_processed = ClosingFilter.Execute(img_processed)

    print("Binary Morphological closing completed with a kernel size of " + str(ClosingSize))

    print("SimpleSegmentation done")

    return img_processed

def BanikSegmentation(image):
# Segmentation based on the paper by Banik et al.
# Automatic Segmentation of the Ribs, the Vertebral Column, and the Spinal Canal in Pediatric Computed Tomographic Images  https://doi.org/10.1007/s10278-009-9176-x

# Steps described:
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

    ThresholdFilter.SetLowerThreshold(150) #Original paper gave 100, but this gives better results
    ThresholdFilter.SetUpperThreshold(int(np.max(image_array)))
    OpeningFilter.SetKernelRadius(1) #Original paper gave 3, but this gives better results
    ClosingFilter.SetKernelRadius(2)

    img_processed = ThresholdFilter.Execute(image)

    img_processed = OpeningFilter.Execute(img_processed)



    return img_processed

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    img_scoliosis = OpenScoliosis(scoliosis_path, "1preop.nii")
    image_array = sitk.GetArrayFromImage(img_scoliosis) #Image array has values based on Houndsfield units
    print("Maximal value " + str(np.max(image_array)) + " Minimal value " + str(np.min(image_array)))

    img_processed = SimpleSegmentation(img_scoliosis)

    VoxelSize = img_scoliosis.GetSpacing()
    segmentation_array = sitk.GetArrayFromImage(img_processed)

    slice_num = 200
    plt.imshow(image_array[slice_num, :, :], cmap="gray")
    plt.title("Original Image")
    plt.figure()
    plt.imshow(image_array[slice_num, :, :]*segmentation_array[slice_num,:,:], cmap="gray")
    plt.title("Segmented Image")
    plt.show()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
