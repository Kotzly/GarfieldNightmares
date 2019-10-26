import requests
import shutil
from bs4 import BeautifulSoup
import pandas as pd
import os
import tqdm
# This is the image url.
#image_url = "http://images.ucomics.com/comics/ga/1994/ga940101.gif"
first_year = 1978
last_year = 2019
images_folder = "C:/Users/Paulo/Desktop/Python shit/GarfieldNightmares/images"

#jikos_database = "http://pt.jikos.cz/garfield/"
#garfield_database = "https://d1ejxu6vysztl5.cloudfront.net/comics/garfield/2011/2011-07-13.gif?v=1.1"

def mkdirs(folder, new_folders):
    if isinstance(new_folders, str):
        new_folders = new_folders.split("/")
    for new_folder in new_folders:
        folder = os.path.join(folder, new_folder)
        try:
            os.mkdir(folder)
        except:
            pass

def download_image(url, name, folder="."):
    file_path = os.path.join(folder, name)
    with open(file_path, 'wb') as file:
        resp = requests.get(url, stream=True)
        resp.raw.decode_content = True
        shutil.copyfileobj(resp.raw, file)

def get_info(td, mode=0):
    day, month, year = td.text.split("/")
    day = day.rjust(2,"0")
    month = month.rjust(2,"0")
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
def start_jikos(save_folder=images_folder):
    infos = []
    for year in range(first_year, last_year+1):
        for month in tqdm.tqdm(range(1, 13)):
            image_url = "http://pt.jikos.cz/garfield/{}/{}/".format(year, month)
            resp = requests.get(image_url, stream=True)
            soup = BeautifulSoup(resp.content, "lxml")
            images_td = soup.find_all("td")
            for i, image_td in enumerate(images_td):
                info = get_info(image_td)
                day, month, year, url, name = info
                infos.append(info)
                mkdirs(save_folder, [year, month])
                new_folder = os.path.join(save_folder, year, month)
                if not name in os.listdir(new_folder):
                    download_image(url, name, new_folder)
            del(resp)
    infos = pd.DataFrame(infos, columns=["day","month","year","src","name"])
    infos.to_csv(os.path.join(save_folder, "images.csv"))


def start_gdotcom(save_folder=images_folder):
    infos = []
    for year in range(first_year, last_year+1):
        for month in range(1, 13):
            for day in range(32):
                year = str(year)
                day = str(day).rjust(2,"0")
                month = str(month).rjust(2,"0")
                image_url = "https://d1ejxu6vysztl5.cloudfront.net/comics/garfield/{}/{}-{}-{}.gif?v=1.1".format(year, year, month, day)
                resp = requests.get(image_url, stream=True)
                soup = BeautifulSoup(resp.content, "lxml")
                if not soup.find("error"):
                    info = get_info_from_url(image_url)
                    infos.append(info)
                    day, month, year, url, name = info
                    mkdirs(save_folder, [year, month])
                    new_folder = os.path.join(save_folder, year, month)
                    download_image(image_url, name, new_folder)
    infos = pd.DataFrame(infos, columns=["day","month","year","src","name"])
    infos.to_csv(os.path.join(save_folder, "images.csv"))
