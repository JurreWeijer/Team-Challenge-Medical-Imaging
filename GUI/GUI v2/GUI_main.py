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

from GUI_layout import GUI_Layout
from GUI_functionality import GUI_Functionality


    
class Application:
    def __init__(self, master):
        self.master = master
        self.layout = GUI_Layout(master)
        self.functionality = GUI_Functionality(master, self.layout)


if __name__ == "__main__":
    
    root = customtkinter.CTk()
    #layout = GUI_Layout(root)
    #print(dir(layout.image_frame))
    app = Application(root)
    root.mainloop()

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        