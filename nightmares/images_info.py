# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 18:27:01 2019

@author: Paulo
"""

import pandas as pd
import numpy as np
from PIL import Image
from nightmares.images_defines import GDOT_SAVE_FOLDER
from os.path import join, isdir
from os import listdir as ls

def create_info_cols(df):
    """ Create width and height columns in a dataframe.
        Arguments:
            df: Dataframe to put the columns.
        Returns:
            df: Modified dataframe.
    """
    df["width"] = np.nan
    df["height"] = np.nan
    return df

def put_image_info(df, name, width=np.nan, height=np.nan):
    """ Put width and height information into a dataframe.
        Arguments:
            df: Dataframe to put width and height information.
            name: Name of the image to put the information.
            width: Width of the image.
            height: Height of the image.
        Returns:
            df: Modified dataframe.
    """
    df.loc[df.name == name, "width"] = width
    df.loc[df.name == name, "height"] = height
    return df

def join_per_year(root_folder=GDOT_SAVE_FOLDER):
    """ Uses all years images informations to make a info file with all csv.
        The function will read the images.csv files, join then and put the new
        file in the root_folder.s
        Arguments:
            root_folder: Folder with the year/month folders.
    """
    infos = []
    for year_folder in ls(root_folder):
        print(year_folder)
        year_folder = join(root_folder, year_folder)
        if not isdir(year_folder): continue
        image_info_file = join(year_folder, "images.csv")
        try:
            info = pd.read_csv(image_info_file)
            info = create_info_cols(info)
        except:
            print("image.csv from {} does not exists!".format(year_folder))
            continue
        for month_folder in ls(year_folder):
            month_folder = join(year_folder, month_folder)
            if not isdir(month_folder): continue
            images = ls(month_folder)
            for image in images:
                image_filepath = join(month_folder, image)
                with Image.open(image_filepath) as img:
                    width, height = img.size
                    info = put_image_info(info, image, width=width, height=height)
        info.to_csv(image_info_file, index=False)
        infos.append(info)
    infos = pd.concat(infos, axis=0)
    infos.to_csv(join(root_folder, "images.csv"), index=False)
