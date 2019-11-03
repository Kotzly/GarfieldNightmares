# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 21:40:27 2019

@author: Paulo
"""

from keras.preprocessing.image import ImageDataGenerator
from keras.utils import Sequence
from images_defines import IMAGE_INFO_CSV, GDOT_SAVE_FOLDER, GDOT_PNG_FOLDER
import pandas as pd
from PIL import Image
import glob
from os.path import join
import numpy as np
import tqdm

def load_images_info(height_bounds = None, width_bounds=None, info_file=IMAGE_INFO_CSV):
    info = pd.read_csv(info_file)
    if height_bounds is not None:
        if height_bounds[0] is not None:
            info = info[info.height>=height_bounds[0]]
        if height_bounds[1] is not None:
            info = info[info.height<=height_bounds[1]]
    if width_bounds is not None:
        if width_bounds[0] is not None:
            info = info[info.width>=width_bounds[0]]
        if width_bounds[1] is not None:
            info = info[info.width<=width_bounds[1]]
    return info

def get_info_from_filename(filename):
    year, month, day = filename.split("/")[-1].split(".")[0].split("-")
    year, month, day = int(year), int(month), int(day)
    return year, month, day

def get_images_paths(ymd, dataset_path=GDOT_SAVE_FOLDER):
    images = glob.glob(join(GDOT_PNG_FOLDER,"**/*.png"), recursive=True)
    images = [image.replace("\\", "/") for image in images]
    images = [image for image in images if get_info_from_filename(image) in ymd]
    return images

def load_images(images, resize=(1200, 400), strip_mode="3"):
    data = []
    for image in tqdm.tqdm(images):
        with Image.open(image) as img:
            if resize:
                img = img.resize(resize)
            content = np.array(img.convert("RGB"))
            data.append(content)
    try:
        data = np.stack(data)
    except:
        pass
    return data

def strip_image(image, mode="3"):
    w, h = image.size
    if mode == "1x3":
        k = 5
        dx = image.width//3
        w, h = image.size
        boxes = [[0, 0, dx+k//2, h],
                 [dx+k, 0, 2*dx-k, h],
                 [2*dx+k, 0, w, h]]
        return [image.crop(box) for box in boxes]
    if mode == "2x3":
#        kx =
        dx = image.width//3

        boxes = [[0, 0, dx, h],
                 [dx+k, 0, 2*dx-k, h],
                 [2*dx+k, 0, w, h],
                 [0, 0, dx, h],
                 [dx+k, 0, 2*dx-k, h],
                 [2*dx+k, 0, w, h]]
    if mode == "2x4x2x3":
        ky = 20
    if mode == "2x4x2x3":
            ky = 20
    if mode == "3x3":
        ky = 30
        kx = 20
        dx = image.width//3
        dy = image.height//3

        boxes [[0,0,2*dx, dy],
               [2*dx+kx, 0, 0, w, ]]
        return [image.crop(box) for box in boxes]

