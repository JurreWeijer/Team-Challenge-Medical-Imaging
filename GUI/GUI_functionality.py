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
from scipy.ndimage import gaussian_filter 
from skimage import feature
import math


class GUI_Functionality:
    
    def __init__(self, master, layout):
        self.master = master
        self.layout = layout
        
        #Variables
        self.image_array = None
        self.slice_number = 200
        self.map = "gray"
        self.df_params = None
        self.param_value = None
        self.current_param = None
        self.dict_landmarks = {}
        self.dict_parameters = {}
        self.start_slice = None
        self.end_slice = None
        
        #parameters
        self.assymetry_index = "assymetry index"
        self.trunk_rotation = "angle trunk rotation"
        self.pectus_index = "pectus index"
        self.sagital_diameter = "sagital diameter"
        self.steep_vertebral = "steep vertebral"
        self.dict_num_points = {self.assymetry_index : 4,
                                self.trunk_rotation: 2,
                                self.pectus_index: 4, 
                                self.sagital_diameter: 2, 
                                self.steep_vertebral: 2}
        self.dict_landmark_num = {self.assymetry_index : [5,6,7,8], 
                                  self.trunk_rotation : [3,4], 
                                  self.pectus_index : [9,10,11,12],
                                  self.sagital_diameter: [11,13], 
                                  self.steep_vertebral: [11,12]}
        
        #Buttons
        self.button_open_image = self.layout.master.button_open_image
        self.button_open_image.bind('<Button-1>', lambda event: self.open_file())
        
        self.button_plus = self.layout.master.button_plus
        self.button_plus.bind('<Button-1>', lambda event: self.next_slice())
        
        self.button_min = self.layout.master.button_min
        self.button_min.bind('<Button-1>', lambda event: self.previous_slice())
        
        self.button_goto_slice = self.layout.master.button_goto_slice
        self.button_goto_slice.bind('<Button-1>', lambda event: self.go_to_slice())
        
        self.button_assymetry_index = self.layout.master.button_assymetry_index
        self.button_assymetry_index.bind('<Button-1>', lambda event: self.get_parameter(self.assymetry_index, self.slice_number))
        
        self.button_trunk_angle = self.layout.master.button_trunk_angle
        self.button_trunk_angle.bind('<Button-1>', lambda event: self.get_parameter(self.trunk_rotation, self.slice_number))
        
        self.button_pectus_index = self.layout.master.button_pectus_index
        self.button_pectus_index.bind('<Button-1>', lambda event: self.get_parameter(self.pectus_index, self.slice_number))
        
        self.button_sagital_diameter = self.layout.master.button_sagital_diameter
        self.button_sagital_diameter.bind('<Button-1>', lambda event: self.get_parameter(self.sagital_diameter, self.slice_number))
        
        self.button_steep_vertebral = self.layout.master.button_steep_vertebral
        self.button_steep_vertebral.bind('<Button-1>', lambda event: self.get_parameter(self.steep_vertebral, self.slice_number))
        
        self.button_save_parameters = self.layout.master.button_save_parameters
        self.button_save_parameters.bind('<Button-1>', lambda event: self.save_parameters())
        
        self.button_begin = self.layout.master.button_begin
        self.button_begin.bind('<Button-1>', lambda event: self.set_slice("start", self.slice_number))
        
        self.button_end = self.layout.master.button_end
        self.button_end.bind('<Button-1>', lambda event: self.set_slice("end", self.slice_number))
        
        self.button_landmark_extension = self.layout.master.button_landmark_extension
        self.button_landmark_extension.bind('<Button-1>', lambda event: self.landmark_extension(self.start_slice, self.end_slice))
        
        self.button_compute_parameters = self.layout.master.compute_parameters
        self.button_compute_parameters.bind('<Button-1>', lambda event: self.test())
        
        #entrys
        self.slice_entry = self.layout.master.slice_entry
        self.parameter_menu = self.layout.master.parameter_menu
        
        #table 
        self.output_table = self.layout.master.table

            
    def open_file(self):
        #open directory to find a file
        file_path = filedialog.askopenfile()
        
        if os.path.splitext(file_path.name)[1] == '.nii':
            image = sitk.ReadImage(file_path.name)
            self.image_array = sitk.GetArrayFromImage(image)
            self.layout.draw_image(self.image_array, self.slice_number, self.map)
        else:
            messagebox.showinfo(title="Message", message="incorrect file type")
            
    def next_slice(self):
        if self.image_array is not None:
            if 0 < self.slice_number < np.shape(self.image_array)[0]:
                self.slice_number += 1
                self.layout.draw_image(self.image_array, self.slice_number, self.map)
                self.layout.show_landmarks(self.slice_number, self.dict_landmarks)
    
    def previous_slice(self):
        if self.image_array is not None:
            if 0 < self.slice_number < np.shape(self.image_array)[0]:
                self.slice_number -= 1
                self.layout.draw_image(self.image_array, self.slice_number, self.map)
                self.layout.show_landmarks(self.slice_number, self.dict_landmarks)
    
    def go_to_slice(self):
        try:
            dialog_input = self.slice_entry.get()
            self.slice_number = int(dialog_input)
        except ValueError:
            # error message if the input is not an integer
            messagebox.showinfo(title="Message", message="Must input an integer to change the slice.")
        else:
            if self.image_array is not None:
                # check if the slice number is within the range of the image
                if 0 <= self.slice_number <= np.shape(self.image_array)[0]:
                    self.layout.draw_image(self.image_array, self.slice_number, self.map)
                    self.layout.show_landmarks(self.slice_number, self.dict_landmarks)
                else:
                    # error message in the text frame that the slice number is out of range
                    messagebox.showinfo(title="Message", message="Slice is out of range.")
        finally:
            self.slice_entry.delete(0, "end")
            
    
    def set_slice(self, position, slice_number):
        if position == "start":
            if self.end_slice == None or self.end_slice > slice_number:
                self.start_slice = slice_number
                print(self.start_slice)
            else: 
                messagebox.showinfo(title="Error", message="Starting slice has to come before the end slice")
            
        elif position == "end":
            if self.start_slice == None or self.start_slice < slice_number:
                self.end_slice = slice_number
                print(self.end_slice)
            else:
                messagebox.showinfo(title="Error", message="End slice has to come after the starting slice")
    
    def get_points(self, parameter, slice_num):
        #show the image in new window
        plt.imshow(self.image_array[slice_num, :, :],cmap=self.map)

        #retreive points
        points = []
        points = np.asarray(plt.ginput(self.dict_num_points[parameter], timeout=-1))

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
        
        #display the marked point in the GUI
        #self.layout.draw_landmarks(pts)
        
        return points

    def get_parameter(self, parameter, slice_number):
        self.current_param = parameter
        if self.image_array is not None:
            self.get_points(parameter, slice_number)
            
            self.layout.show_landmarks(slice_number, self.dict_landmarks)

            param_value = round(calculate_parameter(self.dict_landmarks, parameter, slice_number),3)
            print(param_value)
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
            
    def landmark_extension(self, start_slice, end_slice):
        test = self.parameter_menu.get()
        print(test)
        parameter = self.assymetry_index
        
        #retreive the input seed and put them into the point dicts
        #save the slice used for seed in the original_seeds list
        original_seeds = []
        for i in range(start_slice, end_slice, 50):
            self.get_points(parameter, i)
            original_seeds.append(i)
        
        for point in self.dict_landmark_num[parameter]:
            n_seed = 0
            prev_seed = self.dict_landmarks[f"slice_{original_seeds[n_seed]}"][f"point_{point}"]
            print(prev_seed.dtype)
            for i in range(26):
                next_seed = self.GetNextSeed(self.image_array[start_slice+i+1,:,:], prev_seed)
                
                if f"slice_{original_seeds[0]+i}" not in self.dict_landmarks:
                    # If the key doesn't exist, create it with an empty dictionary as its value
                    self.dict_landmarks[f"slice_{original_seeds[n_seed]+i}"] = {}
                    
                self.dict_landmarks[f"slice_{original_seeds[n_seed]+i}"][f"point_{point}"] = next_seed  
                prev_seed = next_seed
            
            
            #after first 25 propagate from next seed up
            for i in range(start_slice+50,end_slice, 50):
                n_seed += 1
                
                prev_seed = self.dict_landmarks[f"slice_{original_seeds[n_seed]}"][f"point_{point}"]

                for j in range(25):
                    next_seed = self.GetNextSeed(self.image_array[start_slice+j-1,:,:], prev_seed)
                    
                    if f"slice_{original_seeds[n_seed]-j}" not in self.dict_landmarks:
                        # If the key doesn't exist, create it with an empty dictionary as its value
                        self.dict_landmarks[f"slice_{original_seeds[n_seed]-j}"] = {}
                        
                    self.dict_landmarks[f"slice_{original_seeds[n_seed]-j}"][f"point_{point}"] = next_seed  
                    prev_seed = next_seed
                
                #set prev_seed back to input seed point
                prev_seed = self.dict_landmarks[f"slice_{original_seeds[n_seed]}"][f"point_{point}"]
                
                for k in range(26):
                    next_seed = self.GetNextSeed(self.image_array[start_slice+k+1,:,:], prev_seed)
                    
                    if f"slice_{original_seeds[n_seed]+k}" not in self.dict_landmarks:
                        # If the key doesn't exist, create it with an empty dictionary as its value
                        self.dict_landmarks[f"slice_{original_seeds[n_seed]+k}"] = {}
                        
                    self.dict_landmarks[f"slice_{original_seeds[n_seed]+k}"][f"point_{point}"] = next_seed  
                    prev_seed = next_seed
                
       
        
    
    def GetNextSeed(self, work_slice, seed):
        
        seedx = seed[0]
        seedy = seed[1]
        
        gaussian = gaussian_filter(work_slice, sigma=3)
        edges1 = feature.canny(gaussian, sigma = 3)
        #window = edges1[seedy-100:seedy+100,seedx-100:seedx+100]
        
        #find closest gradient points within an increading radius i 
        i = 1
        near_points = []
        looking = True
        while(looking):
            for k in range((seedx-i),(seedx+i+1)):
                for j in range(seedy-i,seedy+i+1):
                    if edges1[k,j]:
                        near_points.append((k,j))
            i += 1
            if len(near_points) != 0:
                looking = False
            #stops looking when we find the first gradient points 
            
        # now we need to determine which one is the closest
        #get the euclidean distance from all and decide on the new seed
        min_distance = math.dist((seedx,seedy), (near_points[0]))
        next_seed = near_points[0]
        for point in near_points:
            if math.dist((seedx,seedy), point) < min_distance:
                min_distance = math.dist((seedx,seedy), point)
                next_seed = point
                

            
        return next_seed 
    
    def test(self):
        test = self.parameter_menu.get()
        print(test)
    
