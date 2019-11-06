import requests
import shutil
from bs4 import BeautifulSoup
import pandas as pd
import multiprocessing as mp
import os
import tqdm
import numpy as np
from nightmares.utils import mkdirs
# This is the image url.
#image_url = "http://images.ucomics.com/comics/ga/1994/ga940101.gif"

from images_defines import JIKOS_SAVE_FOLDER, GDOT_SAVE_FOLDER, LAST_YEAR_DOWNLOAD, FIRST_YEAR_DOWNLOAD, YEAR_RANGE_DOWNLOAD

#jikos_database = "http://pt.jikos.cz/garfield/"
#garfield_database = "https://d1ejxu6vysztl5.cloudfront.net/comics/garfield/2011/2011-07-13.gif?v=1.1"

def download_image(url, name, folder="."):
    file_path = os.path.join(folder, name)
    with open(file_path, 'wb') as file:
        resp = requests.get(url, stream=True)
        resp.raw.decode_content = True
        shutil.copyfileobj(resp.raw, file)

def get_info(td, mode=0):
    day, month, year = td.text.split("/")
    day = day.rjust(2, "0")
    month = month.rjust(2, "0")
    src = td.find("img")["src"]
    name = src.split("/")[-1]
    return day, month, year, src, name

def get_info_from_url(url):
    year, month, day = url.split("/")[-1].split(".")[0].split("-")
    day = day.rjust(2,"0")
    month = month.rjust(2,"0")
    name = url.split("/")[-1].split("?")[0]
    return day, month, year, url, name

#def start():

def jikos_worker(td, i, save_folder):
    info = get_info(td)
    day, month, year, url, name = info
    new_folder = os.path.join(save_folder, year, month)
    if not name in os.listdir(new_folder):
        download_image(url, name, new_folder)
    return info

def start_jikos(save_folder=JIKOS_SAVE_FOLDER, years=YEAR_RANGE_DOWNLOAD,n_jobs=4):
    for year in years:
        infos = []
        for month in tqdm.tqdm(range(1, 13)):
            image_url = "http://pt.jikos.cz/garfield/{}/{}/".format(year, month)
            resp = requests.get(image_url, stream=True)
            soup = BeautifulSoup(resp.content, "lxml")
            images_td = soup.find_all("td")
            with mp.Pool(processes=n_jobs) as pool:
                n= len(images_td)
                save_folders = [save_folder]*n
                mkdirs(save_folder, [year, month])
                args = zip(images_td, range(n), save_folders)
                info = pool.starmap(jikos_worker, args)
                infos.extend(info)
            del(resp)
        infos = pd.DataFrame(infos, columns=["day","month","year","src","name"])
        infos.to_csv(os.path.join(save_folder, str(year), "images.csv"), index=False)

def gdotcom_worker(save_folder, day, month, year):
    year = str(year)
    day = str(day).rjust(2,"0")
    month = str(month).rjust(2,"0")
    image_url = "https://d1ejxu6vysztl5.cloudfront.net/comics/garfield/{}/{}-{}-{}.gif?v=1.1".format(year, year, month, day)
    resp = requests.get(image_url, stream=True)
    soup = BeautifulSoup(resp.content, "lxml")
    if not soup.find("error"):
        info = get_info_from_url(image_url)
        day, month, year, url, name = info
        new_folder = os.path.join(save_folder, year, month)
        download_image(image_url, name, new_folder)
    else:
        info = None
    return info

def start_gdotcom(save_folder=GDOT_SAVE_FOLDER, years=YEAR_RANGE_DOWNLOAD, n_jobs=3):
    for year in years:
        infos = []
        for month in tqdm.tqdm(range(1, 12+1)):
            print(month)
            save_folders = [save_folder]*32
            years_ = [year]*32
            months = [month]*32
            days = range(32)
            mkdirs(save_folder, [year, month])
            args = zip(save_folders, days, months, years_)
            with mp.Pool(processes=n_jobs) as pool:
                info = pool.starmap(gdotcom_worker, args)
                info = [i for i in info if not i is None]
            infos.extend(info)
        infos = pd.DataFrame(infos, columns=["day","month","year","src","name"])
        infos.to_csv(os.path.join(save_folder, str(year), "images.csv"), index=False)

if __name__ == "__main__":
    start_gdotcom()
