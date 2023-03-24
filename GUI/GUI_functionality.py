# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 17:15:37 2023

@author: 20182371
"""
import customtkinter 
import tkinter as tk 
from tkinter import filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
import os
import SimpleITK as sitk
import pandas as pd
from Tools.Deformity_Parameters import calculate_parameter
import Tools.Segmentation
import Tools.Contouring
import GUI.GUI_utils

from scipy.ndimage import gaussian_filter 
from skimage import feature
import math
import time 

import cv2 as cv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GUI_Functionality:
    
    def __init__(self, master, layout):
        self.master = master
        self.layout = layout
        
        #parameters
        self.non_segmented = "normal image"
        self.segmentation = "segmentation"
        self.map = "gray"
        self.coronal = "coronal"
        self.transverse = "transverse"
        self.plus = '+'
        self.minus = '-'
        self.assymetry_index = "Assymetry Index"
        self.trunk_rotation = "Angle Trunk Rotation"
        self.pectus_index = "Pectus Index"
        self.sagital_diameter = "Sagital Diameter"
        self.steep_vertebral = "Steep Vertebral"
        self.dict_landmark_num = {self.assymetry_index : [5,6,7,8], 
                                  self.trunk_rotation : [3,4], 
                                  self.pectus_index : [9,10,11,12],
                                  self.sagital_diameter: [11,13], 
                                  self.steep_vertebral: [11,12]}
        
        
        #Variables
        self.file_path = None
        self.image = None
        self.image_array = None
        self.segmented_image = None
        self.segmented_image_array = None
        self.trans_image_array = None
        self.trans_array_state = None
        self.coronal_image_array = None
        self.coronal_array_state = None
        self.trans_slice = 200
        self.coronal_slice = 135
        self.contour_points = None
        self.df_params = None
        self.param_value = None
        self.current_param = None
        self.dict_landmarks = {}
        self.dict_parameters = {}
        self.start_slice = None
        self.end_slice = None
        self.contour = False
        #self.contour_fig = None
        #self.contour_exists = False
        
        #---------------------------------------------- image frame buttons ----------------------------------------------
        self.button_open_image = self.layout.master.button_open_image
        self.button_open_image.bind('<Button-1>', lambda event: self.open_file())

        self.button_plus = self.layout.master.button_plus
        self.button_plus.bind('<Button-1>', lambda event: self.change_slice(self.transverse, self.plus))

        self.button_min = self.layout.master.button_min
        self.button_min.bind('<Button-1>', lambda event: self.change_slice(self.transverse, self.minus))

        self.button_forward = self.layout.master.button_forward
        self.button_forward.bind('<Button-1>', lambda event: self.change_slice(self.coronal, self.plus))

        self.button_backward = self.layout.master.button_backward
        self.button_backward.bind('<Button-1>', lambda event: self.change_slice(self.coronal, self.minus))

        self.button_goto_slice = self.layout.master.button_goto_slice
        self.button_goto_slice.bind('<Button-1>', lambda event: self.go_to_slice(self.transverse))

        self.coronal_button_goto_slice = self.layout.master.coronal_button_goto_slice
        self.coronal_button_goto_slice.bind('<Button-1>', lambda event: self.go_to_slice(self.coronal))
        
        #---------------------------------------------- manual parameter buttons -----------------------------------------
        self.button_assymetry_index = self.layout.master.button_assymetry_index
        self.button_assymetry_index.bind('<Button-1>', lambda event: self.get_parameter(self.assymetry_index, self.trans_slice))
        
        self.button_trunk_angle = self.layout.master.button_trunk_angle
        self.button_trunk_angle.bind('<Button-1>', lambda event: self.get_parameter(self.trunk_rotation, self.trans_slice))
        
        self.button_pectus_index = self.layout.master.button_pectus_index
        self.button_pectus_index.bind('<Button-1>', lambda event: self.get_parameter(self.pectus_index, self.trans_slice))
        
        self.button_sagital_diameter = self.layout.master.button_sagital_diameter
        self.button_sagital_diameter.bind('<Button-1>', lambda event: self.get_parameter(self.sagital_diameter, self.trans_slice))
        
        self.button_steep_vertebral = self.layout.master.button_steep_vertebral
        self.button_steep_vertebral.bind('<Button-1>', lambda event: self.get_parameter(self.steep_vertebral, self.trans_slice))
        
        self.button_save_parameters = self.layout.master.button_save_parameters
        self.button_save_parameters.bind('<Button-1>', lambda event: self.save_parameters())
        
        #---------------------------------------------- landmark extension buttons --------------------------------------
        self.button_begin = self.layout.master.button_begin
        self.button_begin.bind('<Button-1>', lambda event: self.set_slice("start", self.trans_slice))
        
        self.button_end = self.layout.master.button_end
        self.button_end.bind('<Button-1>', lambda event: self.set_slice("end", self.trans_slice))
        
        self.button_landmark_extension = self.layout.master.button_landmark_extension
        self.button_landmark_extension.bind('<Button-1>', lambda event: self.weighted_landmark_extension(self.start_slice, self.end_slice))
        
        self.button_change_landmarks = self.layout.master.button_change_landmarks
        self.button_change_landmarks.bind('<Button-1>', lambda event: self.change_landmarks(self.parameter_menu.get(), self.trans_slice))
        
        self.button_compute_parameters = self.layout.master.compute_parameters
        self.button_compute_parameters.bind('<Button-1>', lambda event: self.get_parameter(self.parameter_menu.get(), self.trans_slice, get_points = False))

        self.button_compute_rib_rotation = self.layout.master.button_compute_rib_rotation
        self.button_compute_rib_rotation.bind('<Button-1>', lambda event: self.computer_rib_rotation(self.dict_landmarks))
        
        #---------------------------------------------- segmentation buttons ---------------------------------------------
        self.button_segment = self.layout.master.button_segment
        self.button_segment.bind('<Button-1>', lambda event: self.automatic_segmentation())
        
        self.button_show_trans_segment = self.layout.master.button_show_trans_segment
        self.button_show_trans_segment.bind('<Button-1>', lambda event: self.change_image_view(self.transverse))
        
        self.button_show_coronal_segment = self.layout.master.button_show_coronal_segment
        self.button_show_coronal_segment.bind('<Button-1>', lambda event: self.change_image_view(self.coronal))
        
        self.button_calculate_contour = self.layout.master.button_calculate_contour
        self.button_calculate_contour.bind('<Button-1>', lambda event: self.draw_contour())
        
        self.button_remove_contour = self.layout.master.button_remove_contour
        self.button_remove_contour.bind('<Button-1>', lambda event: self.remove_contour())

        self.button_load_contour = self.layout.master.button_load_contour
        self.button_load_contour.bind('<Button-1>', lambda event: self.get_contour())

        self.button_auto_parameter = self.layout.master.button_auto_parameter
        self.button_auto_parameter.bind('<Button-1>', lambda event: self.get_contour_params(self.trans_slice))
        
        #----------------------------------------------------- entrys -----------------------------------------------------
        self.slice_entry = self.layout.master.slice_entry
        self.coronal_slice_entry = self.layout.master.coronal_slice_entry
        
        #----------------------------------------------------- menus ------------------------------------------------------
        self.parameter_menu = self.layout.master.parameter_menu
        
        #--------------------------------------------------- help button ---------------------------------------------
        self.button_help = self.layout.master.button_help 
        self.button_help.bind('<Button-1>', lambda event: self.help_button())
        
        #--------------------------------------------------- output table -------------------------------------------------
        self.output_table = self.layout.master.table

    
    
        
    def open_file(self):
        try:
            #open directory to find a file
            self.file_path = filedialog.askopenfile(title = "Open patient image")
        
            if os.path.splitext(self.file_path.name)[1] == '.nii':
                self.image = sitk.ReadImage(self.file_path.name)
                self.image_array = sitk.GetArrayFromImage(self.image)
                self.trans_image_array = self.image_array
                self.trans_array_state = self.non_segmented
                self.coronal_image_array = self.image_array
                self.coronal_array_state = self.non_segmented
                self.layout.draw_image(self.trans_image_array, self.coronal_image_array, self.trans_slice, self.coronal_slice, self.contour, self.map)
            else:
                messagebox.showinfo(title="Message", message="incorrect file type")
        except:
            messagebox.showerror("opening file", "Problem with opening the file, please try another one")
    
    def change_slice(self, view, direction): 
        if self.image_array is None:
            return

        if view == self.transverse: 
            if self.trans_slice < 0 and self.trans_slice > np.shape(self.image_array)[0]:
                return

            if direction == self.plus: 
                self.trans_slice += 1
            elif direction == self.minus: 
                self.trans_slice -= 1

        elif view == self.coronal: 
            if self.coronal_slice < 0 and self.coronal_slice > np.shape(self.image_array)[0]:
                return

            if direction == self.plus: 
                self.coronal_slice += 1
            elif direction == self.minus: 
                self.coronal_slice -= 1

        self.layout.draw_image(self.trans_image_array, self.coronal_image_array, self.trans_slice, self.coronal_slice, self.contour, self.map)
        self.layout.show_landmarks(self.image_array, self.trans_slice, self.coronal_slice, self.dict_landmarks, self.map)
    
    def go_to_slice(self, view):
        try:
            if view == self.transverse:
                dialog_input = self.slice_entry.get()
                self.trans_slice = int(dialog_input)
            elif view == self.coronal: 
                dialog_input = self.coronal_slice_entry.get()
                self.coronal_slice = int(dialog_input)
        except ValueError:
            # error message if the input is not an integer
            messagebox.showinfo(title="Message", message="Must input an integer to change the slice.")
        else:
            if self.image_array is not None:
                # check if the slice number is within the range of the image
                if 0 <= self.trans_slice <= np.shape(self.image_array)[0] and 0 <= self.coronal_slice <= np.shape(self.image_array)[0] :
                    self.layout.draw_image(self.trans_image_array, self.coronal_image_array, self.trans_slice, self.coronal_slice, self.contour, self.map)
                    self.layout.show_landmarks(self.image_array, self.trans_slice, self.coronal_slice, self.dict_landmarks, self.map)
                else:
                    # error message in the text frame that the slice number is out of range
                    messagebox.showinfo(title="Message", message="Slice is out of range.")
        finally:
            self.slice_entry.delete(0, "end")
            self.coronal_slice_entry.delete(0, "end")
    
    def change_image_view(self, view):
        if self.segmented_image_array is not None: 
            
            if view == self.transverse:
                if self.trans_array_state == self.non_segmented:
                    self.trans_image_array = self.segmented_image_array
                    self.trans_array_state = self.segmentation
                elif self.trans_array_state == self.segmentation:
                    self.trans_image_array = self.image_array
                    self.trans_array_state = self.non_segmented
            elif view == self.coronal:
                if self.coronal_array_state == self.non_segmented: 
                    self.coronal_image_array = self.segmented_image_array
                    self.coronal_array_state = self.segmentation
                elif self.coronal_array_state == self.segmentation:
                    self.coronal_image_array = self.image_array
                    self.coronal_array_state = self.non_segmented
            
            self.layout.draw_image(self.trans_image_array, self.coronal_image_array, self.trans_slice, self.coronal_slice, self.contour, self.map)
            
    def set_slice(self, position, slice_number):
        if position == "start":
            if self.end_slice == None or self.end_slice > slice_number:
                self.start_slice = slice_number
            else: 
                messagebox.showinfo(title="Error", message="Starting slice has to come before the end slice")
            
        elif position == "end":
            if self.start_slice == None or self.start_slice < slice_number:
                self.end_slice = slice_number
            else:
                messagebox.showinfo(title="Error", message="End slice has to come after the starting slice")
    
    def get_points(self, parameter, slice_num):
        #show the image in new window
        plt.imshow(self.image_array[slice_num, :, :],cmap=self.map)
        plt.gca().invert_yaxis()

        
        #retreive points
        points = []
        points = np.asarray(plt.ginput(len(self.dict_landmark_num[parameter]), timeout=-1))
        plt.close()
        
        if f"slice_{slice_num}" not in self.dict_landmarks:
            # If the key doesn't exist, create it with an empty dictionary as its value
            self.dict_landmarks[f"slice_{slice_num}"] = {}
            
        if parameter == self.trunk_rotation:
            self.dict_landmarks[f"slice_{slice_num}"]["point_3"] = points[0,:].astype(int)
            self.dict_landmarks[f"slice_{slice_num}"]["point_4"] = points[1,:].astype(int)
        elif parameter == self.assymetry_index: 
            self.dict_landmarks[f"slice_{slice_num}"]["point_5"] = points[0,:].astype(int)
            self.dict_landmarks[f"slice_{slice_num}"]["point_6"] = points[1,:].astype(int)
            self.dict_landmarks[f"slice_{slice_num}"]["point_7"] = points[2,:].astype(int)
            self.dict_landmarks[f"slice_{slice_num}"]["point_8"] = points[3,:].astype(int)
        elif parameter == self.pectus_index: 
            self.dict_landmarks[f"slice_{slice_num}"]["point_9"] = points[0,:].astype(int)
            self.dict_landmarks[f"slice_{slice_num}"]["point_10"] = points[1,:].astype(int)
            self.dict_landmarks[f"slice_{slice_num}"]["point_11"] = points[2,:].astype(int)
            self.dict_landmarks[f"slice_{slice_num}"]["point_12"] = points[3,:].astype(int)
        elif parameter == self.sagital_diameter: 
            self.dict_landmarks[f"slice_{slice_num}"]["point_11"] = points[0,:].astype(int)
            self.dict_landmarks[f"slice_{slice_num}"]["point_13"] = points[1,:].astype(int)
        elif parameter == self.steep_vertebral:
            self.dict_landmarks[f"slice_{slice_num}"]["point_11"] = points[0,:].astype(int)
            self.dict_landmarks[f"slice_{slice_num}"]["point_12"] = points[1,:].astype(int)
        
        return points

    def get_parameter(self, parameter, slice_number, get_points = True):
        self.current_param = parameter
        if self.image_array is not None:
            if get_points == True:
                self.get_points(parameter, slice_number)
                self.layout.show_landmarks(self.image_array, self.trans_slice, self.coronal_slice, self.dict_landmarks, self.map)
            
            param_value = round(calculate_parameter(self.dict_landmarks, parameter, slice_number),3) 
            self.add_parameter(parameter, param_value, slice_number)
            self.output_table.insert(parent= '', index = tk.END, values = (parameter, param_value, slice_number))
        else:
            messagebox.showinfo(title="Message", message="must open image first")
        
    def add_parameter(self, parameter, param_value, slice_number):
        if self.df_params is None:  
            self.df_params = pd.DataFrame({'Parameter': [], 'Value': [], "Slice":[]})
            
        new_row = {'Parameter': parameter, 'Value': param_value, "Slice": slice_number}
        self.df_params = self.df_params.append(new_row, ignore_index=True)

        if f"slice_{slice_number}" not in self.dict_parameters:
            # If the key doesn't exist, create it with an empty dictionary as its value
            self.dict_parameters[f"{slice_number}"] = {}
            
        self.dict_parameters[f"{slice_number}"][f"{parameter}"] = param_value
        
    def save_parameters(self):
        if self.df_params is not None:
            dialog = customtkinter.CTkInputDialog(text="give a name for the file:", title="save parameters")
            file_name = dialog.get_input()
            self.df_params.to_csv(f'{file_name}.csv', index=False)
    
    def weighted_landmark_extension(self, start_slice, end_slice):
        parameter = self.parameter_menu.get()
        
        #retreive the input seed and put them into the point dicts
        #save the slice used for seed in the original_seeds list
        original_seeds = []
        for i in range(start_slice, end_slice, 25):
            self.get_points(parameter, i)
            original_seeds.append(i)
        
        window, progressbar = self.progressbar("Landmark Extension")
        window.update()
        
        progress = 0
        for point in self.dict_landmark_num[parameter]:
            for n_seed in range(0,len(original_seeds)-1, 1):
                up_seed = []
                down_seed = []
                prev_seed = self.dict_landmarks[f"slice_{original_seeds[n_seed]}"][f"point_{point}"]
                
                for i in range(original_seeds[n_seed]+1, original_seeds[n_seed+1], 1):
                    next_seed = GUI.GUI_utils.GetNextSeed(self.image_array[i,:,:], prev_seed)
                    up_seed.append(next_seed)
                    prev_seed = next_seed
                
                prev_seed = self.dict_landmarks[f"slice_{original_seeds[n_seed+1]}"][f"point_{point}"]
                
                for j in range(original_seeds[n_seed+1]+1, original_seeds[n_seed], -1):
                    next_seed = GUI.GUI_utils.GetNextSeed(self.image_array[j,:,:], prev_seed)
                    down_seed.append(next_seed)
                    prev_seed = next_seed
                
                print(len(up_seed))
                for k in range(len(up_seed)): 
                    seed_x = ((23-1-k) * up_seed[k][0] + (k+1) * down_seed[-k][0])/23
                    seed_y = ((23-1-k) * up_seed[k][1] + (k+1)* down_seed[-k][1])/23
                    seed = (seed_x, seed_y)
                    
                    if f"slice_{original_seeds[n_seed]+k+1}" not in self.dict_landmarks:
                        # If the key doesn't exist, create it with an empty dictionary as its value
                        self.dict_landmarks[f"slice_{original_seeds[n_seed]+k+1}"] = {}
                        
                    self.dict_landmarks[f"slice_{original_seeds[n_seed]+k+1}"][f"point_{point}"] = seed
            progress += 1/len(self.dict_landmark_num[parameter])
            progressbar.set(progress)
            window.update()
        
        time.sleep(2)
        window.destroy()
        
    def change_landmarks(self,parameter, slice_number):
        self.get_points(parameter, slice_number)    
        
    def computer_rib_rotation(self, dict_landmarks):
        for i in range(np.shape(self.image_array)[0]):
            if f"slice_{i}" in dict_landmarks:
                if "point_3" in self.dict_landmarks[f"slice_{i}"] and "point_4" in self.dict_landmarks[f"slice_{i}"]:
                      img = self.image_array[i, :, :]


    def automatic_segmentation(self):
        if self.image_array is None:
            messagebox.showinfo(title="Message", message="Please first select an image")
            return

        segmented_image = Tools.Segmentation.SimpleSegmentation(self.image, threshold=150, OpeningSize=1, ClosingSize=2)
        self.segmented_image = Tools.Segmentation.FilterLargestComponents(segmented_image)
        self.segmented_image_array = sitk.GetArrayFromImage(self.segmented_image)
        
        #save segmentation
        filename = str(os.getcwd() + "/Segmented" + os.path.split(self.file_path.name)[1])
        sitk.WriteImage(self.segmented_image, fileName=filename)
        messagebox.showinfo("Segmentation", "Segmentation completed, image placed at " + filename)
    
        return

    def draw_contour(self):
        if self.segmented_image_array is None: 
            messagebox.showerror("Contouring", "must segement the image first")
            return 
        
        self.contour = True 
        self.layout.draw_image(self.trans_image_array, self.coronal_image_array, self.trans_slice, self.coronal_slice, self.contour, self.map)
        
    
    def remove_contour(self):
        self.contour = False 
        self.layout.draw_image(self.trans_image_array, self.coronal_image_array, self.trans_slice, self.coronal_slice, self.contour, self.map)
        
        
    

    def get_contour(self):
        #Get contour from CSO file
        print("Getting contour")
        contour_path = filedialog.askopenfile(title="Open contour file")
        try:
            #Does not work quite yet
            f = os.open(contour_path.name, os.O_RDONLY)
            contour = os.read(f, 1000)
            print(contour.decode('utf-8'))
            os.close(f)
        except:
            messagebox.showerror("Contouring", "Problem with opening the file, please try another one")

        print(contour)

        return

    def get_contour_params(self, slice_number):
        if self.image_array is None:
            messagebox.showerror("Parameters", "Please calculate or load the contour first")
            return

        if f"slice_{slice_number}" not in self.dict_landmarks:
            # If the key doesn't exist, create it with an empty dictionary as its value
            self.dict_landmarks[f"slice_{slice_number}"] = {}

        image_half = np.array(self.image_array.shape)/2

        #Split the image in right and left points
        Left_points = self.contour_points[self.contour_points[:,0] < image_half[-1]]
        Left_top = Left_points[np.argmin(Left_points[:,1]),:]

        Right_points = self.contour_points[self.contour_points[:,0] > image_half[-1]]
        Right_top = Right_points[np.argmin(Right_points[:,1]),:]

        self.dict_landmarks[f"slice_{slice_number}"]["point_3"] = Right_top.astype(int)
        self.dict_landmarks[f"slice_{slice_number}"]["point_4"] = Left_top.astype(int)

        self.get_parameter("Angle Trunk Rotation", slice_number, get_points=False)

        #Pectus index
        maxdist = 0
        leftmaxidx = 0
        rightmaxidx = 0
        #quick solution that does not take all edge cases into account, like points that are not opposite of eachother
        # for i, (x,y) in enumerate(Left_points):
        #     #Find the two points on the left and right that are the farthest apart
        #     idx = (np.abs(Right_points[:,1] - y).argmin())
        #     xdist = np.abs(x - Right_points[idx,0])
        #     if xdist > maxdist:
        #         maxdist = xdist
        #         leftmaxidx = i
        #         rightmaxidx = idx
        #
        # leftmaxPoint = Left_points[leftmaxidx]
        # rightmaxPoint = Right_points[rightmaxidx]
        maxdist, leftmaxPoint, rightmaxPoint = Tools.Deformity_Parameters.Find_Longest(Left_points, Right_points)

        self.dict_landmarks[f"slice_{slice_number}"]["point_9"] = Left_points[leftmaxidx].astype(int)
        self.dict_landmarks[f"slice_{slice_number}"]["point_10"] = Right_points[rightmaxidx].astype(int)

        #TODO calculate the sternum and top of vertebra, but the segmentation does not yet allow for that

        #Asymmetry index
        TopRight_points = Right_points[Right_points[:,1] < image_half[-2]] #divide the contour into quarters, pay attention to the flipped axis!
        BotRight_points = Right_points[Right_points[:,1] > image_half[-2]]
        TopLeft_points = Left_points[Left_points[:,1] < image_half[-2]]
        BotLeft_points = Left_points[Left_points[:,1] > image_half[-2]]

        #Does not interpolate between contour points yet
        maxdist, maxright, minright = Tools.Deformity_Parameters.Find_Longest(TopRight_points, BotRight_points, c = 1)
        maxdist, maxleft, minleft = Tools.Deformity_Parameters.Find_Longest(TopLeft_points, BotLeft_points, c = 1)

        self.dict_landmarks[f"slice_{slice_number}"]["point_5"] = maxright.astype(int)
        self.dict_landmarks[f"slice_{slice_number}"]["point_6"] = minright.astype(int)
        self.dict_landmarks[f"slice_{slice_number}"]["point_7"] = maxleft.astype(int)
        self.dict_landmarks[f"slice_{slice_number}"]["point_8"] = minleft.astype(int)

        self.get_parameter("Assymetry Index", slice_number, get_points=False)

        #Quick debug plot
        plt.figure()
        plt.imshow(sitk.GetArrayFromImage(self.segmented_image)[slice_number,:,:])
        plt.scatter(self.contour_points[:,0], self.contour_points[:,1], s=1)
        plt.scatter([maxright[0], maxleft[0]], [maxright[1], maxleft[1]], c = 'b')
        plt.scatter([minright[0], minleft[0]], [minright[1], minleft[1]], c = 'r')
        plt.show()


        return

    def progressbar(self, label):
        window = customtkinter.CTkToplevel(self.master)
        self.master.eval(f"tk::PlaceWindow {str(window)} center")

        window.title(label + " progress")
        window.geometry("300x150")
        customtkinter.CTkLabel(window, text = "Please wait for " + label).pack()
        # progressbar
        pb = customtkinter.CTkProgressBar(master = window, mode = "determinate")
        # place the progressbar
        pb.pack()

        #Make sure the progress bar is set and the window updated
        window.grab_set()
        pb.set(0)
        pb.start()
        window.update()
        return window, pb
    
    def help_button(self):
       
       # configure window 
       self.window = customtkinter.CTk()
       self.window.title("Help page")

       self.window.mainloop()


"""def calc_contour(self):
    if self.segmented_image is None:
        segmentation_path = filedialog.askopenfile(title="Open segmentation image")
        try:
            self.segmented_image = sitk.ReadImage(segmentation_path.name)
            self.image_array = sitk.GetArrayFromImage(self.segmented_image)
        except:
            messagebox.showerror("Contouring", "Problem with loading the image, please try a different one")
    try:
        centroids = Tools.Contouring.MultiSliceContour(sitk.GetArrayFromImage(self.segmented_image), self.trans_slice)
    except:
        messagebox.showerror("Contouring", "Problem with retrieving contour, please try a different segmentation")
    
    self.draw_contour(self.trans_slice, centroids)
    self.contour_exists = True"""

"""def draw_contour_test(self, slice_num, centroids): 
    slice = sitk.GetArrayFromImage(self.segmented_image)[slice_num, :, :]
    canvas = np.zeros_like(slice)
    
    if self.contour_fig is not None:
        self.contour_fig.clf()
        plt.close(self.contour_fig)
    
    self.contour_fig = plt.figure()

    hull = cv.convexHull(centroids[1:])
    cv.drawContours(canvas, [hull], 0, color = (255,255,255), thickness= 1)
    plt.scatter(hull[:,0,0], hull[:,0,1], c = "blue")
    plt.axis("off", emit = False)
    plt.imshow(canvas, alpha = 1, cmap= "gray")
    plt.imshow(slice, alpha= 0.3, cmap = "gray", vmax = 1)

    #Only takes hull, as there is a lot of noise because of the multiple slices
    self.contour_points = hull.reshape((-1,2))
    
    #Move large canvas out of the way to display the contouring canvas next to it
    self.layout.master.canvas.get_tk_widget().grid(row=1, column=0, columnspan=3, padx=(10,10), pady=(0,10), sticky = 'nwes')

    self.master.canvas2 = FigureCanvasTkAgg(self.contour_fig, master=self.layout.master.image_frame)  # A tk.DrawingArea.
    self.master.canvas2.draw()
    self.layout.master.canvas2.get_tk_widget().grid(row=1, column=3, columnspan=3, padx=(10, 10), pady=(0, 10),
                                                   sticky='news')
    return"""

"""def remove_contour(self):
    self.contour_fig.clf()
    plt.close(self.contour_fig)
    #self.master.canvas2.draw()
    
    self.master.canvas2.get_tk_widget().grid_forget()  # Remove the old canvas widget
    self.master.canvas2.draw()
    #self.master.canvas2 = None
    self.contour_exists = False
    self.layout.master.canvas.get_tk_widget().grid(row=1, column=0, columnspan=6, padx=(10,10), pady=(0,10), sticky='nwes')"""