"""
    def calc_assymetry_index(self):
        self.current_param = self.assymetry_index
        if self.image_array is not None:
            pts = self.get_points(self.assymetry_index)
            
            if f"slice_{self.slice_number}" not in self.dict_landmarks:
                # If the key doesn't exist, create it with an empty dictionary as its value
                self.dict_landmarks[f"slice_{self.slice_number}"] = {}
                
            self.dict_landmarks[f"slice_{self.slice_number}"]["point_5"] = pts[0,:]
            self.dict_landmarks[f"slice_{self.slice_number}"]["point_6"] = pts[1,:]
            self.dict_landmarks[f"slice_{self.slice_number}"]["point_7"] = pts[2,:]
            self.dict_landmarks[f"slice_{self.slice_number}"]["point_8"] = pts[3,:]
            
            self.layout.show_landmarks(self.slice_number, self.dict_landmarks)

            self.param_value = round(calculate_parameter(self.dict_landmarks, self.current_param, self.slice_number),3)
            
            self.add_parameter()
            self.output_table.insert(parent= '', index = tk.END, values = (self.current_param, self.param_value, self.slice_number))
        else:
            messagebox.showinfo(title="Message", message="must open image first")
    
    def calc_trunk_angle(self):
        self.current_param = self.trunk_rotation
        if self.image_array is not None:
            pts = self.get_points(self.trunk_rotation)
            
            
            if f"slice_{self.slice_number}" not in self.dict_landmarks:
                # If the key doesn't exist, create it with an empty dictionary as its value
                self.dict_landmarks[f"slice_{self.slice_number}"] = {}
                
            self.dict_landmarks[f"slice_{self.slice_number}"]["point_3"] = pts[0,:]
            self.dict_landmarks[f"slice_{self.slice_number}"]["point_4"] = pts[1,:]
            
            self.layout.show_landmarks(self.slice_number, self.dict_landmarks)
            
            self.param_value = round(calculate_parameter(self.dict_landmarks, self.current_param, self.slice_number),3)
            
            self.add_parameter()
            self.output_table.insert(parent= '', index = tk.END, values = (self.current_param, self.param_value, self.slice_number))
        else:
            messagebox.showinfo(title="Message", message="must open image first")
    
    def calc_pectus_index(self):
        self.current_param = self.pectus_index
        if self.image_array is not None:
            pts = self.get_points(self.pectus_index)
            
            if f"slice_{self.slice_number}" not in self.dict_landmarks:
                # If the key doesn't exist, create it with an empty dictionary as its value
                self.dict_landmarks[f"slice_{self.slice_number}"] = {}
                
            self.dict_landmarks[f"slice_{self.slice_number}"]["point_9"] = pts[0,:]
            self.dict_landmarks[f"slice_{self.slice_number}"]["point_10"] = pts[1,:]
            self.dict_landmarks[f"slice_{self.slice_number}"]["point_11"] = pts[2,:]
            self.dict_landmarks[f"slice_{self.slice_number}"]["point_12"] = pts[3,:]
            
            self.layout.show_landmarks(self.slice_number, self.dict_landmarks)
            
            self.param_value = round(calculate_parameter(self.dict_landmarks, self.current_param, self.slice_number),3)
            
            self.add_parameter()
            self.output_table.insert(parent= '', index = tk.END, values = (self.current_param, self.param_value, self.slice_number))
        else:
            messagebox.showinfo(title="Message", message="must open image first")
    
    def calc_sagital_diameter(self):
        self.current_param = self.sagital_diameter
        if self.image_array is not None:
            pts = self.get_points(self.sagital_diameter)
            
            
            if f"slice_{self.slice_number}" not in self.dict_landmarks:
                # If the key doesn't exist, create it with an empty dictionary as its value
                self.dict_landmarks[f"slice_{self.slice_number}"] = {}
                
            self.dict_landmarks[f"slice_{self.slice_number}"]["point_11"] = pts[0,:]
            self.dict_landmarks[f"slice_{self.slice_number}"]["point_13"] = pts[1,:]
            
            
            self.layout.show_landmarks(self.slice_number, self.dict_landmarks)
            
            self.param_value = round(calculate_parameter(self.dict_landmarks, self.current_param, self.slice_number),3)
        
            self.add_parameter()
            self.output_table.insert(parent= '', index = tk.END, values = (self.current_param, self.param_value, self.slice_number))
        else:
            messagebox.showinfo(title="Message", message="must open image first")
    
    def calc_steep_vertebral(self):
        self.current_param = "steep vertebral"
        if self.image_array is not None:
            pts = self.get_points(num_points=2)
            
            
            if f"slice_{self.slice_number}" not in self.dict_landmarks:
                # If the key doesn't exist, create it with an empty dictionary as its value
                self.dict_landmarks[f"slice_{self.slice_number}"] = {}
                
            self.dict_landmarks[f"slice_{self.slice_number}"]["point_11"] = pts[0,:]
            self.dict_landmarks[f"slice_{self.slice_number}"]["point_12"] = pts[1,:]
            
            
            self.layout.show_landmarks(self.slice_number, self.dict_landmarks)
            
            self.param_value = round(calculate_parameter(self.dict_landmarks, self.current_param, self.slice_number),3)
            
            self.add_parameter()
            self.output_table.insert(parent= '', index = tk.END, values = (self.current_param, self.param_value, self.slice_number))
        else:
            messagebox.showinfo(title="Message", message="must open image first")
   
"""

            