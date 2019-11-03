# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 21:11:38 2019

@author: Paulo
"""

from PIL import Image
from images_defines import GDOT_SAVE_FOLDER
from utils import mkdirs
from os.path import join, isdir
from os import listdir as ls
import tqdm

OUTPUT_FOLDER = "C:/Users/Paulo/Desktop/Python shit/GarfieldNightmares/outputpng"

def convert_to(source=GDOT_SAVE_FOLDER, dest=OUTPUT_FOLDER, ext="png"):
    """ Convert .gif images from GDOT to .png using PIL.
        Arguments:
            source: path to the folder where the /year/month directories are.
            dest: destination/save path.
            ext: extension to save. See PIL.Image for supported extensions.
    """
    for year_folder in tqdm.tqdm(ls(source)):
        mkdirs(dest,[year_folder])
        year_save_folder = join(dest, year_folder)
        year_folder = join(source, year_folder)
        if not isdir(year_folder): continue
        for month_folder in ls(year_folder):
            mkdirs(year_save_folder,[month_folder])
            month_save_folder = join(year_save_folder, month_folder)
            month_folder = join(year_folder, month_folder)
            if not isdir(month_folder): continue
            images = ls(month_folder)
            for image in images:
                image_filepath = join(month_folder, image)
                with Image.open(image_filepath) as img:
                    image_save_path = join(month_save_folder, image.split(".")[0] + "." + ext)
                    img.save(image_save_path)


if __name__ == "__main__":
    convert_to()