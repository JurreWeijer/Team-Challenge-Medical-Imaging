# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 16:14:50 2023

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

"""
Known bugs: 
    - Changing the tab view is horrible as everything changes in size, this is because of the treview and canvas used withing the tab
      probably best to remove the tab and the put table somewhere else in the GUI
    - The figure does nog change size when you enlarge the screen resulting in quite a big area that is not use
    - Only the assymetry index is currently implemented. 

"""

class MyGUI(customtkinter.CTk): 
    
    def __init__(self):
        super().__init__()
        
        #global variables
        self.image_array = None
        self.slice_number = 200
        self.map = "gray"
        self.df_params = None
        self.param_value = None
        self.current_param = None 
        
        # configure window
        self.title("Scoliosis Chest Deformity")
        self.protocol("WM_DELETE_WINDOW", self.on_closing) 
        
        # configure grid layout
        self.grid_columnconfigure(0,weight = 1)
        self.grid_columnconfigure((1), weight=3)
        self.grid_columnconfigure((2), weight=2)
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=1)
        
        #---------------------------------------- Side bar ----------------------------------------
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar_frame.columnconfigure(0, weight = 1)
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Menu", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky = 'ew')
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Save Parameters", command=self.save_parameters)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10, sticky = 'ew')
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0), sticky = 'ew')
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10), sticky = 'ew')
        
        #---------------------------------------- Center frame ----------------------------------------
        self.image_frame = customtkinter.CTkFrame(self, width = 500, height = 700,fg_color = 'transparent', corner_radius=0)
        self.image_frame.grid(row=0, column=1, sticky = "nsew")
        self.image_frame.columnconfigure(0, weight = 1)
        self.image_frame.rowconfigure(1, weight = 1)
        
        self.image_label = customtkinter.CTkLabel(self.image_frame,  text = "Patient Image", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.image_label.grid(row =0, column = 0,padx=20, pady=(20, 10))
        
        #tab views
        self.tabview = customtkinter.CTkTabview(self.image_frame)
        self.tabview.grid(row=1, column=0, sticky = "nsew")
        self.tabview.add("Image")
        self.tabview.add("Table")
        self.tabview.tab("Image").grid_columnconfigure((0,3), weight=1)
        self.tabview.tab("Image").grid_rowconfigure((0,1,2), weight=1)
        self.tabview.tab("Table").grid_columnconfigure((0), weight=1)
        self.tabview.tab("Table").grid_rowconfigure((0), weight=1)
        
        #---------------------------------------- Image tab ----------------------------------------
        self.fig = plt.Figure(figsize=(4,4),dpi=100)
        self.fig.set_facecolor(color = "white")
        self.subplot = self.fig.add_subplot()
        self.subplot.axis("off")
        self.subplot.set_facecolor(color = "white")
        
        #https://matplotlib.org/3.1.0/gallery/user_interfaces/embedding_in_tk_sgskip.html
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tabview.tab("Image"))  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=5, padx=(10,10), pady=(10,10))
        
        self.btn_open_image = customtkinter.CTkButton(self.tabview.tab("Image"), width = 200, text="Open Image", command=self.open_file)
        self.btn_open_image.grid(row=2, column=0,padx=(10,10), pady=(0,0), sticky = "w")
        
        self.plus_btn = customtkinter.CTkButton(self.tabview.tab("Image"), width = 50, text="-", command=self.minus_slice)
        self.plus_btn.grid(row=2, column=1,padx=(10,0), pady=(0,0), sticky = 'ew')
        
        self.minus_btn = customtkinter.CTkButton(self.tabview.tab("Image"), width = 50, text="+", command=self.plus_slice)
        self.minus_btn.grid(row=2, column=2,padx=(0,10), pady=(0,0), sticky = 'e')
        
        self.slice_entry = customtkinter.CTkEntry(self.tabview.tab("Image"), width = 100, placeholder_text="Slice Number")
        self.slice_entry.grid(row=2, column=3, columnspan=1, padx=(0, 0), pady=(0, 0), sticky="e")
        
        self.skipto_btn = customtkinter.CTkButton(self.tabview.tab("Image"), width = 100, text="skip to", command=self.skip_to_slice)
        self.skipto_btn.grid(row=2, column=4 ,padx=(0,10), pady=(0,0), sticky = 'e')
        
        #---------------------------------------- Table tab ----------------------------------------
        
        #https://www.youtube.com/watch?v=jRpHmF-iuMI&t=266s
        self.table = ttk.Treeview(self.tabview.tab("Table"), columns = ("parameter", "value", "slice"), show = "headings")
        self.table.heading("parameter", text = "Parameter")
        self.table.heading("value", text = "Value")
        self.table.heading("slice", text = "Slice")
        self.table.pack(fill = "both", expand = True)
        self.table.grid(row=0, column=0, sticky = "news")
        
        self.table.bind('<Delete>', self.delete_items)
        
        #---------------------------------------- Output frame ----------------------------------------
        self.output_frame = customtkinter.CTkFrame(self, fg_color = "transparent", corner_radius=(0))
        self.output_frame.grid(row=1, column=1, padx=(10,10), pady=(0,10), sticky='nsew')
        self.output_frame.columnconfigure(0, weight = 1)
        
        self.output_label = customtkinter.CTkLabel(self.output_frame,  text = "Output", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.output_label.grid(row =0, column = 0)
        
        self.results_label = customtkinter.CTkLabel(self.output_frame, text=" ", height = 50)
        self.results_label.grid(row =1, column = 0)
        
        self.keep_btn = customtkinter.CTkButton(self.output_frame, text = "Keep", font = ("Arial",18), command=self.keep_parameters)
        self.keep_btn.grid(row=2, column = 0)
        
        #---------------------------------------- Button frame ----------------------------------------
        self.button_frame = customtkinter.CTkFrame(self, width = 250, fg_color="transparent", corner_radius=0)
        self.button_frame.grid(row=0, column=2, padx=(5,5), pady=(5,5), sticky="nsew")
        self.button_frame.columnconfigure((0,1), weight = 1)
        
        self.button_label = customtkinter.CTkLabel(self.button_frame, text="Deformity Parameters", anchor = "center", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.button_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10))
        
        self.param_btn1 = customtkinter.CTkButton(self.button_frame, text = "assymetry index", font = ("Arial",18), command=self.calc_assymetry_ind	)
        self.param_btn1.grid(row=1, column = 0, padx=(5,5), pady=(5,5), sticky= 'ew')
        
        self.param_btn2 = customtkinter.CTkButton(self.button_frame, text = "Param 2", font = ("Arial",18), command=self.dummydef)
        self.param_btn2.grid(row=1, column = 1, padx=(5,5), pady=(5,5), sticky = 'ew')
        
        self.param_btn3 = customtkinter.CTkButton(self.button_frame, text = "Param 3", font = ("Arial",18), command=self.dummydef)
        self.param_btn3.grid(row=2, column = 0, padx=(5,5), pady=(5,5), sticky = 'ew')
        
        self.param_btn4 = customtkinter.CTkButton(self.button_frame, text = "Param 4", font = ("Arial",18), command=self.dummydef)
        self.param_btn4.grid(row=2, column = 1, padx=(5,5), pady=(5,5), sticky = 'ew')
        
        self.param_btn5 = customtkinter.CTkButton(self.button_frame, text = "Param 5", font = ("Arial",18), command=self.dummydef)
        self.param_btn5.grid(row=3, column = 0, padx=(5,5), pady=(5,5), sticky = 'ew')
        
        self.param_btn6 = customtkinter.CTkButton(self.button_frame, text = "Param 6", font = ("Arial",18), command=self.dummydef)
        self.param_btn6.grid(row=3, column = 1, padx=(5,5), pady=(5,5), sticky = 'ew')
        
    
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    def on_closing(self):
        # Perform any necessary cleanup or save operations here
        self.destroy()  # Close the window
        raise SystemExit  # Stop the kernel
    
    def delete_items(self):
        for i in self.table.selection():
            self.table.delete(i)
    
    def open_file(self):
        #open directory to find a file
        file_path = filedialog.askopenfile()
      
        if os.path.exists(file_path.name):
            if os.path.splitext(file_path.name)[1] == '.nii':
                image = sitk.ReadImage(file_path.name)
                self.image_array = sitk.GetArrayFromImage(image)
                #display the image in GUI
                self.subplot.imshow(self.image_array[self.slice_number, :, :], cmap=self.map)
                self.canvas.draw()
            else:
                messagebox.showinfo(title="Message", message="incorrect file type")  
        else:
            messagebox.showinfo(title="Message", message="incorrect file type")
        
    def skip_to_slice(self):
        #dialog = customtkinter.CTkInputDialog(text="Type in a slice number:", title="slice number input")
        dialog_input = self.slice_entry.get()
        
        #first try of the input can be change to an integer
        try:
            #check is an image if already opened
            if self.image_array is not None:
                self.slice_number = int(dialog_input)
                #check if the slice number is withint the range of the image
                if 0 <= self.slice_number <= np.shape(self.image_array)[0]:
                    #show the image in the subplot 
                    self.subplot.imshow(self.image_array[self.slice_number, :, :],cmap=self.map)
                    self.canvas.draw()
                    self.slice_entry.delete(0,"end")
                else:
                    #error message in the text frame that the slice number is out of range
                    messagebox.showinfo(title="Message", message="slice is out of range")
                    self.slice_entry.delete(0,"end")
            #else:
                #error message that first an image should be opened
            #    messagebox.showinfo(title="Message", message="must open image before changing the slice")
                
        except ValueError:
            #error message if the input is not an integer
            messagebox.showinfo(title="Message", message="must give integer to change the slice")
            self.slice_entry.delete(0,"end")
    
    def plus_slice(self):
        if self.image_array is not None:
            self.slice_number += 1
            if 0 <= self.slice_number <= np.shape(self.image_array)[0]:
                self.subplot.imshow(self.image_array[self.slice_number, :, :],cmap=self.map)
                self.canvas.draw()
    
    def minus_slice(self):
        if self.image_array is not None:
            self.slice_number -= 1
            if 0 <= self.slice_number <= np.shape(self.image_array)[0]:
                self.subplot.imshow(self.image_array[self.slice_number, :, :],cmap=self.map)
                self.canvas.draw()
                
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
    
    def assymetry_index(self,pts):
        #pts = self.pts
        Ax = int(pts[0,0])
        Ay = int(pts[0,1])
        Bx = int(pts[1,0])
        By = int(pts[1,1])
        Cx = int(pts[2,0])
        Cy = int(pts[2,1])
        Dx = int(pts[3,0])
        Dy = int(pts[3,1])
        
        Dist_AB = math.sqrt((Bx-Ax)^2 + (By-Ay)^2)
        Dist_CD = math.sqrt((Dx-Cx)^2 + (Dy-Cy)^2)
        
        assymetry_ind = abs(1 - (Dist_AB/Dist_CD))
        
        return assymetry_ind
        
    def calc_assymetry_ind(self):
        if self.image_array is not None:
            pts = self.get_points(num_points=4)
            assymetry_ind = self.assymetry_index(pts)
            self.param_value = round(assymetry_ind,3)
            
            self.results_label = customtkinter.CTkLabel(self.output_frame, text=f"assymetry index: {self.param_value}", height = 50)
            self.results_label.grid(row =1, column = 0)
            self.current_param = "asymmetry index"
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

#class assymetry_parameters():
    
    

if __name__ == "__main__":
    app = MyGUI()
    app.mainloop()