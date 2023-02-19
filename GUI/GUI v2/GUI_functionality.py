# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 17:15:37 2023

@author: 20182371
"""
import customtkinter 
import tkinter as tk 
from tkinter import filedialog, messagebox, ttk
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
import SimpleITK as sitk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
import pandas as pd
from PIL import ImageTk, Image
from Deformity_Parameters import assymetry_index, angle_trunk_rotation, pectus_index, sagital_diameter, steep_vertebral

from GUI_layout import GUI_Layout

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
        self.button_assymetry_index.bind('<Button-1>', lambda event: self.calc_assymetry_ind())
        
        
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
    
    def previous_slice(self):
        if self.image_array is not None:
            if 0 < self.slice_number < np.shape(self.image_array)[0]:
                self.slice_number -= 1
                self.layout.draw_image(self.image_array, self.slice_number, self.map)
    
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
        self.layout.draw_landmarks(pts)
        
        return pts
    
    def calc_assymetry_ind(self):
        if self.image_array is not None:
            pts = self.get_points(num_points=4)
            assymetry_ind = assymetry_index(pts)
            self.param_value = round(assymetry_ind,3)
            
            self.current_param = "assymetry index"
            self.output_table.insert(parent= '', index = tk.END, values = (self.current_param, self.param_value, self.slice_number))
        else:
            messagebox.showinfo(title="Message", message="must open image first")
            
            
            
            