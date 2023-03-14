# This is a sample Python script.
import cv2
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
import SimpleITK as sitk
import cv2 as cv


# datapath to map with Scoliotic and Nonscoliotic data, assumed to be in the same folder as your code
datapath = Path("../Data")

scoliosis_path = datapath / "Scoliose"

def OpenScoliosis(path, name):
    patient_path = path / name
    if os.path.exists(patient_path):
        image = sitk.ReadImage(str(patient_path))

    else:
        raise Exception("File does not exist at " + str(patient_path))

    return image

ThresholdFilter = sitk.BinaryThresholdImageFilter()
DilationFilter = sitk.DilateObjectMorphologyImageFilter()
ErosionFilter = sitk.ErodeObjectMorphologyImageFilter()
GaussianFilter = sitk.SmoothingRecursiveGaussianImageFilter()
OpeningFilter = sitk.BinaryMorphologicalOpeningImageFilter()
ClosingFilter = sitk.BinaryMorphologicalClosingImageFilter()
ThinningFilter = sitk.BinaryThinningImageFilter()

def SimpleSegmentation(image, threshold = 150, OpeningSize = 1, ClosingSize = 2):
    #Segments the given grey-scale image based on the following parameters
    #Implements a very basic segmentation with only an opening and closing filter

    ThresholdFilter.SetLowerThreshold(threshold)
    ThresholdFilter.SetUpperThreshold(int(np.max(sitk.GetArrayFromImage(image))))
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

def FilterLargestComponents(image, size= 100000):
    #Filters out only components that are larger than the given size from the segmentation mask

    MinSize = 100 #To make sure tiny objects are not printed

    ConnectedComponentFilter = sitk.ConnectedComponentImageFilter()
    RelabelComponentFilter = sitk.RelabelComponentImageFilter()
    RelabelComponentFilter.SetSortByObjectSize(True)
    RelabelComponentFilter.SetMinimumObjectSize(MinSize)

    component_image = ConnectedComponentFilter.Execute(image)
    sorted_component_image = RelabelComponentFilter.Execute(component_image)

    print("Objects in image larger than " + str(MinSize) + " are " + str(RelabelComponentFilter.GetSizeOfObjectsInPixels()) + " Pixels")
    print("Filtering objects larger than " + str(size))

    RelabelComponentFilter.SetMinimumObjectSize(size)
    large_component_image = RelabelComponentFilter.Execute(component_image)

    ThresholdFilter.SetLowerThreshold(1)
    thresholded_large_component_image = ThresholdFilter.Execute(large_component_image)

    return thresholded_large_component_image

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

    ThresholdFilter.SetLowerThreshold(200)
    ThresholdFilter.SetUpperThreshold(int(np.max(image_array)))
    OpeningFilter.SetKernelRadius(3)

    img_processed = ThresholdFilter.Execute(image)

    img_processed = OpeningFilter.Execute(img_processed)



    return img_processed

GetSegmented = False

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    img_scoliosis = OpenScoliosis(scoliosis_path, "1preop.nii")
    image_array = sitk.GetArrayFromImage(img_scoliosis) #Image array has values based on Houndsfield units
    print("Maximal value " + str(np.max(image_array)) + " Minimal value " + str(np.min(image_array)))

    #Quick if statement for skipping the segmentation if it already has been run once. To run segmentation again, make sure GetSegmented = False above the __main__ function
    if GetSegmented == False:
        img_processed = SimpleSegmentation(img_scoliosis)
        img_largest = FilterLargestComponents(img_processed)
        sitk.WriteImage(img_processed, str(datapath / "mask_result.nii"))
        sitk.WriteImage(img_largest , str(datapath/ "LargestComponent.nii"))
    else:
        img_processed = sitk.ReadImage(str(datapath/"mask_result.nii"))
        img_largest = sitk.ReadImage(str(datapath/ "LargestComponent.nii"))

    segmentation_mask = sitk.GetArrayFromImage(img_largest)

    slice_num = 100

    plt.figure()
    plt.imshow(image_array[slice_num,:,:], cmap="gray")
    plt.title("Original Image")
    plt.figure()
    plt.imshow(segmentation_mask[slice_num,:,:], cmap="gray")
    plt.title("Segmentation mask")
    plt.figure()
    plt.imshow(image_array[slice_num,:,:] * segmentation_mask[slice_num,:,:], cmap="gray", vmin = 0)
    plt.title("Segmented Image")
    plt.show()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
