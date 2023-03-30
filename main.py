# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#this does work but is seems prone to errors
%matplotlib qt
import customtkinter
import os
from GUI.GUI_main import Application

datadir = './Data'

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    if os.path.exists(datadir) is False:
        os.mkdir(datadir)

    #make sure that upon startup the working directory is changed so the main folder does not get clogged
    os.chdir(datadir)

    root = customtkinter.CTk()
    app = Application(root)
    root.mainloop()
   
    
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
