# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 17:15:37 2023

@author: 20182371
"""
import customtkinter 
import tkinter as tk 
from tkinter import filedialog, messagebox
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
import os
import SimpleITK as sitk
import pandas as pd
from Tools.Deformity_Parameters import calculate_parameter
import Tools.Segmentation
import Tools.Contouring
import GUI.GUI_utils

import scipy as sc
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
        self.assymetry_index = "Assymetry index"
        self.trunk_rotation = "Angle trunk rotation"
        self.pectus_index = "Pectus index"
        self.sagital_diameter = "Sagittal diameter"
        self.steep_vertebral = "Steep vertebral"
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
        self.trans_slice = 199
        self.coronal_slice = 134
        self.contour_points = None
        self.df_params = None
        self.param_value = None
        self.current_param = None
        self.dict_landmarks = {}
        self.dict_parameters = {}
        self.start_slice = None
        self.end_slice = None
        self.contour = False
        self.help_window = None
        
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
        
        #---------------------------------------------- general buttons -----------------------------------------
        self.button_begin = self.layout.master.button_begin
        self.button_begin.bind('<Button-1>', lambda event: self.set_slice("start"))
        
        self.button_end = self.layout.master.button_end
        self.button_end.bind('<Button-1>', lambda event: self.set_slice("end"))
        
        self.button_landmark_extension = self.layout.master.button_landmark_extension
        self.button_landmark_extension.bind('<Button-1>', lambda event: self.weighted_landmark_extension(self.start_slice, self.end_slice))
        
        self.button_segment = self.layout.master.button_segment
        self.button_segment.bind('<Button-1>', lambda event: self.automatic_segmentation())
        
        self.button_show_trans_segment = self.layout.master.button_show_trans_segment
        self.button_show_trans_segment.bind('<Button-1>', lambda event: self.change_image_view(self.transverse))
        
        self.button_show_coronal_segment = self.layout.master.button_show_coronal_segment
        self.button_show_coronal_segment.bind('<Button-1>', lambda event: self.change_image_view(self.coronal))
        
        #---------------------------------------------- parameter buttons --------------------------------------
        self.button_manual_parameters = self.layout.master.button_manual_parameters
        self.button_manual_parameters.bind('<Button-1>', lambda event: self.get_parameter(self.parameter_menu.get(), self.trans_slice))
        
        self.button_compute_parameters = self.layout.master.button_compute_parameters
        self.button_compute_parameters.bind('<Button-1>', lambda event: self.get_parameter(self.parameter_menu.get(), self.trans_slice, get_points = False))

        self.button_compute_rib_rotation = self.layout.master.button_compute_rib_rotation
        self.button_compute_rib_rotation.bind('<Button-1>', lambda event: self.computer_rib_params(self.dict_landmarks, type = 'middle'))

        self.button_compute_all_parameters = self.layout.master.button_compute_all_parameters
        self.button_compute_all_parameters.bind('<Button-1>', lambda event: self.compute_all_params(self.dict_landmarks))

        self.button_auto_landmarks = self.layout.master.button_auto_landmarks
        self.button_auto_landmarks.bind('<Button-1>', lambda event: self.get_contour_landmarks_range())
        
        #----------------------------------------------------- output part -----------------------------------------------
        self.button_clear_parameters = self.layout.master.button_clear_parameters
        self.button_clear_parameters.bind('<Button-1>', lambda event: self.clear_parameters())
        
        self.button_save_parameters = self.layout.master.button_save_parameters
        self.button_save_parameters.bind('<Button-1>', lambda event: self.save_parameters())
        
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
        self.output_table.bind('<Delete>', self.delete_items())
        
        
    
    # I can't get this delete option to work: https://www.youtube.com/watch?v=jRpHmF-iuMI&t=614s
    def delete_items(self):
        print("delete")
        for i in self.output_table.selection():
            self.output_table.delete(i)
        
    def open_file(self):
        """function that opens the filedialog and allows for opening of an image 
        which is then displayed in the transverse and coronal view"""
        
        try:
            #open directory to find a file
            self.file_path = filedialog.askopenfile(title = "Open patient image")
            
            #only proceed if the selected file is .nii
            if os.path.splitext(self.file_path.name)[1] != '.nii':
                messagebox.showinfo(title="Message", message="incorrect file type")
                return 
            
            #read the image and get the array
            self.image = sitk.ReadImage(self.file_path.name)
            self.image_array = sitk.GetArrayFromImage(self.image)
            
            if np.all(self.image_array <= 1) and np.all(self.image_array >= 0):
                messagebox.showinfo(title="Message", message="incorrect file type, please open a non-segmented image")
                return 
            
            #initialize the trans array image and state 
            self.trans_image_array = self.image_array
            self.trans_array_state = self.non_segmented
            
            #initialize the coronal image array and state
            self.coronal_image_array = self.image_array
            self.coronal_array_state = self.non_segmented
            
            #reset variables upon opening an image
            self.segmented_image = None
            self.segmented_image_array = None
            self.trans_slice = 199
            self.coronal_slice = 134
            self.contour_points = None
            self.df_params = None
            self.param_value = None
            self.current_param = None
            self.dict_landmarks = {}
            self.dict_parameters = {}
            self.start_slice = None
            self.end_slice = None
            self.contour = False
            
            for i in self.output_table.get_children():
                self.output_table.delete(i)
            
            #draw the image in the GUI
            self.layout.draw_image(self.trans_image_array, self.coronal_image_array, self.trans_slice, self.coronal_slice, self.contour, self.start_slice, self.end_slice, self.map)
            self.layout.show_landmarks(self.image_array, self.trans_slice, self.coronal_slice, self.dict_landmarks, self.map)
            
        except:
            messagebox.showerror("opening file", "Problem with opening the file, please. try another one")
            
    def change_slice(self, view, direction):
        """Handle changing the slice using plus and minus buttons below the 
        transverse and coronal images
        
        Parameters
        ----------
        view: string
            the view, transverse or coronal, of which the 
            slice is changed 
        direction: string
            the direction, plus or minus, in which the slice
            is changed
        """
        
        if self.image_array is None:
            #if there is no opened image then do nothing
            return
        
        if view == self.transverse:
            #if the view is transverse, check the direction, plus or minus, in which the slice is changed
            if direction == self.plus: 
                #if the direction is plus, check whether the slice is still within range
                if self.trans_slice >= 0 and self.trans_slice < np.shape(self.image_array)[0]-1:
                    #if the slice is withing range, change the slice number
                    self.trans_slice += 1
            elif direction == self.minus:
                #if the direction is minus, check whether the slice is still within range
                if self.trans_slice > 0 and self.trans_slice <= np.shape(self.image_array)[0]-1:
                    #if the slice is within range, change the slice number
                    self.trans_slice -= 1

        elif view == self.coronal:
            #if the view is coronal, check the direction, plus or minus, in which the slice is changed
            if direction == self.plus:
                #if the direction is plus, check whether the slice is still within range
                if self.coronal_slice >= 0 and self.coronal_slice < np.shape(self.image_array)[1]-1:
                    #if the slice is withing range, change the slice number
                    self.coronal_slice += 1
            elif direction == self.minus:
                #if the direction is minus, check whether the slice is still within range
                if self.coronal_slice > 0 and self.coronal_slice <= np.shape(self.image_array)[1]-1:
                    #if the slice is withing range, change the slice number
                    self.coronal_slice -= 1
                
            
        #update the image and the landmarks to the chage in slice number
        self.layout.draw_image(self.trans_image_array, self.coronal_image_array, self.trans_slice, self.coronal_slice, self.contour, self.start_slice, self.end_slice, self.map)
        self.layout.show_landmarks(self.image_array, self.trans_slice, self.coronal_slice, self.dict_landmarks, self.map)
    
    def go_to_slice(self, view):
        """handle changing the slice of both views based on the entry input
        
        Parameters
        ----------
        view: string
            the view, transverse or coronal, of which the 
            slice is changed 
        """
        
        try:
            #retrieve the slice number from the entry and assign it to the dialog_input
            if view == self.transverse:
                dialog_input = int(self.slice_entry.get())-1
            elif view == self.coronal: 
                dialog_input = int(self.coronal_slice_entry.get())-1 
        except ValueError:
            # error message if the input is not an integer
            messagebox.showinfo(title="Message", message="Must input an integer to change the slice.")
        else:
            if self.image_array is None: 
                #if there is no opened image then do nothing
                messagebox.showinfo(title="Message", message="no image opened, please open an image first")
                return  
            
            if view == self.transverse:
                #if the view is transverse, check whether the slice is in range
                if dialog_input >= 0 and dialog_input <= np.shape(self.trans_image_array)[1]:
                    #if the slice is within range, assign it to the trans_slice variable
                    self.trans_slice = dialog_input
                    
                else: 
                    #if the slice is out of range give an error message and stop 
                    messagebox.showinfo(title="Message", message="Slice is out of range.")
                    return 
            
            if view == self.coronal:
               #if the view is coronal, check whether the slice is in range
               if dialog_input >= 0 and dialog_input <= np.shape(self.coronal_image_array)[1]:
                   #if the slice is within range, assign it to the coronal_slice variable 
                   self.coronal_slice = dialog_input
               else:
                   #if the slice is out of range give an error message and stop
                   messagebox.showinfo(title="Message", message="Slice is out of range.")
                   return
            
            #update the image and the landmarks to the chage in slice number
            self.layout.draw_image(self.trans_image_array, self.coronal_image_array, self.trans_slice, self.coronal_slice, self.contour, self.start_slice, self.end_slice, self.map)
            self.layout.show_landmarks(self.image_array, self.trans_slice, self.coronal_slice, self.dict_landmarks, self.map)
                    
        finally:
            #clear the entry for future user input
            self.slice_entry.delete(0, "end")
            self.coronal_slice_entry.delete(0, "end")
    
    def change_image_view(self, view):
        """handle changing from the normal image to the segmentated image
        
        Parameters
        ----------
        view: string
            the view, transverse or coronal, of which the 
            slice is changed 
        """
        
        if self.image_array is None: 
            #if there is no opened image then do nothing
            messagebox.showinfo(title="Message", message="no image opened, please open an image first")
            return 
        
        if self.segmented_image_array is None:
            #if there is no opened image then open the file dialog to allow the user to select an segmented image
            segmentation_path = filedialog.askopenfile(title="Open segmentation image")
            try:
                #read the image and get the array
                self.segmented_image = sitk.ReadImage(segmentation_path.name)
                self.segmented_image_array = sitk.GetArrayFromImage(self.segmented_image)
            except ValueError:
                #if there is a problem with opening the image then give an error
                messagebox.showerror("Contouring", "Problem with loading the image, please try a different one")
        
        if view == self.transverse:
            #if the view is transverse then check what the current state is
            if self.trans_array_state == self.non_segmented:
                #if the current state is non segmented then change the image and state to segmented and enable contouring
                self.trans_image_array = self.segmented_image_array
                self.contour = True
                self.trans_array_state = self.segmentation
            elif self.trans_array_state == self.segmentation:
                #if the current state is segmented then change the image and state to non segmented and disable contouring
                self.trans_image_array = self.image_array
                self.trans_array_state = self.non_segmented
                self.contour = False
        elif view == self.coronal:
            #if the view is transverse then check what the current state is
            if self.coronal_array_state == self.non_segmented:
                #if the current state is non segmented then change the image and state to segmented and enable contouring 
                self.coronal_image_array = self.segmented_image_array
                self.coronal_array_state = self.segmentation
            elif self.coronal_array_state == self.segmentation:
                #if the current state is segmented then change the image and state to non segmented and disable contouring
                self.coronal_image_array = self.image_array
                self.coronal_array_state = self.non_segmented
            
        #update the image 
        self.layout.draw_image(self.trans_image_array, self.coronal_image_array, self.trans_slice, self.coronal_slice, self.contour, self.start_slice, self.end_slice, self.map)
        if self.trans_array_state == self.non_segmented: 
            #if the transverse state is non segemented update the landmarks
            self.layout.show_landmarks(self.image_array, self.trans_slice, self.coronal_slice, self.dict_landmarks, self.map)
        
            
    def set_slice(self, position):
        """handle changing from the normal image to the segmentated image
        
        Parameters
        ----------
        position: string
            the position, start or end, of the point that is set
        """
        if self.image_array is None: 
            #if there is no opened image then do nothing
            messagebox.showinfo(title="Message", message="no imaged opened, please open an image first")
            return 
        
        if position == "start":
            #if the position is start then check if the slice is lower than the set end slice
            if self.end_slice == None or self.end_slice > self.trans_slice:
                self.start_slice = self.trans_slice
            else: 
                #if the slice is higher then the end slice then give an error 
                messagebox.showinfo(title="Error", message="Starting slice has to come before the end slice")
            
        elif position == "end":
            #if the position is end then check if the slice is higher than the set start slice
            if self.start_slice == None or self.start_slice < self.trans_slice:
                self.end_slice = self.trans_slice
            else:
                #if the slice is lower than the start slice then give an error 
                messagebox.showinfo(title="Error", message="End slice has to come after the starting slice")
    
    def get_points(self, parameter, slice_num):
        """get landmarks position based on user input
        
        Parameters
        ----------
        parameter: string
            the parameter for which the points are retreived 
        slice_num: int
            the slice number for which points have to be retreived
        """
        
        if self.help_window is not None: 
            self.help_window.destroy()
            self.help_window = None
        
        #show the image in new window
        plt.imshow(self.image_array[slice_num, :, :], cmap=self.map)
        plt.title(f"Put in the landmarks for {parameter}")
        plt.gca().invert_yaxis()

        #retreive points by user input 
        points = []
        points = np.asarray(plt.ginput(len(self.dict_landmark_num[parameter]), timeout=-1))
        plt.close() 
        
        if f"slice_{slice_num}" not in self.dict_landmarks:
            # if the key doesn't exist, create it with an empty dictionary as its value
            self.dict_landmarks[f"slice_{slice_num}"] = {}
        
        #assign the retreived point to the correct keys in the dictionary based on the parameter 
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

    def get_parameter(self, parameter, slice_num, get_points = True):
        """calculate the parameter value and store in the dictionary 
        
        Parameters
        ----------
        parameter: string
            the parameter for which the points are retreived 
        slice_num: int
            the slice number for which points have to be retreived
        get_points: boolean
            whether the landmarks still have to be retreived via user input or not
        """
        
        
        if self.image_array is None: 
            #if there is no opened image then do nothing
            messagebox.showinfo(title="Message", message="no image opened, please open an image first")
            return 
        
        #set the current parameter value to the parameter value that is passed 
        self.current_param = parameter
        
        if get_points == True:
            #if get points is True then call function for retreiving landmarks and update the landmarks in the image
            self.get_points(parameter, slice_num)
            self.layout.show_landmarks(self.image_array, self.trans_slice, self.coronal_slice, self.dict_landmarks, self.map)
        
        elif get_points == False: 
            for i in range(len(self.dict_landmark_num[parameter])):
                if f"slice_{slice_num}" not in self.dict_landmarks:
                   messagebox.showinfo(title="Message", message=f"the landmarks for {parameter} are not known in the current slice")
                   return       
                if f"point_{self.dict_landmark_num[parameter][i]}" not in self.dict_landmarks[f"slice_{slice_num}"]:
                    messagebox.showinfo(title="Message", message=f"the landmarks for {parameter} are not known in the current slice")
                    return
                    
        #calculate the parameters value
        if parameter == self.assymetry_index:
            param_value = round(calculate_parameter(self.dict_landmarks, parameter, slice_num),3)
        else:
            param_value = round(calculate_parameter(self.dict_landmarks, parameter, slice_num),1)
        #add the parameter to the dictionary 
        self.add_parameter(parameter, param_value, slice_num)
        #insert the parameter value to the output table
        self.output_table.insert(parent= '', index = tk.END, values = (parameter, param_value, slice_num+1))
        
    def add_parameter(self, parameter, param_value, slice_num):
        """store the parameter value in the correct locations 
        
        Parameters
        ----------
        parameter: string
            the parameter for which the points are retreived 
        param__value: float 
            the value of the calculated parameter
        slice_num: int
            the slice number for which points have to be retreived
        """
        if self.df_params is None:
            #if the parameter dataframe does not exist yet then create it 
            self.df_params = pd.DataFrame({'Parameter': [], 'Value': [], "Slice":[]})
            
        #creat a new row and add it to the dataframe 
        new_row = {'Parameter': parameter, 'Value': param_value, "Slice": slice_num}
        self.df_params = self.df_params.append(new_row, ignore_index=True)

        
        if f"slice_{slice_num}" not in self.dict_parameters:
            # if the key doesn't exist, create it with an empty dictionary as its value
            self.dict_parameters[f"{slice_num}"] = {}
        
        #add the parameter value to the dictionary
        self.dict_parameters[f"{slice_num}"][f"{parameter}"] = param_value
        
    def save_parameters(self):
        """save the calculated parameters in a .csv file
        
        Parameters
        ----------
        
        """
        
        if self.df_params is None:
            messagebox.showinfo(title = "Message", message = "no parameters computed, please compute parameters before saving" )
            return 
        
        #ask for a file name and retreive it from the input dialog
        dialog = customtkinter.CTkInputDialog(text="give a name for the file:", title="save parameters")
        file_name = dialog.get_input()
        
        #save the file as .csv
        self.df_params.to_csv(f'{file_name}.csv', index=False)
        
        #show a message to inform that the parameters are save and where
        path = str(os.getcwd())
        messagebox.showinfo("Parameters", "File " + file_name + " saved at " + path )
        
    def clear_parameters(self):
        for i in self.output_table.get_children():
            self.output_table.delete(i)
        
    def weighted_landmark_extension(self, start_slice, end_slice):
        """save the calculated parameters in a .csv file
        
        Parameters
        ----------
        start_slice: int 
            the the start slice for weighted landmark extension 
        end_slice: int 
            the end slice for weighted landmark extension
        
        """
        if self.image_array is None: 
            #if there is no opened image then do nothing
            messagebox.showinfo(title="Message", message="no image opened, please open an image first")
            return
        
        #retreive the parameter that is currently selected in the dropdown menu
        parameter = self.parameter_menu.get()
        
        #check if the start and end slice are set and give error if on of the two is not 
        if start_slice == None or end_slice == None:
            messagebox.showerror("Landmark extension", "Start or end slice not set, please set them and try again")
            return
        
        #create empty list to save the slice number that have a manual input 
        original_seeds = []
        
        #get a manual input every 25 slice between the start and end slice, add the slice number to the original_seeds list
        for i in range(start_slice, end_slice, 25):
            self.get_points(parameter, i)
            original_seeds.append(i)
        
        #if the end slice is not in the orignal seed list then add it and get a manual input
        if original_seeds[-1] != end_slice:
            self.get_points(parameter, end_slice)
            original_seeds.append(end_slice)

        #create a window and progress bar
        window, progressbar = self.progressbar("Landmark Extension")
        window.update()
        
        #set the progress to zero 
        progress = 0
        
        #loop over all the required landmarks for the selected parameter
        for point in self.dict_landmark_num[parameter]:
            #loop over the slices that have a manual input
            for n_seed in range(0,len(original_seeds)-1, 1):
                #empty lists to add the value for the upward and downward landmark extension
                up_seed = []
                down_seed = []
                
                #retrieve the first seed that is used for upward landmark extension 
                prev_seed = self.dict_landmarks[f"slice_{original_seeds[n_seed]}"][f"point_{point}"]
                
                #perform upward landmark extension starting form the point that was manual input
                for i in range(original_seeds[n_seed]+1, original_seeds[n_seed+1], 1):
                    next_seed = GUI.GUI_utils.GetNextSeed(self.image_array[i,:,:], prev_seed)
                    up_seed.append(next_seed)
                    prev_seed = next_seed
                
                #retrieve the seed from the next point for downward landmark extension
                prev_seed = self.dict_landmarks[f"slice_{original_seeds[n_seed+1]}"][f"point_{point}"]
                
                #perform downward landmark extension starting from the manual input
                for j in range(original_seeds[n_seed+1]+1, original_seeds[n_seed], -1):
                    next_seed = GUI.GUI_utils.GetNextSeed(self.image_array[j,:,:], prev_seed)
                    down_seed.append(next_seed)
                    prev_seed = next_seed
                
                #perform weigting usin the seed from upward and downward landmark extesion, weighting is done based on the distance from the manual inputs
                for k in range(len(up_seed)): 
                    seed_x = ((len(up_seed)-1-k) * up_seed[k][0] + (k+1) * down_seed[-k][0])/len(up_seed)
                    seed_y = ((len(up_seed)-1-k) * up_seed[k][1] + (k+1)* down_seed[-k][1])/len(up_seed)
                    seed = (seed_x, seed_y)
                    
                    if f"slice_{original_seeds[n_seed]+k+1}" not in self.dict_landmarks:
                        # if the key doesn't exist, create it with an empty dictionary as its value
                        self.dict_landmarks[f"slice_{original_seeds[n_seed]+k+1}"] = {}
                     
                    #save the the seed in the landmark dictionary 
                    self.dict_landmarks[f"slice_{original_seeds[n_seed]+k+1}"][f"point_{point}"] = seed
            
            #update the progress bar 
            progress += 1/len(self.dict_landmark_num[parameter])
            progressbar.set(progress-0.1)
            window.update_idletasks()
        
        #draw the computed landmarks 
        self.layout.draw_image(self.trans_image_array, self.coronal_image_array, self.trans_slice, self.coronal_slice, self.contour, self.start_slice, self.end_slice, self.map)
        self.layout.show_landmarks(self.image_array, self.trans_slice, self.coronal_slice, self.dict_landmarks, self.map)
        
        #destroy the progress window
        time.sleep(2)
        window.destroy()
        
    def computer_rib_params(self, dict_landmarks, maxdist = 200, type = 'middle'):
        """compute selected parameter between the selected start slice and end slice
        and only if it is no further than maxdist from the closest rib and if it has the largest deformity of this rib.
        it is assumed that there are at least slidesize slices between each rib and the next
        
        Parameters
        ----------
        dict_landmarks: dictionary 
            dictionary that contains the landmarks locations 
        max_dist: int 
            maximum distance between the landmarks and the rib centroids
        type: str
            Type of slice selection, options:
            'middle' for slice in the middle of each rib
            'max' for slice at maximum deformity
        
        """
        if self.image_array is None: 
            #if there is no opened image then do nothing
            messagebox.showinfo(title="Message", message="no image opened, please open an image first")
            return
        
        maxrot = 0
        maxsym = 0
        maxparamslice = 0
        rib_begin = 0
        rib_end = 0
        slidesize = 10

        # Some error handling
        if self.start_slice == None or self.end_slice == None:
            messagebox.showerror("Rib parameters", "Start slice or end slice not selected")
            return

        for slice_num in range(self.start_slice, self.end_slice + 1):
            if f"slice_{slice_num}" in dict_landmarks:
                break
            if slice_num == self.end_slice:
                messagebox.showerror("Rib parameters", "No landmarks found between start slice and end slice")
                return

        #ask for segmentation image if this has not been generated yet
        if self.segmented_image is None:
            segmentation_path = filedialog.askopenfile(title="Open segmentation image")
            try:
                #read the segmented image and get get the array
                self.segmented_image = sitk.ReadImage(segmentation_path.name)
                self.segmented_image_array = sitk.GetArrayFromImage(self.segmented_image)
            except:
                #if the image cannot be read then give an error
                messagebox.showerror("Segmentation", "Problem with loading the segmented image, please try a different one or run the segmentation function")
                return

        #Progressbar to show progress for the parameter calculation
        window, progressbar = self.progressbar("Parameter calculation")
        window.update()
        parameter = self.parameter_menu.get()
        
        #loop over all slices between start_slice and end_slice and compute the selected landmark
        for slice_num in range(self.start_slice, self.end_slice+1):
            progressbar.set(slice_num/np.shape(self.image_array)[0])
            window.update_idletasks()
            
            if f"slice_{slice_num}" in dict_landmarks:
                
                if parameter == self.trunk_rotation:
                    if "point_3" in self.dict_landmarks[f"slice_{slice_num}"] and "point_4" in self.dict_landmarks[f"slice_{slice_num}"]:
                        contour_points = Tools.Contouring.MultiSliceContour(self.segmented_image_array, slice_num, dist = 10, interval=1, verbose = False)
                        contour_points = contour_points.reshape(-1,2)
                        point3 = np.array(self.dict_landmarks[f"slice_{slice_num}"]["point_3"])
                        point4 = np.array(self.dict_landmarks[f"slice_{slice_num}"]["point_4"])
                        
                        #Distance calculation
                        dist3 = np.dot((contour_points - point3)**2, np.ones(2))
                        dist4 = np.dot((contour_points - point4)**2, np.ones(2))
                        print("Distance for slice " + str(slice_num) + " is " + str(np.min(dist3)) + " " + str(np.min(dist4)))

                        if (np.min(dist3) < maxdist and np.min(dist4) < maxdist):
                            Rotation = calculate_parameter(dict_landmarks, self.trunk_rotation, slice_num)
                            if rib_begin == 0:
                                rib_begin = slice_num
                                rib_end = slice_num
                            else:
                                rib_end = slice_num
                            if (maxrot < Rotation):
                                maxrot = Rotation
                                maxparamslice = slice_num
                        
                        if (slice_num - rib_end) > slidesize and rib_begin != 0:
                            if type == 'middle':
                                param_slice = (rib_end-rib_begin)//2 + rib_begin
                            elif type == 'max':
                                param_slice = maxparamslice
                            self.get_parameter(self.trunk_rotation, param_slice, get_points=False)
                            maxrot = 0
                            maxparamslice = 0
                            rib_begin = 0
                            rib_end = 0
                    else:
                        messagebox.showerror("Rib parameters", "Not all landmarks are generated for " + str(parameter) + " at slice " + str(slice_num))
                
                elif parameter == self.assymetry_index:
                    if "point_5" in self.dict_landmarks[f"slice_{slice_num}"] and "point_6" in self.dict_landmarks[f"slice_{slice_num}"] and "point_7" in self.dict_landmarks[f"slice_{slice_num}"] and "point_8" in self.dict_landmarks[f"slice_{slice_num}"]:
                        contour_points = Tools.Contouring.MultiSliceContour(self.segmented_image_array, slice_num, dist=10,
                                                                            interval=1, verbose=False)
                        contour_points = contour_points.reshape(-1, 2)
                        point5 = np.array(self.dict_landmarks[f"slice_{slice_num}"]["point_5"])
                        point6 = np.array(self.dict_landmarks[f"slice_{slice_num}"]["point_6"])
                        point7 = np.array(self.dict_landmarks[f"slice_{slice_num}"]["point_7"])
                        point8 = np.array(self.dict_landmarks[f"slice_{slice_num}"]["point_8"])
                       
                        # Not quite sure if the distance calculation is right
                        dist5 = np.dot((contour_points - point5) ** 2, np.ones(2))
                        dist6 = np.dot((contour_points - point6) ** 2, np.ones(2))
                        dist7 = np.dot((contour_points - point7) ** 2, np.ones(2))
                        dist8 = np.dot((contour_points - point8) ** 2, np.ones(2))
                       
                        print(
                            "Distance for slice " + str(slice_num) + " is " + str(np.min(dist5)) + " " + str(np.min(dist6)) + " " + str(np.min(dist7)) + " " + str(np.min(dist8)))

                        if type == 'all':
                            self.get_parameter(self.assymetry_index, slice_num, get_points=False)
                            continue

                        if (np.min(dist5) < maxdist and np.min(dist7) < maxdist):
                            #Only takes the points that are close to the back, because there are very few ribs in front
                            Asymmetry = calculate_parameter(dict_landmarks, self.assymetry_index, slice_num)
                            if (maxsym < Asymmetry):
                                maxsym = Asymmetry
                                maxparamslice = slice_num
                       
                        if (slice_num - maxparamslice) > slidesize and maxparamslice != 0:
                            self.get_parameter(self.assymetry_index, maxparamslice, get_points=False)
                            maxsym = 0
                            maxparamslice = 0
                    else:
                        messagebox.showerror("Rib parameters","Not all landmarks are generated for " + str(parameter) + " at slice " + str(slice_num))
                else:
                    messagebox.showerror("Rib parameters", str(parameter) + " has not been implemented yet")
                    window.destroy()
                    return
        
        window.destroy()
        
        return


    def compute_all_params(self, dict_landmarks):
        #Computes all parameters between the start and end slice

        #Error handling
        if self.image_array is None:
            #if there is no opened image then do nothing
            messagebox.showinfo(title="Message", message="no image opened, please open an image first")
            return

        if self.start_slice == None or self.end_slice == None:
            messagebox.showerror("All parameters", "Start slice or end slice not selected")
            return

        for slice_num in range(self.start_slice, self.end_slice + 1):
            if f"slice_{slice_num}" in dict_landmarks:
                break
            if slice_num == self.end_slice:
                messagebox.showerror("All parameters", "No landmarks found between start slice and end slice")
                return

        window, progressbar = self.progressbar("Parameter calculation")
        window.update()
        parameter = self.parameter_menu.get()

        # loop over all slices between start_slice and end_slice and compute the selected landmark
        for slice_num in range(self.start_slice, self.end_slice + 1):
            progressbar.set(slice_num / np.shape(self.image_array)[0])
            window.update_idletasks()
            if f"slice_{slice_num}" in dict_landmarks:
                self.get_parameter(parameter, slice_num, get_points=False)

        window.destroy()
        return




    def automatic_segmentation(self):
        """compute the segmented image for the image that is currently loaded in, saving it after it is done
        
        Parameters
        ----------
     
        """
        if self.image_array is None: 
            #if there is no opened image then do nothing
            messagebox.showinfo(title="Message", message="no image opened, please open an image first")
            return

        window, progressbar = self.progressbar("Segmentation")

        #retreive the segmented image and the array of that image
        segmented_image = Tools.Segmentation.SimpleSegmentation(self.image, threshold=150, OpeningSize=1, ClosingSize=2)
        progressbar.set(0.5)
        window.update_idletasks()
        
        self.segmented_image = Tools.Segmentation.FilterLargestComponents(segmented_image)
        self.segmented_image_array = sitk.GetArrayFromImage(self.segmented_image)
        progressbar.set(0.9)
        window.update_idletasks()
        
        #save segmentation
        filename = str(os.getcwd() + "/Segmented" + os.path.split(self.file_path.name)[1])
        sitk.WriteImage(self.segmented_image, fileName=filename)
        window.destroy()
        
        messagebox.showinfo("Segmentation", "Segmentation completed, image placed at " + filename)
        
        
        return

    def get_contour_landmarks(self, slice_num, loop = False):
        """retreive the landmark based on the contour made from the segmented image
        
        Parameters
        ----------
        slice_num: int 
            the slice number for which the landmarks have to be retreived

        loop: bool
            Whether or not we should recalculate the contour points for every single loop
            
        """
        
        if self.segmented_image is None:
            #if there is no opened image then give an error message
            segmentation_path = filedialog.askopenfile(title="Open segmentation image")
            try:
                #read the segmented image and get get the array
                self.segmented_image = sitk.ReadImage(segmentation_path.name)
                self.segmented_image_array = sitk.GetArrayFromImage(self.segmented_image)
            except:
                #if the image cannot be read then give an error
                messagebox.showerror("Contouring", "Problem with loading the image, please try a different one")

        if self.contour_points is None or loop == True:
            try:
                #if there is no contour then retrieve the contour using the function MultiSlcieContour
                centroids = Tools.Contouring.MultiSliceContour(self.segmented_image_array, slice_num, verbose = False)
                hull = cv.convexHull(centroids[1:])
                self.contour_points = hull.reshape(-1,2)
            except:
                #if there are problems retreiving the contour give an errror
                messagebox.showerror("Contouring", "Problem with calculating the contour points")

        if f"slice_{slice_num}" not in self.dict_landmarks:
            # if the key doesn't exist, create it with an empty dictionary as its value
            self.dict_landmarks[f"slice_{slice_num}"] = {}

        image_half = np.array(self.segmented_image_array.shape)/2

        #Split the image in right and left points
        Left_points = self.contour_points[self.contour_points[:,0] < image_half[-1]]
        Left_top = Left_points[np.argmin(Left_points[:,1]),:]

        Right_points = self.contour_points[self.contour_points[:,0] > image_half[-1]]
        Right_top = Right_points[np.argmin(Right_points[:,1]),:]

        #add the points for angle of trunk rotation to the landmark dictionary
        self.dict_landmarks[f"slice_{slice_num}"]["point_3"] = Right_top.astype(int)
        self.dict_landmarks[f"slice_{slice_num}"]["point_4"] = Left_top.astype(int)

        #Pectus index
        maxdist = 0
        leftmaxidx = 0
        rightmaxidx = 0
        maxdist, leftmaxPoint, rightmaxPoint = Tools.Deformity_Parameters.Find_Longest(Left_points, Right_points)

        #add the landmarks for the pectus index to the landmark dictionary
# =============================================================================
#         self.dict_landmarks[f"slice_{slice_num}"]["point_9"] = Left_points[leftmaxidx].astype(int)
#         self.dict_landmarks[f"slice_{slice_num}"]["point_10"] = Right_points[rightmaxidx].astype(int)
# 
# =============================================================================
        #TODO calculate the sternum and top of vertebra, but the segmentation does not yet allow for that

        #Asymmetry index
        
        #get all the contour points in an array
        conts = self.contour_points
        canva = np.zeros((self.image_array[slice_num,:,:].shape[0],self.image_array[slice_num,:,:].shape[1], 3 ))
        cv.drawContours(canva, [conts], -1, (0, 255, 0), 1)
        canva = canva[:,:,1]
        size = canva.shape
        midpoint = int(size[1]/2)
        
        
        #examine left half of the image 
        max_dist = 0
        coor_right = []
        for x in range(0,midpoint-5):
            inline = []
            for y in range(size[0]):
                if canva[y,x] != 0:
                    inline.append([x,y])
            if len(inline) == 2:
                dist = np.abs(inline[0][1]-inline[1][1])
                if dist > max_dist :
                    max_dist = dist
                    coor_right = np.array(inline)
                
        #examine right half of the image
        max_dist = 0
        coor_left = []
        for x in range(midpoint+5, size[1]):
            inline = []
            for y in range(size[0]):
                if canva[y,x] != 0:
                    inline.append([x,y])
            if len(inline) == 2:
                dist = np.abs(inline[0][1]-inline[1][1])
                if dist > max_dist :
                    max_dist = dist
                    coor_left = np.array(inline)


        
        self.dict_landmarks[f"slice_{slice_num}"]["point_5"] = coor_left[0].astype(int)
        self.dict_landmarks[f"slice_{slice_num}"]["point_6"] = coor_left[1].astype(int)
        self.dict_landmarks[f"slice_{slice_num}"]["point_7"] = coor_right[0].astype(int)
        self.dict_landmarks[f"slice_{slice_num}"]["point_8"] = coor_right[1].astype(int)



        return

    def get_contour_landmarks_range(self):
        
        if self.image_array is None: 
            #if there is no opened image then do nothing
            messagebox.showinfo(title="Message", message="no image opened, please open an image first")
            return
        
        if self.start_slice == None or self.end_slice == None:
            messagebox.showerror("Contouring", "Please make sure that the start slice and end slice have been selected")
            return
        
        if self.segmented_image is None:
            #if there is no opened image then give an error message
            segmentation_path = filedialog.askopenfile(title="Open segmentation image")
            try:
                #read the segmented image and get get the array
                self.segmented_image = sitk.ReadImage(segmentation_path.name)
                self.segmented_image_array = sitk.GetArrayFromImage(self.segmented_image)
            except:
                #if the image cannot be read then give an error
                messagebox.showerror("Contouring", "Problem with loading the image, please try a different one")
                return 
            
        window, progressbar = self.progressbar("Multi-slice contouring")
        
        r = range(self.start_slice, self.end_slice)
        for slice_num in r:
            self.get_contour_landmarks(slice_num, loop = True)
            progressbar.set((len(r)+self.start_slice)/slice_num)
            window.update_idletasks()

        window.destroy()
        return

    def progressbar(self, label):
        """creat a window with a progress bar in it
        
        Parameters
        ----------
        label: string 
            label that indicates what the progress bar is for
            
        """
        #create a new window
        window = customtkinter.CTkToplevel(self.master)
        self.master.eval(f"tk::PlaceWindow {str(window)} center")
        window.title(label + " progress")
        window.geometry("300x150")
        
        #create and pack a label in the window to show what the user is waiting for
        customtkinter.CTkLabel(window, text = "Please wait for " + label).pack()
        #create and pack the progress bar 
        pb = customtkinter.CTkProgressBar(master = window, mode = "determinate")
        pb.pack()

        #Make sure the progress bar is set and the window updated
        window.grab_set()
        pb.set(0)
        pb.start()
        window.update()
        
        return window, pb
     
    def help_button(self):
        self.help_window = customtkinter.CTkToplevel(self.master)
        self.help_window.title("Help page")
        self.help_window.grab_set()
        
        #title label
        title_label = customtkinter.CTkLabel(self.help_window, text="Welcome to the help page", fg_color = "transparent", font=customtkinter.CTkFont(size=18, weight="bold"))
        title_label.grid(row=0, column=0, columnspan = 2, padx=(10, 10), pady=(10, 10), sticky = 'ew')
        
        #help image
        help_image = plt.imread('../GUI/Help_image.jpeg')
        
        self.help_fig = plt.Figure(figsize=(4,3),dpi=100)
        self.help_fig.set_facecolor(color = "white")
       
        self.help_fig_subplot = self.help_fig.add_subplot()
        self.help_fig_subplot.axis("off")
        self.help_fig_subplot.set_facecolor(color = "white")
        
        self.help_fig_canvas = FigureCanvasTkAgg(self.help_fig, master=self.help_window)  # A tk.DrawingArea.
        self.help_fig_canvas.get_tk_widget().grid(row=1, column=0, rowspan = 2, padx=(10,10), pady=(0,10), sticky = 'news')
        self.help_fig_subplot.imshow(help_image)
        self.help_fig_canvas.draw()
       
        #ROTATE BUTTON
        global rotate
        rotate = 0;
        # Create the rotate button
        #self.button_rotate = customtkinter.CTkButton(rotate_button, text="rotate", font=("Arial", 18), command=rotate_image)
        rotate_button = tk.Frame(master = self.help_window, relief=tk.RAISED, borderwidth=0)
        rotate_button.grid(row=3, column = 0)
        #label = tk.Label(master = rotate_button, text = f"rotate")
        #label.pack() 
        
        def rotate_image(): 
            # Clear the current image from the subplot
            self.help_fig_subplot.clear()
            # create a variable that keeps track of the help image 
            global rotate 
            rotate = (rotate + 1) % 2
            # Load a new image
            if rotate == 0:
                new_image = plt.imread('../GUI/Help_image.jpeg')
            else: 
                new_image = plt.imread('../GUI/Help_image180.jpeg')
   
            # Display the new image on the subplot
            self.help_fig_subplot.imshow(new_image)
            self.help_fig_subplot.axis("off")
            self.help_fig_subplot.set_facecolor(color = "white")
   
            # Update the canvas to show the new image
            self.help_fig_canvas.draw()
    
        
        self.button_rotate = customtkinter.CTkButton(rotate_button, text = "rotate", font = ("Arial",18),  command=rotate_image)
        rotate_button = tk.Frame(master = self.help_window, relief=tk.RAISED, borderwidth=0)
        rotate_button.grid(row=3, column = 0)
        self.button_rotate.pack()
        
        #explanation
        explanation_frame = customtkinter.CTkFrame(self.help_window, fg_color = 'transparent', corner_radius=0) 
        explanation_frame.grid(row = 1, column = 1, sticky = "news")
        # create textbox
        self.textbox = customtkinter.CTkTextbox(explanation_frame, wrap = tk.WORD, width = 400)#, width=400, height = 300)
        self.textbox.grid(row=1, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
        self.textbox.insert("0.0", "How to use the program:\n\n" + 
                            "Before anything can be calculated an image must be opened, " + 
                            "this can be done with the Open Image button in the centre of the Scoliosis Chest Deformity window. " + 
                            "On the left side the axial view pops up and on the right side the coronal view pops up. " + 
                            "It is possible to go to a different slice in each of the views. \n \n" +  
                            "After loading in the image, there are a couple things the user can do: \n " 
                            "- Segment the image \n" + 
                            "- Calculate parameters from manual input \n" + 
                            "- Calculate parameters from landmark extension (semi automatic) \n"+ 
                            "- Calculate parameters automatically \n"+
                            "\n # Segment the image \n"+
                            "The user can segment the image (with the Segment image button). "+
                            "After applying image segmentation, the path of where the image is saved is given. "+
                            "The segmentation can be viewed by using the Transverse segmentation button (for axial view) "+
                            "and Coronal segmentation button (for coronal view). \n\n" +  
                            "# Calculate parameters from manual input \n"+  
                            "The user is asked to put in the landmarks for the selected parameter. "+
                            "The parameter value is directly added to the table below. \n\n"+  
                            "# Calculate parameters from landmark extension (semi automatic) \n" +
                            "First set a startpoint and an endpoint. Then press the Landmark extension button, "+
                            "the user is asked to put in the landmarks for a fraction of the slices. After the extension "+
                            "is done the user can go through the slices and view the landmarks for the previous selected parameter. "+
                            "If the user wants to calculate the value of the parameter, the Compute slice parameters button can be used."+
                            "The value will then be shown in the table below. \n\n"+  
                            "# Calculate parameters automatically \n"+ 
                            "First set a startpoint and an endpoint. Then the user can press the Automatic calculation button, "+
                            "the landmarkpositions are now automatically determined. The user can go through the slices and save "+ 
                            "the parameter values by pressing Compute slice parameters. \n \n"+  
                            "For some of the parameters, the value is more significant when it is calculated with landmarks closer to the rib."+ 
                            "To get those values, the Compute rib parameters can be used. This is available for Angle trunk rotation "+
                            "and Assymetry index. The Compute rib parameters can only be used after calculating the parameters from "+
                            "landmark extension or automatically. \n \n"+  
                            "In the table down below, the calculated values pop up. These can be saved with the button on the bottom."
                            )
        
        legend = customtkinter.CTkFrame(self.help_window, fg_color = 'transparent', corner_radius=0) 
        legend.grid(row = 2, column = 1, sticky = "nswe")
        text = tk.Label(legend, text = "Legend for selection of the landmark points")
        text.grid(row =0, column = 0, columnspan = 2)
        
        # Legenda Angle of trunk rotation
        block = tk.Canvas(legend, width=20, height=20, bg="dodger blue",  highlightthickness=0)
        block.grid(row=1, column =0, padx=(0, 0), pady=(0, 0), sticky="nsew")
        text = tk.Label(legend, text=" Angle of the trunk rotation: 1-2")
        text.grid(row= 1, column=1 , padx=(0, 0), pady=(0, 0), sticky="w")
        # Legenda Assymmetry index
        block = tk.Canvas(legend, width=20, height=20, bg="sky blue",  highlightthickness=0)
        block.grid(row= 2, column=0, padx=(0, 0), pady=(0, 0) , sticky="nsew")
        text = tk.Label(legend, text=" Assymmetry index: 3-4-5-6")
        text.grid(row= 2, column=1, padx=(0, 0), pady=(0, 0), sticky="w")
        # Legenda Pectus index 
        block = tk.Canvas(legend, width=20, height=20, bg="SlateBlue3",  highlightthickness=0)
        block.grid(row= 3, column=0, padx=(0, 0), pady=(0, 0) , sticky="nsew" )
        text = tk.Label(legend, text=" Pectus index: 7-8-9-10")
        text.grid(row= 3, column=1 , padx=(0, 0), pady=(0, 0) , sticky="w")
        # Legenda Sagital diameter
        block = tk.Canvas(legend, width=20, height=20, bg="medium blue",  highlightthickness=0)
        block.grid(row= 4, column=0 , padx=(0, 0), pady=(0, 0) , sticky="nsew")
        text = tk.Label(legend, text=" Sagital diameter: 9-11")
        text.grid(row= 4, column=1, padx=(0, 0), pady=(0, 0) , sticky="w" )
        # Legenda Steep vertebral distance
        block = tk.Canvas(legend, width=20, height=20, bg="midnight blue" ,  highlightthickness=0)
        block.grid(row= 5, column=0, padx=(0, 0), pady=(0, 0) , sticky="nsew")
        text = tk.Label(legend, text= " Steep vertebral distance: 9-10")
        text.grid(row= 5, column=1, padx=(0, 0), pady=(0, 0) , sticky="w" )
        

            
    
    def help_button_test(self):
       
       # configure window 
       self.window = customtkinter.CTkToplevel(self.master)
       self.window.title("Help page")
       
       general_explanation = tk.Frame(master = self.window, relief=tk.RAISED, borderwidth=0)
       general_explanation.grid(row=0, column = 0, columnspan = 2, sticky = "ew")
       general_explanation.logo_label = customtkinter.CTkLabel(general_explanation, text="Help centre", fg_color = "transparent", font=customtkinter.CTkFont(size=12, weight="bold"))
       general_explanation.logo_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky = 'ew')
       
       #HELP IMAGE 
       #self.master.output_frame = customtkinter.CTkFrame(self.master, width = 400, height = 400, fg_color = "transparent", corner_radius=(0))
       self.window.help_image = tk.Frame(master = self.window, relief=tk.RAISED, borderwidth=1)
       self.window.help_image.grid(row=1, column = 0)
       #img = ImageTk.PhotoImage('C:/Users/Laurie/Documents/Medical_Imaging/2022-2023/Team_Challenge/GUI_Laurie/image_help.png')
       #label = tk.Label(master = self.window.help_image, text = f"helpimage")
       #label.pack() 
       fig, ax = plt.subplots()
       # add the path from the github "C:\Users\Laurie\Documents\GitHub\Team-Challenge-Medical-Imaging\GUI\Help_image.jpeg"
       #background = plt.imread('C:/Users/Laurie/Documents/Medical_Imaging/2022-2023/Team_Challenge/GUI_Laurie/image_help.png')
       working_path = os.getcwd()
       background_path = os.path.join(working_path, "Help_image.jpeg")
       background = plt.imread('../GUI/Help_image.jpeg')
       help_image = sitk.ReadImage('../GUI/Help_image.jpeg')
       ax.imshow(background)
       canvas = FigureCanvasTkAgg(fig, master=self.window.help_image)
       canvas.draw()
       
       self.help_fig = plt.Figure(figsize=(4,4),dpi=100)
       self.help_fig.set_facecolor(color = "white")
      
       self.help_fig_subplot = self.help_fig.add_subplot()
       self.help_fig_subplot.axis("off")
       self.help_fig_subplot.set_facecolor(color = "white")
       
       self.help_fig_canvas = FigureCanvasTkAgg(self.help_fig, master=self.window.help_image)  # A tk.DrawingArea.
       self.master.coronal_canvas.draw()
       self.help_fig_canvas.get_tk_widget().grid(row=1, column=0, padx=(10,10), pady=(0,10), sticky = 'news')
       self.help_fig_subplot.imshow(help_image)
       
       #ROTATE BUTTON
       rotate_button = tk.Frame(master = self.window, relief=tk.RAISED, borderwidth=0)
       rotate_button.grid(row=2, column = 0)
       #label = tk.Label(master = rotate_button, text = f"rotate")
       #label.pack() 
       self.button_rotate = customtkinter.CTkButton(rotate_button, text = "rotate", font = ("Arial",18), )
       #button_rotate.place(x=20, y = 20)
       #Button(root, text="rotate", command=rotateimage)
       self.button_rotate.pack()
       
       #VARIABLE NUMBERS
       variable_numb= tk.Frame(master = self.window, relief=tk.RAISED, borderwidth=0)
       variable_numb.grid(row=1, column = 1)
       label = tk.Label(master = variable_numb, text = f"Hier komt een lap tekst")
       label.pack() 
       tekst = tk.Label(variable_numb, text= "Select the landmark point from the selected variable in ascending order.")
       tekst.pack()
       tekstline1 = tk.Label(variable_numb, text= "Angle of the trunk rotation: 1-2")
       tekstline1.pack()
       tekstline2 = tk.Label(variable_numb, text= "Asymmetry index: 3-4-5-6")
       tekstline2.pack()
       tekstline3 = tk.Label(variable_numb, text= "Pectus index: 7-8-9-10")
       tekstline3.pack()
       tekstline4 = tk.Label(variable_numb, text= "Sagital diameter: 9-11")
       tekstline4.pack()
       tekstline5 = tk.Label(variable_numb, text= "Steep vertebral distance: 9-10")
       tekstline5.pack()
            
            
            
            
            

"""
def draw_contour(self):

    if self.segmented_image_array is None:
        segmentation_path = filedialog.askopenfile(title="Open segmentation image")
        try:
            self.segmented_image = sitk.ReadImage(segmentation_path.name)
            self.image_array = sitk.GetArrayFromImage(self.segmented_image)
            self.trans_image_array = self.image_array
            self.coronal_image_array = self.image_array
        except:
            messagebox.showerror("Contouring", "Problem with loading the image, please try a different one")

    self.contour = True 
    self.layout.draw_image(self.trans_image_array, self.coronal_image_array, self.trans_slice, self.coronal_slice, self.contour, self.start_slice, self.end_slice, self.map)
    

def remove_contour(self):
    self.contour = False 
    self.layout.draw_image(self.trans_image_array, self.coronal_image_array, self.trans_slice, self.coronal_slice, self.contour, self.start_slice, self.end_slice, self.map)

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

def calc_contour(self):
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