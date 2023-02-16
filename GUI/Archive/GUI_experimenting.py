# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 19:15:56 2023

@author: 20182371
"""

import tkinter as tk 
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
import SimpleITK as sitk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


class MyGUI: 
    
    def __init__(self):
        
        self.root = tk.Tk()
        self.root.title("Scoliosis Chest Deformity")
        #self.root.geometry("800x500")
        
        self.button = tk.Button(self.root, text = "Open Image", font = ("Arial",18), command=self.mfileopen)
        self.button.pack(side= "right", padx=10,pady=10)
        
        self.button2 = tk.Button(self.root, text = "Open Image", font = ("Arial",18), command=self.mfileopen)
        self.button2.pack(side= "right", padx=10,pady=10)
        
        self.fig = plt.Figure(figsize=(5, 4), dpi=100)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        #self.canvas._tkcanvas.pack(side="top", fill="both", expand=1)
        
        #self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        #self.toolbar.update()
        #self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        #self.label = tk.Label(self.root, text="Scolisis Chest Deformity", font=("Arial",18))
        #self.label.pack(padx=10,pady=10)
        
        #self.textbox = tk.Text(self.root, height = 1, font = ("Arial", 16))
        #self.textbox.pack(padx=10,pady=10)
        
        #self.check_state = tk.IntVar()
        
        #self.check = tk.Checkbutton(self.root, text = "Show Messagebox", font = ("Arial", 16), variable=self.check_state)
        #self.check.pack(padx=10,pady=10)
        
        self.root.mainloop()
        
    def mfileopen(self):
        file_path = filedialog.askopenfile()
        #print(file_path.name)
        if os.path.exists(file_path.name):
            image = sitk.ReadImage(file_path.name)
            image_array = sitk.GetArrayFromImage(image)
        else:
            print("File does not exist")
        
        a = self.fig.add_subplot(111)
        a.imshow(image_array[200, :, :])
        self.canvas.draw()
        
        
    def show_message(self):
        if self.check_state.get() == 0:
            print(self.textbox.get("1.0",tk.END))
        else:
            messagebox.showinfo(title="Message", message=self.textbox.get("1.0",tk.END))  
            
    
MyGUI()