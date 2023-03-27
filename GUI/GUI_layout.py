# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 17:10:27 2023

@author: 20182371
"""
import customtkinter
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import cv2 as cv
import Tools.Contouring


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
        self.master.grid_columnconfigure(1, weight=3)
        self.master.grid_columnconfigure(2, weight=2)
        self.master.grid_rowconfigure(0, weight=2)
        self.master.grid_rowconfigure(1, weight=1)
        
        #init frame functions
        self.sidebar()
        self.image_frame()
        self.output_frame()
        self.manual_buttons()
        self.landmark_extension_buttons()
        self.automatic_buttons()
        
    def sidebar(self):
        #creation of the sidebar frame 
        self.master.sidebar_frame = customtkinter.CTkFrame(self.master, width=140, corner_radius=0)
        self.master.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        
        #sidebar configure 
        self.master.sidebar_frame.columnconfigure(0, weight = 1)
        self.master.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        #components sidebar
        self.master.logo_label = customtkinter.CTkLabel(self.master.sidebar_frame, text="Menu", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.master.logo_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky = 'ew')
        
        self.master.button_help = customtkinter.CTkButton(self.master.sidebar_frame, text = "help", font = ("Arial",18), )
        self.master.button_help.grid(row=1, column = 0, padx=(10,10), pady=(10,10), sticky= 'ew')
        
        self.master.appearance_mode_label = customtkinter.CTkLabel(self.master.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.master.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0), sticky = 'ew')
        
        self.master.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.master.sidebar_frame, values=["Light", "Dark", "System"],command=self.change_appearance_mode_event)
        self.master.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10), sticky = 'ew')
        
    def image_frame(self):
        #creation of the image frame
        self.master.image_frame = customtkinter.CTkFrame(self.master, width = 400, height = 400,fg_color = 'transparent', corner_radius=0)
        self.master.image_frame.grid(row=0, column=1, sticky = "nsew")
        
        #congifure of the image frame 
        self.master.image_frame.columnconfigure((4,5), weight=1)
        self.master.image_frame.rowconfigure((0,1,2), weight=1)
        
        #transverse figure 
        self.master.trans_fig = plt.Figure(figsize=(4,4),dpi=100)
        self.master.trans_fig.set_facecolor(color = "white")
       
        self.master.trans_subplot = self.master.trans_fig.add_subplot()
        self.master.trans_subplot.axis("off")
        self.master.trans_subplot.set_facecolor(color = "white")
        
        #coronal figure
        self.master.coronal_fig = plt.Figure(figsize=(4,4),dpi=100)
        self.master.coronal_fig.set_facecolor(color = "white")
        
        self.master.coronal_subplot = self.master.coronal_fig.add_subplot()
        self.master.coronal_subplot.axis("off")
        self.master.coronal_subplot.set_facecolor(color = "white")
        
        #components of the image frame
        #https://matplotlib.org/3.1.0/gallery/user_interfaces/embedding_in_tk_sgskip.html
        self.master.image_label = customtkinter.CTkLabel(self.master.image_frame,  text = "Patient Image", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.master.image_label.grid(row =0, column = 0, columnspan = 10, padx=(10, 10), pady=(10, 10))
        
        self.master.trans_canvas = FigureCanvasTkAgg(self.master.trans_fig, master=self.master.image_frame)  # A tk.DrawingArea.
        self.master.trans_canvas.draw()
        self.master.trans_canvas.get_tk_widget().grid(row=1, column=0, columnspan=5, padx=(10,10), pady=(0,10), sticky = 'news')
        
        self.master.coronal_canvas = FigureCanvasTkAgg(self.master.coronal_fig, master=self.master.image_frame)  # A tk.DrawingArea.
        self.master.coronal_canvas.draw()
        self.master.coronal_canvas.get_tk_widget().grid(row=1, column=5, columnspan=5, padx=(10,10), pady=(0,10), sticky = 'news')
        
        self.master.slice_entry = customtkinter.CTkEntry(self.master.image_frame, width = 100, placeholder_text="Slice Number")
        self.master.slice_entry.grid(row=2, column=0, columnspan=1, padx=(10, 0), pady=(0, 0), sticky="ew")
        
        self.master.button_goto_slice = customtkinter.CTkButton(self.master.image_frame, width = 100, text="go to", )
        self.master.button_goto_slice.grid(row=2, column=1 ,padx=(0,10), pady=(0,0), sticky = 'ew')
        
        self.master.button_min = customtkinter.CTkButton(self.master.image_frame, width = 50, text="-", )
        self.master.button_min.grid(row=2, column=2,padx=(10,0), pady=(0,0), sticky = 'ew')
        
        self.master.button_plus = customtkinter.CTkButton(self.master.image_frame, width = 50, text="+", )
        self.master.button_plus.grid(row=2, column=3,padx=(0,10), pady=(0,0), sticky = 'ew')
        
        self.master.button_open_image = customtkinter.CTkButton(self.master.image_frame, width = 200, text="Open Image", )
        self.master.button_open_image.grid(row=2, column=4, columnspan = 2, padx=(10,10), pady=(0,0), sticky = "ew")
        
        self.master.button_backward = customtkinter.CTkButton(self.master.image_frame, width = 50, text="-", )
        self.master.button_backward.grid(row=2, column=6,padx=(10,0), pady=(0,0), sticky = 'ew')
        
        self.master.button_forward = customtkinter.CTkButton(self.master.image_frame, width = 50, text="+", )
        self.master.button_forward.grid(row=2, column=7,padx=(0,10), pady=(0,0), sticky = 'ew')
       
        self.master.coronal_slice_entry = customtkinter.CTkEntry(self.master.image_frame, width = 100, placeholder_text="Slice Number")
        self.master.coronal_slice_entry.grid(row=2, column=8, padx=(0, 0), pady=(0, 0), sticky="ew")
        
        self.master.coronal_button_goto_slice = customtkinter.CTkButton(self.master.image_frame, width = 100, text="go to", )
        self.master.coronal_button_goto_slice.grid(row=2, column=9, padx=(0,10), pady=(0,0), sticky = 'ew')
        
    def output_frame(self):
        #creation of the output frame
        self.master.output_frame = customtkinter.CTkFrame(self.master, width = 400, height = 400, fg_color = "transparent", corner_radius=(0))
        self.master.output_frame.grid(row=1, column=1, padx=(10,10), pady=(0,0), sticky='nsew')
        
        #configure of the output frame
        self.master.output_frame.columnconfigure(0, weight = 1)
        
        #components of the output frame
        self.master.output_label = customtkinter.CTkLabel(self.master.output_frame,  text = "Parameter values", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.master.output_label.grid(row =0, column = 0, padx=(10, 10), pady=(10, 10))
        
        #https://www.youtube.com/watch?v=jRpHmF-iuMI&t=266s
        self.master.table = ttk.Treeview(self.master.output_frame, columns = ("parameter", "value", "slice"), show = "headings")
        self.master.table.heading("parameter", text = "Parameter")
        self.master.table.heading("value", text = "Value")
        self.master.table.heading("slice", text = "Slice")
        self.master.table.grid(row=1, column=0, sticky = "news", padx = (5,5), pady = (5,0))
        
        self.master.table.bind('<Delete>', self.delete_items)
        
        self.master.button_save_parameters = customtkinter.CTkButton(self.master.output_frame, text="Save Parameters", )
        self.master.button_save_parameters.grid(row=3, column=0, padx=(5,5), pady=(5,5), sticky = 'ew')
        
    def manual_buttons(self):
        #creation of the button frame 
        self.master.button_frame = customtkinter.CTkFrame(self.master, width = 250, fg_color="transparent", corner_radius=0)
        self.master.button_frame.grid(row=0, column=2, rowspan = 2, padx=(5,5), pady=(5,5), sticky="nsew")
        
        #configure of the button frame
        self.master.button_frame.columnconfigure((0,1), weight = 1)
        
        #manual components of the button frame
        self.master.manual_parameter_label = customtkinter.CTkLabel(self.master.button_frame, text="Manual Parameters", anchor = "center", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.master.manual_parameter_label.grid(row=0, column=0, columnspan=2, padx=(10, 10), pady=(10, 10))
        
        self.master.button_assymetry_index = customtkinter.CTkButton(self.master.button_frame, text = "assymetry index", font = ("Arial",18), fg_color = "sky blue")
        self.master.button_assymetry_index.grid(row=1, column = 0, padx=(5,5), pady=(5,5), sticky= 'ew')
        
        self.master.button_trunk_angle = customtkinter.CTkButton(self.master.button_frame, text = "trunk angle", font = ("Arial",18), fg_color = "dodger blue")
        self.master.button_trunk_angle.grid(row=1, column = 1, padx=(5,5), pady=(5,5), sticky = 'ew')
        
        self.master.button_pectus_index = customtkinter.CTkButton(self.master.button_frame, text = "pectus index", font = ("Arial",18), fg_color = "SlateBlue3")
        self.master.button_pectus_index.grid(row=2, column = 0, padx=(5,5), pady=(5,5), sticky = 'ew')
        
        self.master.button_sagital_diameter = customtkinter.CTkButton(self.master.button_frame, text = "sagital diameter", font = ("Arial",18), fg_color = "medium blue")
        self.master.button_sagital_diameter.grid(row=2, column = 1, padx=(5,5), pady=(5,5), sticky = 'ew')
        
        self.master.button_steep_vertebral = customtkinter.CTkButton(self.master.button_frame, text = "steep vertebral", font = ("Arial",18), fg_color = "midnight blue")
        self.master.button_steep_vertebral.grid(row=3, column = 0, padx=(5,5), pady=(5,5), sticky = 'ew')
        
    def landmark_extension_buttons(self):
        #landmark extenstion components of the button frame
        self.master.landmark_extention_label = customtkinter.CTkLabel(self.master.button_frame, text="Landmark Extension", anchor = "center", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.master.landmark_extention_label.grid(row=4, column=0, columnspan=2, padx=(10, 10), pady=(10, 10))
        
        self.master.parameter_menu = customtkinter.CTkOptionMenu(self.master.button_frame, dynamic_resizing=False,
                                                        values=["Angle Trunk Rotation", "Assymetry Index", "Pectus Index", "Saggital Diameter", "Steep Vertebral"])
        self.master.parameter_menu.grid(row=5, column=0, columnspan = 2, padx=(10, 10), pady=(10, 10), sticky = 'ew')
        
        self.master.button_begin = customtkinter.CTkButton(self.master.button_frame, text = "set startpoint", font = ("Arial",18), )
        self.master.button_begin.grid(row=6, column = 0, padx=(5,5), pady=(5,5), sticky = 'ew')
        
        self.master.button_end = customtkinter.CTkButton(self.master.button_frame, text = "set endpoint", font = ("Arial",18), )
        self.master.button_end.grid(row=6, column = 1, padx=(5,5), pady=(5,5), sticky = 'ew')
        
        self.master.button_landmark_extension = customtkinter.CTkButton(self.master.button_frame, text = "compute landmarks", font = ("Arial",18), )
        self.master.button_landmark_extension.grid(row=7, column = 0, columnspan = 2, padx=(5,5), pady=(5,5), sticky = 'ew')
        
        self.master.button_change_landmarks = customtkinter.CTkButton(self.master.button_frame, text = "change landmarks", font = ("Arial",18), )
        self.master.button_change_landmarks.grid(row=8, column = 0, columnspan = 2, padx=(5,5), pady=(5,5), sticky = 'ew')
        
        self.master.compute_parameters = customtkinter.CTkButton(self.master.button_frame, text = "compute parameter", font = ("Arial",18), )
        self.master.compute_parameters.grid(row=9, column = 0, columnspan = 1, padx=(5,5), pady=(5,5), sticky = 'ew')
        
        self.master.button_compute_rib_rotation = customtkinter.CTkButton(self.master.button_frame, text = "compute rib parameter", font = ("Arial",18), )
        self.master.button_compute_rib_rotation.grid(row=9, column = 1, columnspan = 1, padx=(5,5), pady=(5,5), sticky = 'ew')
        
    def automatic_buttons(self):
        #automatic landmarks components of the button frame
        self.master.manual_parameter_label = customtkinter.CTkLabel(self.master.button_frame, text="Automatic Parameters", anchor = "center", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.master.manual_parameter_label.grid(row= 10, column=0, columnspan=2, padx=(10, 10), pady=(10, 10))

        self.master.button_segment = customtkinter.CTkButton(self.master.button_frame, text = "Segment Image", font = ("Arial",18), )
        self.master.button_segment.grid(row=11, column = 0, columnspan = 2, padx=(5,5), pady=(5,5), sticky = 'ew')
        
        self.master.button_show_trans_segment = customtkinter.CTkButton(self.master.button_frame, text = "Transverse Segmentation", font = ("Arial",18), )
        self.master.button_show_trans_segment.grid(row=12, column = 0, padx=(5,5), pady=(5,5), sticky = 'ew')
        
        self.master.button_show_coronal_segment = customtkinter.CTkButton(self.master.button_frame, text = "Coronal Segmentation", font = ("Arial",18), )
        self.master.button_show_coronal_segment.grid(row=12, column = 1, padx=(5,5), pady=(5,5), sticky = 'ew')
        
        #self.master.button_calculate_contour = customtkinter.CTkButton(self.master.button_frame, text = "Show Contour", font = ("Arial",18), )
        #self.master.button_calculate_contour.grid(row=13, column = 0, columnspan = 1, padx=(5,5), pady=(5,5), sticky = 'ew')
        
        #self.master.button_remove_contour = customtkinter.CTkButton(self.master.button_frame, text = "Remove Contour", font = ("Arial",18), )
        #self.master.button_remove_contour.grid(row=13, column = 1, columnspan = 1, padx=(5,5), pady=(5,5), sticky = 'ew')
        
        self.master.button_load_contour = customtkinter.CTkButton(self.master.button_frame, text = "Load Contour", font = ("Arial",18), )
        self.master.button_load_contour.grid(row=13, column = 0, columnspan = 2, padx=(5,5), pady=(5,5), sticky = 'ew')

        self.master.button_auto_parameter = customtkinter.CTkButton(self.master.button_frame, text = "Calculate landmarks", font = ("Arial",18), )
        self.master.button_auto_parameter.grid(row=14, column = 0, columnspan = 2, padx=(5,5), pady=(5,5), sticky = 'ew')
        
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    def delete_items(self):
        for i in self.table.selection():
            self.table.delete(i)
            
    def on_closing(self):
        self.master.destroy()  
        raise SystemExit  
    
    def draw_image(self, trans_image, coronal_image, trans_slice, coronal_slice, contour, start_le, end_le, cmap):
        
        #transverse subplot 
        self.master.trans_subplot.cla()
        self.master.trans_subplot.imshow(trans_image[trans_slice, :, :],  cmap=cmap)
        self.master.trans_subplot.axis('off')
        self.master.trans_subplot.text(0.95, 0.03, f"slice number: {trans_slice+1}", transform=self.master.trans_subplot.transAxes, fontsize=10, color='white', ha='right', va='bottom')
        self.master.trans_subplot.set_ylim(0,trans_image.shape[0])
        self.master.trans_subplot.axhline(y=coronal_slice, color='r', linewidth=1)
        self.master.trans_canvas.draw()
        
        #coronal subplot
        self.master.coronal_subplot.cla()
        self.master.coronal_subplot.imshow(coronal_image[:, coronal_slice, :], cmap=cmap)
        self.master.coronal_subplot.axis('off')
        self.master.coronal_subplot.invert_yaxis()
        self.master.coronal_subplot.axhline(y=trans_slice, color='r', linewidth=1)
        if start_le is not None: 
            self.master.coronal_subplot.axhline(y=start_le, color='b', linewidth=1)
        if end_le is not None: 
            self.master.coronal_subplot.axhline(y=end_le, color = 'b', linewidth=1)
        self.master.coronal_subplot.text(0.95, 0.03, f"slice number: {coronal_slice+1}", transform=self.master.trans_subplot.transAxes, fontsize=10, color='white', ha='right', va='bottom')
        self.master.coronal_canvas.draw()
        
        if contour == True:
            centroids = Tools.Contouring.MultiSliceContour(trans_image, trans_slice)
            hull = cv.convexHull(centroids[1:])
            slice = trans_image[trans_slice,:,:]
            canvas = np.zeros_like(slice)
            
            cv.drawContours(canvas, [hull], 0, color = (255,255,255), thickness= 2)  
            self.master.trans_subplot.scatter(hull[:,0,0], hull[:,0,1], c = "blue")
            self.master.trans_subplot.imshow(canvas, alpha = 0.3, cmap= "gray")
        
        self.master.trans_canvas.draw()
        self.master.coronal_canvas.draw()
        
    def show_landmarks(self, trans_image, trans_slice, coronal_slice, dict_landmarks, cmap):
        
        #check if there are landmarks for the slice and retreive them
        if f"slice_{trans_slice}" in dict_landmarks:
            landmarks_x = []
            landmarks_y = []
            for k in dict_landmarks[f"slice_{trans_slice}"].keys():
                landmarks_x.append(dict_landmarks[f"slice_{trans_slice}"][k][0])
                landmarks_y.append(dict_landmarks[f"slice_{trans_slice}"][k][1])
            
            
            self.master.trans_subplot.cla()
            self.master.trans_subplot.imshow(trans_image[trans_slice, :, :], cmap=cmap)
            self.master.trans_subplot.axis('off')
            self.master.trans_subplot.text(0.95, 0.03, f"slice number: {trans_slice}", transform=self.master.trans_subplot.transAxes, fontsize=10, color='white', ha='right', va='bottom')
            self.master.trans_subplot.set_ylim(0,trans_image.shape[0])
            self.master.trans_subplot.axhline(y=coronal_slice, color='r', linewidth=1)
            self.master.trans_subplot.scatter(landmarks_x,landmarks_y, c="red", marker = "x")
            self.master.trans_canvas.draw()
            self.master.coronal_canvas.draw()
    
        
        