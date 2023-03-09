# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 14:55:40 2023

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


class GUI_Layout: 
    
    def __init__(self, master):
        super().__init__()
        
        self.master = master
        self.master.title("My App")
        
        # configure window
        self.master.title("Scoliosis Chest Deformity")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing) 
        
        # configure grid layout
        self.master.grid_columnconfigure(0,weight = 1)
        self.master.grid_columnconfigure((1), weight=3)
        self.master.grid_columnconfigure((2), weight=2)
        self.master.grid_rowconfigure(0, weight=2)
        self.master.grid_rowconfigure(1, weight=1)
        
        #init frame functions
        self.sidebar()
        self.image_frame()
        self.output_frame()
        self.button_frame()
        
    def sidebar(self):
        self.master.sidebar_frame = customtkinter.CTkFrame(self.master, width=140, corner_radius=0)
        self.master.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        
        self.master.sidebar_frame.columnconfigure(0, weight = 1)
        self.master.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.master.logo_label = customtkinter.CTkLabel(self.master.sidebar_frame, text="Menu", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.master.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky = 'ew')
        
        self.master.sidebar_button_1 = customtkinter.CTkButton(self.master.sidebar_frame, text="Save Parameters", )
        self.master.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10, sticky = 'ew')
        
        self.master.appearance_mode_label = customtkinter.CTkLabel(self.master.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.master.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0), sticky = 'ew')
        
        self.master.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.master.sidebar_frame, values=["Light", "Dark", "System"],command=self.change_appearance_mode_event)
        self.master.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10), sticky = 'ew')
        
    def image_frame(self):
        self.master.image_frame = customtkinter.CTkFrame(self.master, width = 500, height = 700,fg_color = 'transparent', corner_radius=0)
        self.master.image_frame.grid(row=0, column=1, sticky = "nsew")
        self.master.image_frame.columnconfigure(0, weight = 1)
        self.master.image_frame.rowconfigure(1, weight = 1)
        
        self.master.image_label = customtkinter.CTkLabel(self.master.image_frame,  text = "Patient Image", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.master.image_label.grid(row =0, column = 0,padx=20, pady=(20, 10))
        
        #tab views
        self.master.tabview = customtkinter.CTkTabview(self.master.image_frame)
        self.master.tabview.grid(row=1, column=0, sticky = "nsew")
        self.master.tabview.add("Image")
        self.master.tabview.add("Table")
        self.master.tabview.tab("Image").grid_columnconfigure((0,3), weight=1)
        self.master.tabview.tab("Image").grid_rowconfigure((0,1,2), weight=1)
        self.master.tabview.tab("Table").grid_columnconfigure((0), weight=1)
        self.master.tabview.tab("Table").grid_rowconfigure((0), weight=1)
        
        #---------------------------------------- Image tab ----------------------------------------
        self.master.fig = plt.Figure(figsize=(5,5),dpi=100)
        self.master.fig.set_facecolor(color = "white")
        self.master.subplot = self.master.fig.add_subplot()
        self.master.subplot.axis("off")
        self.master.subplot.set_facecolor(color = "white")
        
        #https://matplotlib.org/3.1.0/gallery/user_interfaces/embedding_in_tk_sgskip.html
        self.master.canvas = FigureCanvasTkAgg(self.master.fig, master=self.master.tabview.tab("Image"))  # A tk.DrawingArea.
        self.master.canvas.draw()
        self.master.canvas.get_tk_widget().grid(row=1, column=0, columnspan=5, padx=(10,10), pady=(10,10), sticky = 'news')
        
        self.master.btn_open_image = customtkinter.CTkButton(self.master.tabview.tab("Image"), width = 200, text="Open Image", )
        self.master.btn_open_image.grid(row=2, column=0,padx=(10,10), pady=(0,0), sticky = "w")
        
        self.master.plus_btn = customtkinter.CTkButton(self.master.tabview.tab("Image"), width = 50, text="-", )
        self.master.plus_btn.grid(row=2, column=1,padx=(10,0), pady=(0,0), sticky = 'ew')
        
        self.master.minus_btn = customtkinter.CTkButton(self.master.tabview.tab("Image"), width = 50, text="+", )
        self.master.minus_btn.grid(row=2, column=2,padx=(0,10), pady=(0,0), sticky = 'e')
        
        self.master.slice_entry = customtkinter.CTkEntry(self.master.tabview.tab("Image"), width = 100, placeholder_text="Slice Number")
        self.master.slice_entry.grid(row=2, column=3, columnspan=1, padx=(0, 0), pady=(0, 0), sticky="e")
        
        self.master.skipto_btn = customtkinter.CTkButton(self.master.tabview.tab("Image"), width = 100, text="skip to", )
        self.master.skipto_btn.grid(row=2, column=4 ,padx=(0,10), pady=(0,0), sticky = 'e')
        
        #---------------------------------------- Table tab ----------------------------------------
        
        #https://www.youtube.com/watch?v=jRpHmF-iuMI&t=266s
        self.master.table = ttk.Treeview(self.master.tabview.tab("Table"), columns = ("parameter", "value", "slice"), show = "headings")
        self.master.table.heading("parameter", text = "Parameter")
        self.master.table.heading("value", text = "Value")
        self.master.table.heading("slice", text = "Slice")
        self.master.table.pack(fill = "both", expand = True)
        self.master.table.grid(row=0, column=0, sticky = "news")
        
        self.master.table.bind('<Delete>', self.delete_items)
        
    def output_frame(self):
        self.master.output_frame = customtkinter.CTkFrame(self.master, fg_color = "transparent", corner_radius=(0))
        self.master.output_frame.grid(row=1, column=1, padx=(10,10), pady=(0,10), sticky='nsew')
        self.master.output_frame.columnconfigure(0, weight = 1)
        
        self.master.output_label = customtkinter.CTkLabel(self.master.output_frame,  text = "Output", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.master.output_label.grid(row =0, column = 0)
        
        self.master.results_label = customtkinter.CTkLabel(self.master.output_frame, text=" ", height = 50)
        self.master.results_label.grid(row =1, column = 0)
        
        self.master.keep_btn = customtkinter.CTkButton(self.master.output_frame, text = "Keep", font = ("Arial",18), )
        self.master.keep_btn.grid(row=2, column = 0)
        
    def button_frame(self):
        self.master.button_frame = customtkinter.CTkFrame(self.master, width = 250, fg_color="transparent", corner_radius=0)
        self.master.button_frame.grid(row=0, column=2, padx=(5,5), pady=(5,5), sticky="nsew")
        self.master.button_frame.columnconfigure((0,1), weight = 1)
        
        self.master.button_label = customtkinter.CTkLabel(self.master.button_frame, text="Deformity Parameters", anchor = "center", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.master.button_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10))
        
        self.master.param_info_btn = customtkinter.CTkButton(self.master.button_frame, text = "show landmarks", font = ("Arial",18), )
        self.master.param_info_btn.grid(row=1, column = 0, columnspan = 2, padx=(5,5), pady=(5,5), sticky= 'ew')
        
        self.master.param_btn1 = customtkinter.CTkButton(self.master.button_frame, text = "assymetry index", font = ("Arial",18), )
        self.master.param_btn1.grid(row=2, column = 0, padx=(5,5), pady=(5,5), sticky= 'ew')
        
        self.master.param_btn2 = customtkinter.CTkButton(self.master.button_frame, text = "trunk angle", font = ("Arial",18), )
        self.master.param_btn2.grid(row=2, column = 1, padx=(5,5), pady=(5,5), sticky = 'ew')
        
        self.master.param_btn3 = customtkinter.CTkButton(self.master.button_frame, text = "pectus index", font = ("Arial",18), )
        self.master.param_btn3.grid(row=3, column = 0, padx=(5,5), pady=(5,5), sticky = 'ew')
        
        self.master.param_btn4 = customtkinter.CTkButton(self.master.button_frame, text = "sagital diameter", font = ("Arial",18), )
        self.master.param_btn4.grid(row=3, column = 1, padx=(5,5), pady=(5,5), sticky = 'ew')
        
        self.master.param_btn5 = customtkinter.CTkButton(self.master.button_frame, text = "steep vertebral", font = ("Arial",18), )
        self.master.param_btn5.grid(row=4, column = 0, padx=(5,5), pady=(5,5), sticky = 'ew')
        
        self.master.param_btn6 = customtkinter.CTkButton(self.master.button_frame, text = "Param 6", font = ("Arial",18), )
        self.master.param_btn6.grid(row=4, column = 1, padx=(5,5), pady=(5,5), sticky = 'ew')
        
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    def on_closing(self):
        self.master.destroy()  # Close the window
        raise SystemExit  # Stop the kernel
    
    def delete_items(self):
        for i in self.table.selection():
            self.table.delete(i)
            
    def dummydef(self):
        print("test")

class GUI_Functionality:
    
    def __init__(self, master, layout):
        self.master = master
        self.layout = layout
        self.button = self.layout.button
        self.entry = self.layout.entry
        self.button.bind('<Button-1>', self.submit)
        
        
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    def on_closing(self):
        self.destroy()  # Close the window
        raise SystemExit  # Stop the kernel
    
    def delete_items(self):
        for i in self.table.selection():
            self.table.delete(i)
            
    def draw_image(self):
        self.subplot.cla()
        self.subplot.imshow(self.image_array[self.slice_number, :, :], cmap=self.map)
        self.subplot.axis('off')
        self.subplot.text(0.95, 0.05, f"slice number: {self.slice_number}", transform=self.subplot.transAxes,fontsize=10, color='white', ha='right', va='bottom')
        self.canvas.draw()
    
    def open_file(self):
        #open directory to find a file
        file_path = filedialog.askopenfile()
        
        if os.path.splitext(file_path.name)[1] == '.nii':
            image = sitk.ReadImage(file_path.name)
            self.image_array = sitk.GetArrayFromImage(image)
            self.draw_image()
        else:
            messagebox.showinfo(title="Message", message="incorrect file type")

    def skip_to_slice(self):
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
                    self.draw_image()
                else:
                    # error message in the text frame that the slice number is out of range
                    messagebox.showinfo(title="Message", message="Slice is out of range.")
        finally:
            self.slice_entry.delete(0, "end")

           
    def plus_slice(self):
        if self.image_array is not None:
            self.slice_number += 1
            if 0 <= self.slice_number <= np.shape(self.image_array)[0]:
                self.draw_image()
    
    def minus_slice(self):
        if self.image_array is not None:
            self.slice_number -= 1
            if 0 <= self.slice_number <= np.shape(self.image_array)[0]:
                self.draw_image()
                
    def get_points(self, num_points=4):
        #show the image in new window
        plt.imshow(self.image_array[self.slice_number, :, :],cmap=self.map)

        #emplty list for the points 
        pts = []
        
        #retreive the points 
        pts = np.asarray(plt.ginput(num_points, timeout=-1))
        
        #display the marked point in the GUI
        self.subplot.scatter(pts[:,0],pts[:,1], c="red", marker = "x")
        self.canvas.draw()
        
        plt.close()
        
        return pts
    
    def show_landmarks(self):
        print("to be implemented")
        
    def calc_assymetry_ind(self):
        if self.image_array is not None:
            pts = self.get_points(num_points=4)
            assymetry_ind = assymetry_index(pts)
            self.param_value = round(assymetry_ind,3)
            
            self.results_label = customtkinter.CTkLabel(self.output_frame, text=f"assymetry index: {self.param_value}", height = 50)
            self.results_label.grid(row =1, column = 0)
            self.current_param = "asymmetry index"
        else:
            messagebox.showinfo(title="Message", message="must open image first")
    
    def calc_trunk_angle(self):
        if self.image_array is not None:
            pts = self.get_points(num_points=2)
            angle_trunk_rot = angle_trunk_rotation(pts)
            self.param_value = round(angle_trunk_rot,3)
            
            self.results_label = customtkinter.CTkLabel(self.output_frame, text=f"angle trunk rotation: {self.param_value}", height = 50)
            self.results_label.grid(row =1, column = 0)
            self.current_param = "angle trunk rotation"
        else:
            messagebox.showinfo(title="Message", message="must open image first")
        
    def calc_pectus_index(self):
        if self.image_array is not None:
            pts = self.get_points(num_points=4)
            pectus_ind = pectus_index(pts)
            self.param_value = round(pectus_ind,3)
            
            self.results_label = customtkinter.CTkLabel(self.output_frame, text=f"pectus index: {self.param_value}", height = 50)
            self.results_label.grid(row =1, column = 0)
            self.current_param = "pectus index"
        else:
            messagebox.showinfo(title="Message", message="must open image first")
    
    def calc_sagital_diameter(self):
        if self.image_array is not None:
            pts = self.get_points(num_points=2)
            sagital_diam = sagital_diameter(pts)
            self.param_value = round(sagital_diam,3)
            
            self.results_label = customtkinter.CTkLabel(self.output_frame, text=f"sagital_diameter: {self.param_value}", height = 50)
            self.results_label.grid(row =1, column = 0)
            self.current_param = "sagital diameter"
        else:
            messagebox.showinfo(title="Message", message="must open image first")
    
    def calc_steep_vertebral(self):
        if self.image_array is not None:
            pts = self.get_points(num_points=2)
            steep_vert = steep_vertebral(pts)
            self.param_value = round(steep_vert,3)
            
            self.results_label = customtkinter.CTkLabel(self.output_frame, text=f"sagital_diameter: {self.param_value}", height = 50)
            self.results_label.grid(row =1, column = 0)
            self.current_param = "sagital diameter"
        else:
            messagebox.showinfo(title="Message", message="must open image first")
            
    def keep_parameters(self):
        if self.df_params is None:  
            self.df_params = pd.DataFrame({'Parameter': [], 'Value': [], "Slice":[]})
            
        if self.current_param is not None and self.param_value is not None:
            new_row = {'Parameter': self.current_param, 'Value': self.param_value, "Slice": self.slice_number}
            self.df_params = self.df_params.append(new_row, ignore_index=True)
            
            self.table.insert(parent= '', index = tk.END, values = (self.current_param, self.param_value, self.slice_number))
        else: 
            messagebox.showinfo(title="Message", message="first compute a parameter")
        
    def save_parameters(self):
        if self.df_params is not None:
            dialog = customtkinter.CTkInputDialog(text="give a name for the file:", title="save parameters")
            file_name = dialog.get_input()
            self.df_params.to_csv(f'{file_name}.csv', index=False)
    
    def dummydef(self):
        print("test")
    
class Application:
    def __init__(self, master):
        self.master = master
        self.layout = GUI_Layout(master)
        #self.functionality = Functionality(master, self.layout)


if __name__ == "__main__":
    
    root = customtkinter.CTk()
    app = Application(root)
    root.mainloop()

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        