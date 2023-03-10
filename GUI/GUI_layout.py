# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 17:10:27 2023

@author: 20182371
"""
import customtkinter
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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
        self.manual_buttons()
        self.landmark_extension_buttons()
        self.automatic_buttons()
        
    def sidebar(self):
        self.master.sidebar_frame = customtkinter.CTkFrame(self.master, width=140, corner_radius=0)
        self.master.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        
        self.master.sidebar_frame.columnconfigure(0, weight = 1)
        self.master.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.master.logo_label = customtkinter.CTkLabel(self.master.sidebar_frame, text="Menu", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.master.logo_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky = 'ew')
        
        self.master.appearance_mode_label = customtkinter.CTkLabel(self.master.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.master.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0), sticky = 'ew')
        
        self.master.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.master.sidebar_frame, values=["Light", "Dark", "System"],command=self.change_appearance_mode_event)
        self.master.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10), sticky = 'ew')
        
    def image_frame(self):
        self.master.image_frame = customtkinter.CTkFrame(self.master, width = 400, height = 400,fg_color = 'transparent', corner_radius=0)
        self.master.image_frame.grid(row=0, column=1, sticky = "nsew")
        self.master.image_frame.columnconfigure((0,3), weight=1)
        self.master.image_frame.rowconfigure((0,1,2), weight=1)
        
        self.master.image_label = customtkinter.CTkLabel(self.master.image_frame,  text = "Patient Image", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.master.image_label.grid(row =0, column = 0, columnspan = 5, padx=(10, 10), pady=(10, 10))
        
        #tab views
        #self.master.tabview = customtkinter.CTkTabview(self.master.image_frame)
        #self.master.tabview.grid(row=1, column=0, sticky = "nsew")
        #self.master.tabview.add("Image")
        #self.master.tabview.add("Table")
        #self.master.tabview.tab("Image").grid_columnconfigure((0,3), weight=1)
        #self.master.tabview.tab("Image").grid_rowconfigure((0,1,2), weight=1)
        #self.master.tabview.tab("Table").grid_columnconfigure((0), weight=1)
        #self.master.tabview.tab("Table").grid_rowconfigure((0), weight=1)
        
        #---------------------------------------- Image tab ----------------------------------------
        self.master.fig = plt.Figure(figsize=(4,4),dpi=100)
        self.master.fig.set_facecolor(color = "white")
        self.master.subplot = self.master.fig.add_subplot()
        self.master.subplot.axis("off")
        self.master.subplot.set_facecolor(color = "white")
        
        #https://matplotlib.org/3.1.0/gallery/user_interfaces/embedding_in_tk_sgskip.html
        self.master.canvas = FigureCanvasTkAgg(self.master.fig, master=self.master.image_frame)  # A tk.DrawingArea.
        self.master.canvas.draw()
        self.master.canvas.get_tk_widget().grid(row=1, column=0, columnspan=5, padx=(10,10), pady=(0,10), sticky = 'news')
        
        self.master.button_open_image = customtkinter.CTkButton(self.master.image_frame, width = 200, text="Open Image", )
        self.master.button_open_image.grid(row=2, column=0,padx=(10,10), pady=(0,0), sticky = "w")
        
        self.master.button_min = customtkinter.CTkButton(self.master.image_frame, width = 50, text="-", )
        self.master.button_min.grid(row=2, column=1,padx=(10,0), pady=(0,0), sticky = 'ew')
        
        self.master.button_plus = customtkinter.CTkButton(self.master.image_frame, width = 50, text="+", )
        self.master.button_plus.grid(row=2, column=2,padx=(0,10), pady=(0,0), sticky = 'e')
        
        self.master.slice_entry = customtkinter.CTkEntry(self.master.image_frame, width = 100, placeholder_text="Slice Number")
        self.master.slice_entry.grid(row=2, column=3, columnspan=1, padx=(0, 0), pady=(0, 0), sticky="e")
        
        self.master.button_goto_slice = customtkinter.CTkButton(self.master.image_frame, width = 100, text="go to", )
        self.master.button_goto_slice.grid(row=2, column=4 ,padx=(0,10), pady=(0,0), sticky = 'e')
        
        
    def output_frame(self):
        self.master.output_frame = customtkinter.CTkFrame(self.master, fg_color = "transparent", corner_radius=(0))
        self.master.output_frame.grid(row=1, column=1, padx=(10,10), pady=(0,10), sticky='nsew')
        self.master.output_frame.columnconfigure(0, weight = 1)
        
        self.master.output_label = customtkinter.CTkLabel(self.master.output_frame,  text = "Parameter values", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.master.output_label.grid(row =0, column = 0, padx=(10, 10), pady=(10, 10))
        
        #https://www.youtube.com/watch?v=jRpHmF-iuMI&t=266s
        self.master.table = ttk.Treeview(self.master.output_frame, columns = ("parameter", "value", "slice"), show = "headings")
        self.master.table.heading("parameter", text = "Parameter")
        self.master.table.heading("value", text = "Value")
        self.master.table.heading("slice", text = "Slice")
        #self.master.table.pack(fill = "both", expand = True)
        self.master.table.grid(row=1, column=0, sticky = "news", padx = (5,5), pady = (5,0))
        
        self.master.table.bind('<Delete>', self.delete_items)
        
        self.master.button_save_parameters = customtkinter.CTkButton(self.master.output_frame, text="Save Parameters", )
        self.master.button_save_parameters.grid(row=3, column=0, padx=(5,5), pady=(5,5), sticky = 'ew')
        
        #self.master.output_label = customtkinter.CTkLabel(self.master.output_frame,  text = "Output", font=customtkinter.CTkFont(size=20, weight="bold"))
        #self.master.output_label.grid(row =0, column = 0)
        
        #self.master.results_label = customtkinter.CTkLabel(self.master.output_frame, text=" ", height = 50)
        #self.master.results_label.grid(row =1, column = 0)
        
        #self.master.keep_btn = customtkinter.CTkButton(self.master.output_frame, text = "Keep", font = ("Arial",18), )
        #self.master.keep_btn.grid(row=2, column = 0)
        
    def manual_buttons(self):
        self.master.button_frame = customtkinter.CTkFrame(self.master, width = 250, fg_color="transparent", corner_radius=0)
        self.master.button_frame.grid(row=0, column=2, padx=(5,5), pady=(5,5), sticky="nsew")
        self.master.button_frame.columnconfigure((0,1), weight = 1)
        
        self.master.manual_parameter_label = customtkinter.CTkLabel(self.master.button_frame, text="Manual Parameters", anchor = "center", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.master.manual_parameter_label.grid(row=0, column=0, columnspan=2, padx=(10, 10), pady=(10, 10))
        
        self.master.param_info_btn = customtkinter.CTkButton(self.master.button_frame, text = "show landmarks", font = ("Arial",18), )
        self.master.param_info_btn.grid(row=1, column = 0, columnspan = 2, padx=(5,5), pady=(0,5), sticky= 'ew')
        
        self.master.button_assymetry_index = customtkinter.CTkButton(self.master.button_frame, text = "assymetry index", font = ("Arial",18), )
        self.master.button_assymetry_index.grid(row=2, column = 0, padx=(5,5), pady=(5,5), sticky= 'ew')
        
        self.master.button_trunk_angle = customtkinter.CTkButton(self.master.button_frame, text = "trunk angle", font = ("Arial",18), )
        self.master.button_trunk_angle.grid(row=2, column = 1, padx=(5,5), pady=(5,5), sticky = 'ew')
        
        self.master.button_pectus_index = customtkinter.CTkButton(self.master.button_frame, text = "pectus index", font = ("Arial",18), )
        self.master.button_pectus_index.grid(row=3, column = 0, padx=(5,5), pady=(5,5), sticky = 'ew')
        
        self.master.button_sagital_diameter = customtkinter.CTkButton(self.master.button_frame, text = "sagital diameter", font = ("Arial",18), )
        self.master.button_sagital_diameter.grid(row=3, column = 1, padx=(5,5), pady=(5,5), sticky = 'ew')
        
        self.master.button_steep_vertebral = customtkinter.CTkButton(self.master.button_frame, text = "steep vertebral", font = ("Arial",18), )
        self.master.button_steep_vertebral.grid(row=4, column = 0, padx=(5,5), pady=(5,5), sticky = 'ew')
        
        self.master.param_btn6 = customtkinter.CTkButton(self.master.button_frame, text = "Param 6", font = ("Arial",18), )
        self.master.param_btn6.grid(row=4, column = 1, padx=(5,5), pady=(5,5), sticky = 'ew')
        
    def landmark_extension_buttons(self):
        
        self.master.manual_parameter_label = customtkinter.CTkLabel(self.master.button_frame, text="Landmark Extension", anchor = "center", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.master.manual_parameter_label.grid(row=5, column=0, columnspan=2, padx=(10, 10), pady=(10, 10))
        
        self.master.parameter_menu = customtkinter.CTkOptionMenu(self.master.button_frame, dynamic_resizing=False,
                                                        values=["Angle Trunk Rotation", "Assymetry Index", "Pectus Index", "Saggital Diameter", "Steep Vertebral"])
        self.master.parameter_menu.grid(row=6, column=0, columnspan = 2, padx=(10, 10), pady=(10, 10), sticky = 'ew')
        
        self.master.button_begin = customtkinter.CTkButton(self.master.button_frame, text = "set startpoint", font = ("Arial",18), )
        self.master.button_begin.grid(row=7, column = 0, padx=(5,5), pady=(5,5), sticky = 'ew')
        
        self.master.button_end = customtkinter.CTkButton(self.master.button_frame, text = "set endpoint", font = ("Arial",18), )
        self.master.button_end.grid(row=7, column = 1, padx=(5,5), pady=(5,5), sticky = 'ew')
        
        self.master.button_landmark_extension = customtkinter.CTkButton(self.master.button_frame, text = "compute landmarks", font = ("Arial",18), )
        self.master.button_landmark_extension.grid(row=8, column = 0, columnspan = 2, padx=(5,5), pady=(5,5), sticky = 'ew')
        
        self.master.compute_parameters = customtkinter.CTkButton(self.master.button_frame, text = "compute parameter", font = ("Arial",18), )
        self.master.compute_parameters.grid(row=9, column = 0, columnspan = 2, padx=(5,5), pady=(5,5), sticky = 'ew')
        
    def automatic_buttons(self):
        
        self.master.manual_parameter_label = customtkinter.CTkLabel(self.master.button_frame, text="Automatic Parameters", anchor = "center", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.master.manual_parameter_label.grid(row= 10, column=0, columnspan=2, padx=(10, 10), pady=(10, 10))
        
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    def on_closing(self):
        self.master.destroy()  # Close the window
        raise SystemExit  # Stop the kernel
    
    def delete_items(self):
        for i in self.table.selection():
            self.table.delete(i)
    
    def draw_image(self, data, n_slice, cmap):
        self.master.subplot.cla()
        self.master.subplot.imshow(data[n_slice, :, :], cmap=cmap)
        self.master.subplot.axis('off')
        self.master.subplot.text(0.95, 0.05, f"slice number: {n_slice}", transform=self.master.subplot.transAxes, fontsize=10, color='white', ha='right', va='bottom')
        self.master.canvas.draw()
    
    def draw_landmarks(self, landmarks):
        #display the marked point in the GUI
        self.master.subplot.scatter(landmarks[:,0],landmarks[:,1], c="red", marker = "x")
        self.master.canvas.draw()
    
    def show_landmarks(self, n_slice, dict_landmarks):
        
        if f"slice_{n_slice}" in dict_landmarks:
            landmarks_x = []
            landmarks_y = []
            for k in dict_landmarks[f"slice_{n_slice}"].keys():
                landmarks_x.append(dict_landmarks[f"slice_{n_slice}"][k][0])
                landmarks_y.append(dict_landmarks[f"slice_{n_slice}"][k][1])
        
            self.master.subplot.scatter(landmarks_x,landmarks_y, c="red", marker = "x")
            self.master.canvas.draw()
    
    
    
        
        
        