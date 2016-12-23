# TermProject
Readme 

This project is designed to teach braille to those who are sighted. The goal is to provide perspective
as to how those who are visually impaired interact with the world. In order to run the program open and run the frontend.py file. The extra folder contains files that were used as drafts/experimentation to enable the creation of this project.
It should be noted that this program uses python2 rather than python3 since some functions in opencv2 are not 
compatible with python3. Pillow was also briefly usedin order to import one picture into the program. 

In order to install OpenCV2 here are the instructions taken from an email by Professor David Kosbie's:


Windows Installation Instructions:

 

Make sure you have python 2 installed (get 64bit version if possible):

https://www.python.org/downloads/

Make sure to check the box to install pip, as well as the one to add python.exe to your path

Go to this wonderful site: http://www.lfd.uci.edu/~gohlke/pythonlibs/

Download the numpy and opencv versions corresponding to your version of python

Make sure youíre downloading opencv 2 and not opencv 3

For 32 bit python:

numpy-1.10.1+mkl-cp27-none-win32.whl

opencv_python-2.4.12-cp27-none-win32.whl

For 64 bit python:

numpy-1.10.1+mkl-cp27-none-win_amd64.whl

opencv_python-2.4.12-cp27-none-win_amd64.whl

Now that you have both numpy and opencv downloaded, youíll need to install them using pip. To do so, open up a shell (cmd / powershell / git bash / etc should all work).

Navigate to the directory that you downloaded the files to by using the following command (replace the path with your own):

cd C:\Users\Vasu\Downloads

Install numpy with the following command (change filename if 32 bit):

pip install numpy-1.10.1+mkl-cp27-none-win_amd64.whl

Install opencv with the following command (change filename if 32 bit)

pip install opencv_python-2.4.12-cp27-none-win_amd64.whl

If youíre able to run the following two command successfully in python, youíre good to go:

import numpy as np

import cv2

 

Mac Installation Instructions:

Make sure you have Python 2 installed

If you donít, type the following into the command line: brew install python

Install pip if you donít already have it by following the instructions listed here: https://pip.pypa.io/en/latest/installing/#install-or-upgrade-pip

Install numpy by opening a command line and running pip install numpy

Install opencv by typing the following two lines into the command line:

brew tap homebrew/science

brew install opencv

If youíre able to run the following two command successfully in python, youíre good to go:

import numpy as np

import cv2
