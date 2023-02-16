# Team-Challenge-Medical-Imaging

This project is for the UU & TU/e MiX master project Team Challenge.

The goal is to create a program that imports CT scans from scoliotic and non-scoliotic patients and calculates some kind of metric for the trunk deformity.

## Table of Contents
- [Getting started](#getting-started)
- [Good to Know](#good-to-know)
- [Making code changes](#making-code-changes)

## Getting started

### On your Windows machine
1. Install [Anaconda](https://www.anaconda.com/) for easy environment setup
2. Install [Github Desktop](https://desktop.github.com/) for easy push and pull commits
3. Clone the Github repository by opening Github Desktop and going to file --> Clone repository. Make sure you select the right folder to place the repository in the bottom of the window.
4. Prepare your Python environment in Anaconda by installing all relevant libraries
   1. Open an Anaconda Prompt by searching for Anaconda Prompt in your Windows search bar
   2. Create an environment by typing ``` conda create -n TeamChallenge python=3.6```
   3. Open your environment by typing ```conda activate TeamChallenge```
   4. Install all your dependencies by calling ```conda install Library_Name``` or ```pip install Library_Name```
5. Download the data from the Research drive and place them in a data folder somewhere on your PC 
6. Open your favorite IDE and make sure you have the correct Python Interpreter selected. This is often found in the settings of your IDE 
7. Open the Team-Challenge-Medical-Imaging project and start working!
8. Upload your changes to your own branch using GitHub desktop

### Required dependencies:

Add libraries here if you need to use them!

- Numpy
- Matplotlib
- Pandas
- SimpleITK
- Tkinter 
- CustomTkinter 

## Good to Know

### Find Answers to Questions
- [Stack Overflow](https://stackoverflow.com/questions/tagged/python)
- [Python documentation](https://docs.python.org/3/)
- [GNU make Manual](https://www.gnu.org/software/make/manual/html_node/index.html)
  and [Concise introduction to GNU Make](https://swcarpentry.github.io/make-novice/reference.html)

### Reading List
- [Make a README](https://www.makeareadme.com)
- [Keep a CHANGELOG](https://keepachangelog.com)

#### Git
- [Resources to learn Git](https://try.github.io)
- [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/)
- [Making a Pull Request](https://www.atlassian.com/git/tutorials/making-a-pull-request)
- [Using branches](https://www.atlassian.com/git/tutorials/using-branches)

### Code Quality
- [Clean Code concepts adapted for Python](https://github.com/zedr/clean-code-python)
- [The Hitchhiker’s Guide to Python!](https://docs.python-guide.org)
- [Support for type hints](https://docs.python.org/3/library/typing.html) or
  [PEP 484 -- Type Hints](https://www.python.org/dev/peps/pep-0484/)


### Documentation
- [Google Python Style Guide](http://google.github.io/styleguide/pyguide.html)


## Making code changes

Make sure you have downloaded GitHub Desktop for easy push and pull requests.

1. Select your own branch in the top bar, if you do not have one yet, make sure to create a new one. 
2. Make sure you have pulled all other updates.
3. Create a short but informative Summary in the bottom left
4. Add a longer description about your commit if necessary
5. Commit often to your branch!

This way of working with `git` is known as the [Gitflow
workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
which you should internalize. You should also
* know how to [Keep a changelog](https://keepachangelog.com/en/1.0.0/),
* learn [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/),
* learn how to [Use branches](https://www.atlassian.com/git/tutorials/using-branches),
* learn [Making a Pull Request](https://www.atlassian.com/git/tutorials/making-a-pull-request), and
* adhere to the [PEP8 Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/).

The essence of the Gitflow workflow: There are two permanent branches `master`
and `develop`, where `master` is for releases and `develop` for active
development towards the next release. Features are developed in their own
branches based on `develop` and merged into `develop` when they are finished.
Hot-fixes are developed in their own branches based on `master` and merged into
`master` when they are finished. New releases are made by merging `develop`
into `master`. Each hot-fix and normal release is tagged with a version.


