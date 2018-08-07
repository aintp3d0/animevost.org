#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# __author__ = 'kira@-築城院 真鍳'

from os import mkdir, chdir #----------#
from json import loads #---------------#
from os.path import exists #-----------#
from urllib.error import HTTPError #---#
from urllib.request import urlretrieve #


"""
# http://toly.github.io/blog/2014/02/13/parallelism-in-one-line/
NAH MULTIPROCESSING HERE, IF YA WANT IT TRY:

from os import rename
from wget import download
from multiprocessing import Pool


deque = []

def _download(serie):
    # download downloads link and returns name of downloaded file
    # we need to store this name to rename like "1 серия" ...
    deque.append(download(serie))


def multi_down():
    pool = Pool()
    pool.map(_download, _sd or _hd)     # _sd or _hd in line: 84, 89
    pool.close()
    pool.join()


# dname = "1 серия", deque = ["2147397125.mp4", ...]
for dname, each in zip([each for each in series], deque):
    rename(each, f"{dname}.mp4")


IF YOU IN WINDOWS AND HAVEN'T CURL:

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen


soup = bs(urlopen(url), 'lxml')
for script in soup.find_all('script'):
    if "var data = {" in script.text:
        HERE START USING MY SCRIPT IN LINE 63
"""


# SD FILE -> 480p, HD FILE -> 720p
URL_TO_DOWNLOAD = "http://file.aniland.org/"


with open('series.txt', 'r') as series:
    #     var data = {"1 серия":"1714835899","5 серия":"1707474810","12 серия":"214793857"};
    # READ AND MAKE DICT LIKE STRING
    seri = series.read()
    seri = seri.strip()
    seri = seri.replace(';', '')
    seri = seri.replace('var data = ', '')
    seri = seri.replace(',}', '}')
    # JSON ERROR IF SERI NAH LOOKS LIKE DICT
    seri = loads(seri)

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

    for each in seri:
        try:
            _hd = f"{URL_TO_DOWNLOAD}/720/{seri[each]}.mp4"
            urlretrieve(_hd, f"{each}.mp4")
            print(f"[+] ({each}) <<< {_hd}")
        except HTTPError:
            # IF NOT _SD -> ERROR: NOT FOUND
            _sd = f"{URL_TO_DOWNLOAD}{seri[each]}.mp4"
            urlretrieve(_sd, f"{each}.mp4")
            print(f"[+] ({each}) <<< {_sd}")
