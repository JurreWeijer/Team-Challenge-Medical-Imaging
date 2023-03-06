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
import warnings

import skimage.filters as filters
import skimage.segmentation as seg


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
DilationFilter = sitk.DilateObjectMorphologyImageFilter()
ErosionFilter = sitk.ErodeObjectMorphologyImageFilter()
#GaussianFilter = sitk.RecursiveGaussianImageFilter()
GaussianFilter = sitk.SmoothingRecursiveGaussianImageFilter()
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

def ContinuousContourMaker(image):
    #Experimental and not used, adapted from https://stackoverflow.com/questions/43293915/how-could-i-make-the-discontinuous-contour-of-an-image-consistant
    ClosingFilter.SetKernelRadius(20)
    img_contour = ClosingFilter.Execute(image)

    DilationFilter.SetKernelRadius(20)
    ErosionFilter.SetKernelRadius(13)
    GaussianFilter.SetSigma(10)

    img_contour = DilationFilter.Execute(img_contour)
    img_contour = ErosionFilter.Execute(img_contour)

    img_contour = GaussianFilter.Execute(img_contour)
    ThresholdFilter.SetLowerThreshold(0.5)
    img_contour = ThresholdFilter.Execute(img_contour)

    img_contour = sitk.GetArrayFromImage(img_contour)

    return img_contour

def ActiveContour(slice):
    #active contouring of a single slice, experimental and does not work well

    s = np.linspace(0, 2 * np.pi, 400)
    r = 250 + 250 * np.sin(s)
    c = 250 + 300 * np.cos(s)
    init = np.array([r, c]).T

    #From: https://scikit-image.org/docs/stable/api/skimage.segmentation.html#active-contour
    # alpha: Snake length shape parameter. Higher values makes snake contract faster.
    # beta: Snake smoothness shape parameter. Higher values makes snake smoother.
    # w_line: Controls attraction to brightness. Use negative values to attract toward dark regions.
    # w_edge: Controls attraction to edges. Use negative values to repel snake from edges.
    # gamma: Explicit time stepping parameter.

    snake = seg.active_contour(slice,
                               init, alpha=0.001, beta=5, w_line=100, w_edge=10, gamma=0.001)

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(slice, cmap=plt.cm.gray)
    ax.plot(init[:, 1], init[:, 0], '--r', lw=3)
    ax.plot(snake[:, 1], snake[:, 0], '-b', lw=3)
    return

def SingleSliceContour(slice):
    #Compute the contour of each blob on a single slice using the OpenCV toolkit
    #Adapted from the hull tutorial https://docs.opencv.org/3.4.2/d7/d1d/tutorial_hull.html

    canny_output = cv.Canny(image = slice, threshold1=0.5, threshold2=2)

    try:
        contour_img, contours, hierarchy = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    except:
        raise RuntimeError(
            "cv.findContours not working, most likely a wrong version of OpenCV, program was written for 3.4.2")

    hull_list = []
    centroid_list = []
    for i in range(len(contours)):
        M = cv.moments(contours[i])
        hull = cv.convexHull(contours[i])
        hull_list.append(hull)
        try:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        except:
            cX = 0
            cY = 0
            warnings.warn("Contour not fully segmented, returning 0 at index " + str(i), RuntimeWarning)

        centroid_list.append([cX, cY])
    #
    # cmap = plt.cm.get_cmap("hsv", len(hull_list))
    # plt.figure()
    # plt.imshow(contour_img, cmap="gray")
    # for i in range(len(hull_list)):
    #     plt.scatter(centroid_list[i][0], centroid_list[i][1], marker='P', color=cmap(i), s=4)
    #     plt.scatter(hull_list[i][:, 0, 0], hull_list[i][:, 0, 1], color=cmap(i), s=2)

    return hull_list, centroid_list

def FilterLargestComponents(image, size= 100000):
    #Filters out only components that are larger than the given size from the segmentation mask
    ConnectedComponentFilter = sitk.ConnectedComponentImageFilter()
    RelabelComponentFilter = sitk.RelabelComponentImageFilter()
    RelabelComponentFilter.SetSortByObjectSize(True)
    RelabelComponentFilter.SetMinimumObjectSize(100)

    component_image = ConnectedComponentFilter.Execute(image)
    sorted_component_image = RelabelComponentFilter.Execute(component_image)

    print(RelabelComponentFilter.GetSizeOfObjectsInPixels())

    RelabelComponentFilter.SetMinimumObjectSize(size)
    large_component_image = RelabelComponentFilter.Execute(component_image)

    save = False
    if save == True:
        sitk.WriteImage(large_component_image, str(datapath/"LargestComponentMask.nii"))

    return large_component_image

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


GetSegmented = True
# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    img_scoliosis = OpenScoliosis(scoliosis_path, "1preop.nii")
    image_array = sitk.GetArrayFromImage(img_scoliosis) #Image array has values based on Houndsfield units
    print("Maximal value " + str(np.max(image_array)) + " Minimal value " + str(np.min(image_array)))

    if GetSegmented == False:
        img_processed = SimpleSegmentation(img_scoliosis)
        sitk.WriteImage(img_processed, str(datapath / "mask_result.nii"))
    else:
        img_processed = sitk.ReadImage(str(datapath/"mask_result.nii"))


    mask = FilterLargestComponents(img_processed) #outputs image with numbers based on size
    ThresholdFilter.SetLowerThreshold(1)
    mask = ThresholdFilter.Execute(mask)

    segmentation_mask = sitk.GetArrayFromImage(mask)

    #Current implementation only works on slices without any different bones like shoulder blades
    slice_num = 100

    slice = segmentation_mask[slice_num,:,:]

    #ActiveContour(slice)

    canvas = np.zeros_like(slice)

    for i in range(slice_num, slice_num + 50,10):
        slice = segmentation_mask[i,:,:]

        hull_list, centroid_list = SingleSliceContour(slice)

        for i in range(len(centroid_list)):
            cv.drawContours(canvas, hull_list, i, color = (255,255,255))
            plt.scatter(centroid_list[i][0], centroid_list[i][1])

        centroid_list = np.array(centroid_list[1:])
        #Reordering the list
        centroid_left = centroid_list[centroid_list[:,0] < 512/2]
        centroid_right = centroid_list[centroid_list[:,0] >= 512/2]

        centroid_ordered = [np.append(np.flip(centroid_left, axis = 0), centroid_right, axis = 0)]

        cv.drawContours(canvas, centroid_ordered, 0, color = (255,0,0))

    plt.imshow(slice)
    plt.figure()
    plt.imshow(canvas)


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
