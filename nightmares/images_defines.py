# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 18:28:08 2019

@author: Paulo
"""
import os
from os.path import join

if os.path.isdir(ROOT_FOLDER):
    print("Loading PC files...")
    ROOT_FOLDER = "C:/Users/Paulo/Desktop/Python shit/GarfieldNightmares/"
else:
    print("Loading Drive files...")
    ROOT_FOLDER = "/content/drive/My Drive/GarfieldNightmares"

JIKOS_SAVE_FOLDER = join(ROOT_FOLDER, "images1")
GDOT_SAVE_FOLDER = join(ROOT_FOLDER, "images2")
GDOT_PNG_FOLDER = join(ROOT_FOLDER, "png")
IMAGE_INFO_CSV = join(ROOT_FOLDER, "images2/images.csv")


FIRST_YEAR_DOWNLOAD = 1978
LAST_YEAR_DOWNLOAD = 2019
YEAR_RANGE_DOWNLOAD = range(FIRST_YEAR_DOWNLOAD, LAST_YEAR_DOWNLOAD+1)
