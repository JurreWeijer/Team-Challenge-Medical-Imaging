# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

datapath = "./Data/"

def OpenImage(path, name):
    img = Image.open(path + name)
    return img

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    img = OpenImage(datapath + 'Nonscoliotic/', 'Control1a.tif')
    print(img.size)
    print(img.n_frames)
    img.show()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
