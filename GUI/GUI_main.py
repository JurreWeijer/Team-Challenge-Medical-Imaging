# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 14:55:40 2023

@author: 20182371
"""

import customtkinter

from GUI.GUI_layout import GUI_Layout
from GUI.GUI_functionality import GUI_Functionality


    
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

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        