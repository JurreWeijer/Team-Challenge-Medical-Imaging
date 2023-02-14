# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 18:23:32 2023

@author: 20182371
"""

import tkinter as tk 
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
import SimpleITK as sitk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

class MyGUI: 
    
    def __init__(self):
        
        self.root = tk.Tk()
        self.root.title("Scoliosis Chest Deformity")
        #self.root.geometry("800x500")
        
        self.button = tk.Button(self.root, text = "Open Image", font = ("Arial",18), command=self.mfileopen)
        self.button.pack(side= "bottom", padx=10,pady=10)
        
        self.button2 = tk.Button(self.root, text = "Assymetry Index", font = ("Arial",18), command=self.calc_assymetry_ind)
        self.button2.pack(side= "bottom", padx=10,pady=10)
        
        self.fig = plt.Figure(figsize=(5, 4), dpi=100)
        self.subplot = self.fig.add_subplot()
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        #self.label = tk.Label(self.root, text="Scolisis Chest Deformity", font=("Arial",18))
        #self.label.pack(padx=10,pady=10)
        
        self.root.mainloop()
        
    def mfileopen(self):
        #open directory to find a file
        file_path = filedialog.askopenfile()

        #get the image array
        if os.path.exists(file_path.name):
            image = sitk.ReadImage(file_path.name)
            self.image_array = sitk.GetArrayFromImage(image)
        else:
            print("File does not exist")
        
        #display the image in GUI
        self.subplot.imshow(self.image_array[200, :, :])
        self.canvas.draw() 
        
        
    def get_points(self, num_points=4):
        #show the image in new window
        plt.imshow(self.image_array[200, :, :])

        #emplty list for the points 
        self.pts = []
        
        #retreive the points 
        self.pts = np.asarray(plt.ginput(num_points, timeout=-1))
        
        #display the marked point in the GUI
        self.subplot.scatter(self.pts[:,0],self.pts[:,1], c="red")
        self.canvas.draw()
        
    def assymetry_index(self):
        pts = self.pts
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
        
        assymetry_ind = 1 - (Dist_AB/Dist_CD)
        
        return assymetry_ind
        
    def calc_assymetry_ind(self):
        self.get_points(num_points=4)
        assymetry_ind = self.assymetry_index()
        
        self.label = tk.Label(self.root, text=str(assymetry_ind), font=("Arial",18))
        self.label.pack(side = "bottom", padx=10,pady=10)
        
        print(assymetry_ind)
        
        
MyGUI()
        