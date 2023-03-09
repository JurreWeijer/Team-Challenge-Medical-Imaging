import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
import SimpleITK as sitk
import cv2 as cv
import warnings

import skimage.segmentation as seg
import scipy.optimize as optim

#Make sure you run the segmentation before this, so this image exists
MaskFile = "LargestComponent.nii"

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
ClosingFilter = sitk.BinaryMorphologicalClosingImageFilter()

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

def SingleSliceContour(slice, plot = False):
    #Compute the contour of each blob on a single slice using the OpenCV toolkit
    #Adapted from the hull tutorial https://docs.opencv.org/3.4.2/d7/d1d/tutorial_hull.html

    canny_output = cv.Canny(image = slice, threshold1=0.5, threshold2=2)

    try:
        contours, hierarchy = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    except:
        raise RuntimeError(
            "cv.findContours not working, most likely a wrong version of OpenCV, program was written for >4.0.0")

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

    if (plot == True):
        cmap = plt.cm.get_cmap("hsv", len(hull_list))
        canvas = np.zeros_like(slice)

        plt.figure()
        for i in range(len(hull_list)):
            plt.scatter(centroid_list[i][0], centroid_list[i][1], marker='P', color=cmap(i), s=4)
            plt.scatter(hull_list[i][:, 0, 0], hull_list[i][:, 0, 1], color=cmap(i), s=2)

        plt.figure()

        for i in range(len(centroid_list)):
            cv.drawContours(canvas, hull_list, i, color = (255,255,255))
            plt.scatter(centroid_list[i][0], centroid_list[i][1])

        centroid_list = np.array(centroid_list)
        centroid_left = centroid_list[centroid_list[:, 0] < 512 / 2]
        centroid_right = centroid_list[centroid_list[:, 0] >= 512 / 2]

        centroid_ordered = [np.append(np.flip(centroid_left, axis = 0), centroid_right, axis = 0)]

        cv.drawContours(canvas, centroid_ordered, 0, color = (255,0,0))

        plt.imshow(canvas)

    return hull_list, centroid_list

def MultiSliceContour(image_array, slice_num = 100, plot = False):
    Multi_slice_centroids = np.empty((1,1,2), dtype = np.int32)

    #Get centroids for multiple slices and put them in a single array
    for i in range(slice_num, slice_num + 50,10):
        slice = image_array[i,:,:]

        hull_list, centroid_list = SingleSliceContour(slice)

        centroid_array = np.array(centroid_list)
        centroid_array = centroid_array[np.all(centroid_array != 0, axis = 1)]

        Multi_slice_centroids = np.append(Multi_slice_centroids, np.reshape(centroid_array, (len(centroid_array), 1, 2)), axis = 0)

    #Plot results if necessary
    if (plot == True):
        canvas = np.zeros_like(slice)
        plt.figure()
        hull = cv.convexHull(Multi_slice_centroids[1:])
        cv.drawContours(canvas, [hull], 0, color = (255,255,255), thickness= 1)
        plt.scatter(hull[:,0,0], hull[:,0,1], c = "blue")
        plt.scatter(Multi_slice_centroids[1:,0,0], Multi_slice_centroids[1:,0,1], s = 1, c = "red")
        plt.imshow(canvas, alpha = 1)
        plt.imshow(slice, alpha= 0.3, cmap = "gray")

    return Multi_slice_centroids

if __name__ == '__main__':

    img_scoliosis = OpenScoliosis(scoliosis_path, "1preop.nii")
    image_array = sitk.GetArrayFromImage(img_scoliosis) #Image array has values based on Houndsfield units

    try:
        #Make sure you run the segmentation before this, so this image exists
        mask = sitk.ReadImage(str(datapath/MaskFile))
    except:
        raise RuntimeError("MaskFile not found, make sure you have run the segmentation and that the file exists at " + str(datapath/MaskFile))

    segmentation_mask = sitk.GetArrayFromImage(mask)

    segmentation_mask = segmentation_mask.astype(dtype = np.uint8)

    slice_num = 100

    slice = segmentation_mask[slice_num,:,:]

    #Current implementation only works on slices without any different bones like shoulder blades
    MultiSliceContour(segmentation_mask, slice_num, True)
    #ActiveContour(image_array[slice_num,:,:])

    plt.figure()
    plt.imshow(slice)

    plt.show()
