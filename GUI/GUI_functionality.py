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
from Tools.Deformity_Parameters import calculate_parameter  #, angle_trunk_rotation, pectus_index, sagital_diameter, steep_vertebral


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
        self.button_assymetry_index.bind('<Button-1>', lambda event: self.calc_assymetry_index())
        
        self.button_trunk_angle = self.layout.master.button_trunk_angle
        self.button_trunk_angle.bind('<Button-1>', lambda event: self.calc_trunk_angle())
        
        self.button_pectus_index = self.layout.master.button_pectus_index
        self.button_pectus_index.bind('<Button-1>', lambda event: self.calc_pectus_index())
        
        self.button_sagital_diameter = self.layout.master.button_sagital_diameter
        self.button_sagital_diameter.bind('<Button-1>', lambda event: self.calc_sagital_diameter())
        
        self.button_steep_vertebral = self.layout.master.button_steep_vertebral
        self.button_steep_vertebral.bind('<Button-1>', lambda event: self.calc_steep_vertebral())
        
        self.button_save_parameters = self.layout.master.button_save_parameters
        self.button_save_parameters.bind('<Button-1>', lambda event: self.save_parameters())
        
        #entrys
        self.slice_entry = self.layout.master.slice_entry
        
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
    
    def get_points(self, num_points=4):
        #show the image in new window
        plt.imshow(self.image_array[self.slice_number, :, :],cmap=self.map)

        #emplty list for the points 
        pts = []
        
        #retreive the points 
        pts = np.asarray(plt.ginput(num_points, timeout=-1))
        
        plt.close()
            
        
        #display the marked point in the GUI
        #self.layout.draw_landmarks(pts)
        
        return pts

    
    def add_parameter(self):
        if self.df_params is None:  
            self.df_params = pd.DataFrame({'Parameter': [], 'Value': [], "Slice":[]})
            
        if self.current_param is not None and self.param_value is not None:
            new_row = {'Parameter': self.current_param, 'Value': self.param_value, "Slice": self.slice_number}
            self.df_params = self.df_params.append(new_row, ignore_index=True)
        
        if self.current_param is not None and self.param_value is not None:
            if f"slice_{self.slice_number}" not in self.dict_parameters:
                # If the key doesn't exist, create it with an empty dictionary as its value
                self.dict_parameters[f"{self.slice_number}"] = {}
            
            self.dict_parameters[f"{self.slice_number}"][f"{self.current_param}"] = self.param_value
        
    def save_parameters(self):
        if self.df_params is not None:
            dialog = customtkinter.CTkInputDialog(text="give a name for the file:", title="save parameters")
            file_name = dialog.get_input()
            self.df_params.to_csv(f'{file_name}.csv', index=False)
            
    
    def calc_assymetry_index(self):
        self.current_param = "assymetry index"
        if self.image_array is not None:
            pts = self.get_points(num_points=4)
            
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
        self.current_param = "angle trunk rotation"
        if self.image_array is not None:
            pts = self.get_points(num_points=2)
            
            
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
        self.current_param = "pectus index"
        if self.image_array is not None:
            pts = self.get_points(num_points=4)
            
            
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
        self.current_param = "sagital diameter"
        if self.image_array is not None:
            pts = self.get_points(num_points=2)
            
            
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
            
            