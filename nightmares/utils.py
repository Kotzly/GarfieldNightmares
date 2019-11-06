# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 21:13:53 2019

@author: Paulo
"""
import os

def mkdirs(folder, new_folders):
    if isinstance(new_folders, str):
        new_folders = new_folders.split("/")
    for new_folder in new_folders:
        if isinstance(new_folder, int):
            new_folder = str(new_folder).rjust(2, "0")
        folder = os.path.join(folder, new_folder)
        try:
            os.mkdir(folder)
        except:
            pass