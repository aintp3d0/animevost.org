#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# __author__ = 'kira@-築城院 真鍳'

from os import mkdir, chdir, rename #-----------#
from sys import argv #--------------------------#
from bs4 import BeautifulSoup as bs #-----------#
from wget import download #---------------------#
from json import loads #------------------------#
from glob import glob #-------------------------#
from os.path import exists #--------------------#
from requests import get #----------------------#
from multiprocessing import Pool #--------------#


MP4 = ".mp4"
AP4 = "*{}".format(MP4)
TAR = "var data = {" 
# SD FILE -> 480p, HD FILE -> 720p
URL_TO_DOWNLOAD = "http://file.aniland.org/"


# IT looks like we don't need to sort ID,
# download file will be like ID.mp4,
# and we already have sorted ID (var data)
def _download(item):
    try:
        _hd = "{}/720/{}{}".format(URL_TO_DOWNLOAD, item, MP4)
        download(_hd)
    except Exception:
        # IF NOT _SD -> ERROR: NOT FOUND
        _sd = "{}{}{}".format(URL_TO_DOWNLOAD, item, MP4)
        download(_sd)


def multi_down(series):
    pool = Pool()
    pool.map(_download, series)
    pool.close()
    pool.join()


if len(argv) == 2:
    for script in bs(get(argv[1]).text, 'lxml').find_all('script'):
        #     var data = {"1 серия":"1714835899", ... ,"12 серия":"214793857"};
        if TAR in script.text:
            # READ AND MAKE DICT LIKE STRING
            seri = script.text.split('\n')
            for i in seri:
                if TAR in i:
                    seri = i
            seri = " ".join(seri.split()[3:])
            seri = seri.replace(';', '')
            seri = seri.replace(',}', '}')
            # JSON ERROR IF SERI NAH LOOKS LIKE DICT
            seri = loads(seri)

            # NAME OF SERIES
            nseri = {v:k for k, v in seri.items()}

            # CREATE FOLDER TO KEEP DOWNLOADED SERIES
            MOVE_TO_FOLDER = input('NAME: ')
            # COPY & PASTE NAME FROM BROWSER
            MOVE_TO_FOLDER = MOVE_TO_FOLDER.replace(' ', '_')   # A "B" -> A_"B"
            MOVE_TO_FOLDER = MOVE_TO_FOLDER.replace('"', '')    # A_"B" -> A_B

            # NEW FOLDER FOR NEW ANIME
            if MOVE_TO_FOLDER:
                if not exists(MOVE_TO_FOLDER):
                    mkdir(MOVE_TO_FOLDER)
                chdir(MOVE_TO_FOLDER)

            # RUN MULTIPROCESSING WITH GENERATOR OF IDS
            multi_down(
                (seri[item] for item in seri if item not in\
                (ex.split(MP4)[0] for ex in glob(AP4))
                )
            )

            # down_seri = "2147397125.mp4", glog = ["2147397125.mp4", ...]
            for down_seri in glob(AP4):
                # nseri = {"2147397125.mp4": 1 серия, ... }
                rename(down_seri, "{}{}".format(nseri[down_seri.split('.')[0]], MP4))

            # HOPE ALL SERIES DOWNLOADED | STOP THE FOR LOOP
            break

else:
    print('python3 animevost.py http?://animevost.org/???')
