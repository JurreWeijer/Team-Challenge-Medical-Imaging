# Team-Challenge-Medical-Imaging

Hello and welcome to the program we created for the Team Challenge, a project for the UU & TU/e MiX master. For this project we created a program that uses CT scans from scoliotic and non-scoliotic patients to calculate some trunk deformity parameters from [Harris 2014](https://link.springer.com/article/10.1007/s00586-014-3580-8). This is done manual, semi automatic and fully automatic.

**This tool is under development, metrics are probably not accurate under all circumstances**

### Setup on your Windows machine
1. Install [Anaconda](https://www.anaconda.com/) for easy environment setup
2. Install [Github Desktop](https://desktop.github.com/) for easy push and pull commits
3. Clone the Github repository by opening Github Desktop and going to file --> Clone repository. Make sure you select the right folder to place the repository in the bottom of the window.
4. Prepare your Python environment in Anaconda by installing all relevant libraries
   1. Open an Anaconda Prompt by searching for Anaconda Prompt in your Windows search bar
   2. Create an environment by typing ``` conda create -n TeamChallenge python=3.8```
   3. Open your environment by typing ```conda activate TeamChallenge```
   4. Install all your dependencies by calling ```conda install Library_Name``` or ```pip install Library_Name```
5. Download the data and place them in a data folder somewhere on your PC 
6. Open your favorite IDE and make sure you have the correct Python Interpreter selected. This is often found in the settings of your IDE 
7. You are now able to succesfully run the main.py file which will open the GUI

### Required dependencies:

Add libraries here if you need to use them!

- Numpy
- Matplotlib
- Pandas
- SimpleITK
- opencv
- Tkinter 
- CustomTkinter 
- Scipy 
- Scikit-image

When the program starts a GUI pops up. The first thing the user is supposed to do, is open an image, which can be done with the Open Image button in the centre of the Scoliosis Chest Deformity window. Then on the left side the axial view pops up and on the right side the coronal view pops up. It is possible to go to a different slice in each of the views. 

There are a couple of things the user can do. 
- Segment the image 
- Calculate parameters from manual input 
- Calculate parameters from landmark extension (semi automatic) 
- Calculate parameters automatically 

### Segment the image 
The user can segment the image (with the Segment image button). After applying image segmentation, the path of where the image is saved is given. The segmentation can be viewed by using the Transverse segmentation button (for axial view) and Coronal segmentation button (for coronal view). 

### Calculate parameters from manual input 
The user is asked to put in the landmarks for the selected parameter. The parameter value is directly added to the table below. 

### Calculate parameters from landmark extension (semi automatic) 
First set a startpoint and an endpoint. Then press the Landmark extension button, the user is asked to put in the landmarks for a fraction of the slices. After the extension is done the user can go through the slices and view the landmarks for the previous selected parameter. If the user wants to calculate the value of the parameter, the Compute slice parameters button can be used. The value will then be shown in the table below.

### Calculate parameters automatically
First set a startpoint and an endpoint. Then the user can press the Automatic calculation button, the landmarkpositions are now automatically determined. The user can go through the slices and save the parameter values by pressing Compute slice parameters. 

For some of the parameters, the value is more significant when it is calculated with landmarks closer to the rib. To get those values, the Compute rib parameters can be used. This is available for Angle trunk rotation and Assymetry index. The Compute rib parameters can only be used after calculating the parameters from landmark extension or automatically. 

In the table down below, the calculated values pop up. These can be saved with the button on the bottom.  

