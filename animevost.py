#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# __author__ = 'kira@-築城院 真鍳'

from requests import get
import logging #-------------------------------------------------#
from os import mkdir, chdir, rename, remove, getcwd, environ #---#
from sys import argv, platform #---------------------------------#
from bs4 import BeautifulSoup as bs #----------------------------#
from glob import glob #------------------------------------------#
from json import loads #-----------------------------------------#
from time import sleep #-----------------------------------------#
from wget import download #--------------------------------------#
from shutil import move, rmtree #--------------------------------#
from os.path import exists, join #-------------------------------#
from selenium import webdriver #---------------------------------#
from multiprocessing import Pool #-------------------------------#
from selenium.webdriver.support import expected_conditions as EC #
from selenium.common.exceptions import InvalidArgumentException ##
from selenium.webdriver.support.ui import WebDriverWait #--------#


"""
I've clicked download buttons before using selenium module
After downloading all i wanted was rename downloaded series,
    it was easy to get data with *curl* (linux thing)
    >>> curl url | grep -i "var data = {" > series.txt
    ### Code in deadtest/deadscr.sh function *_get_data*

If any problems with Selenium (or just download series like me)\
    use func self.get_data to rename series_id to series_name
"""

verbs = True if '-v' in argv else False

logging.basicConfig(
    format='[%(asctime)s] --%(levelname)s-- %(message)s',
    level=logging.INFO,
    datefmt="%I:%M:%S"
)

def desc(doc):
    def verbose(func):
        def inner(*args, **kwargs):
            if verbs:
                fname = func.__name__
                space = ' ' * (20 - len(fname))
                logging.info(f"FUNC @{fname}{space}:{doc}")
            return func(*args, **kwargs)
        return inner
    return verbose


class Animevost:
    """
    argv[1] -> http://animevost.org/???:

        series_button          urls_to_download on each series_button
        +-+-+-+---+---+-+      +---+---+
        |1|2|3|...|n-1|n|      |420|720|
        +-+-+-+---+---+-+      +---+---+

    Only click to series_button can open urls_to_download (magic):
        + open url with webdriver
        + click all buttons and get urls (480, 720)
        + try download urls with 720 (HD), E: try 480, E: pass
        + rename downloaded series:
            from:   1714835899.mp4
            to:     1 серия
    """

    def __init__(self):
        self.MP4 = ".mp4"
        self.AP4 = "*{}".format(self.MP4)
        self.TAR = "var data = {"
        self.dir = getcwd()
        self.delay = 10
        self.base_path = "html/body/div/div/div/div/div/div/span/div/div/div/*"
        self.iframe_path = "html/body/div/div/div/div/div/div/span/div/div/iframe"
        self.first_run()
        self.get_folder_name()
        self.run_driver()

    @desc('Move geckodriver* to executable path if exists')
    def first_run(self):
        """Remove nah needed driver

        About downloaded drivers:
            *geckodriver*       for linux64
            *geckodriver.exe*   for win64

        kk i'm running win32 in 64x machine
        """

        def windows():
            for each in env.split(';'):
                if 'python3' in each.lower():
                    return each

        d = 'drivers'

        if exists(d):
            gecko = glob(f'{d}/*')
            env = environ['PATH']

            if gecko and len(gecko) == 2:
                if 'win' in platform:
                    # sorting thing ['geckodriver', 'geckodriver.exe']
                    move(join(self.dir, gecko[1]), windows())
                else:
                    move(join(self.dir, gecko[0]), env.split(':')[0])

            rmtree(d)

    @desc(f'FORpage {argv[1][20:]}')
    def run_driver(self):
        """
        Ubuntu and Windows wants *geckodriver* in executable path
        Kali finding *geckodriver* without executable path
        """
        try:
            self.driver = webdriver.Firefox()
            self.driver.get(argv[1])
        except InvalidArgumentException as e:
            print('Error', e)
            self.driver.close()
            exit(1)

    @desc('First run for downloading HD, second for SD format')
    def get_multiprocessing(self, hd_or_sd):
        pool = Pool()
        pool.map(download, hd_or_sd)
        pool.close()
        pool.join()

    @desc('Creating new directory and changing dir to it')
    def get_folder_name(self):
        MOVE_TO_FOLDER = input('NAME: ')
        MOVE_TO_FOLDER = MOVE_TO_FOLDER.replace(' ', '_')   # A "B" -> A_"B"
        MOVE_TO_FOLDER = MOVE_TO_FOLDER.replace('"', '')    # A_"B" -> A_B
        if MOVE_TO_FOLDER:
            if not exists(MOVE_TO_FOLDER):
                mkdir(MOVE_TO_FOLDER)
            chdir(MOVE_TO_FOLDER)
        else:
            print('Please type folder name, it is important for *renaming series*')
            exit(1)

    @desc('Removing logfile that creating geckodriver')
    def remove_log(self):
        """Remove log after closing driver

        ErrorType in Windows: PermissionError: bla bla because it is being used by another process
        """
        elog = 'geckodriver.log'
        if exists(elog):
            try:
                remove(elog)
            except Exception as e:
                print('\nError', e)

    @desc('Parsing webpage for getting HD and SD')
    def get_series_url(self):
        """
        Get list of series_url (get buttons)
        Get url and keep in list
        # stackoverflow.com/questions
        # /51175323/switching-back-to-parent-frame-after-its-no-longer-in-dom-in-selenium
        # /26566799/how-to-wait-until-the-page-is-loaded-with-selenium-for-python
        # /47790010/how-to-use-expected-conditions-to-check-for-an-element-in-python-selenium
        """
        sd = []
        hd = []
        series = self.driver.find_elements_by_xpath(self.base_path)

        for idx in range(len(series)):
            try:
                # click seri button
                series[idx].click()
                # without *sleep* will be error like...
                # E:  Message: Element not found in the cache \
                #   - perhaps the page has changed since it was looked up
                # num = 2, 1 for good internet and 1 for javascript to changing url
                # dublicating urls bcz of small time for javascript
                sleep(1)

                # wait iframe
                WebDriverWait(self.driver, self.delay).until(
                    EC.frame_to_be_available_and_switch_to_it(
                        self.driver.find_element_by_xpath(self.iframe_path)
                    )
                )
                # wait urls
                WebDriverWait(self.driver, self.delay).until(
                    EC.visibility_of(
                        self.driver.find_element_by_xpath("html/body/div/a")
                    )
                )

                seri = self.driver.find_elements_by_xpath("html/body/div/a")
                sd.append(seri[0].get_attribute('href'))
                hd.append(seri[1].get_attribute('href'))

                # remove iframe
                self.driver.switch_to.default_content()
            except Exception as e:
                print('E: ', e)
                self.driver.close()

        self.driver.close()
        # run multi download, if not hd then sd
        try:
            self.get_multiprocessing(hd)
        except Exception:
            self.get_multiprocessing(sd)
        finally:
            # print verbose in new line
            print()

    @desc('Parsing webpage for getting data of series_id')
    def get_data(self, source):
        """
        js_data to json_data
        """
        for script in source.find_all('script'):
            #     var data = {"1 серия":"1714835899", ... ,"12 серия":"214793857"};
            if self.TAR in script.text:
                seri = script.text.split('\n')
                for i in seri:
                    if self.TAR in i:
                        seri = i
                seri = " ".join(seri.split()[3:])
                seri = seri.replace(';', '')
                seri = seri.replace(',}', '}')
                seri = loads(seri)
                nseri = {v:k for k, v in seri.items()}
                return nseri

    @desc('Entry pointer, make series_id readable')
    def get_page_source(self):
        """
        Get page_(site)_source and unblock series_url by clicking series_button
        Before debug script be sure that your browser not showing you 1 url in each series_button
        """
        page_ready = False
        while not page_ready:
            try:
                r = self.driver.page_source
            except Exception as e:
                print('Waiting page source:', e)
                sleep(1)
            else:
                page_ready = True
                self.get_series_url()
                self.remove_log()
                # nseri = {"2147397125.mp4": 1 серия, ... }
                nseri = self.get_data(bs(r, 'lxml'))
                # down_seri = "2147397125.mp4", glog = ["2147397125.mp4", ...]
                for down_seri in glob(self.AP4):
                    # don't rename dublicates
                    down_id = down_seri.split('.')[0]
                    if down_id in nseri.keys():
                        rename(down_seri, f"{nseri[down_id].replace(' ', '_')}{self.MP4}")


if __name__ == "__main__":
    if len(argv) >= 2:
        anime = Animevost()
        anime.get_page_source()
    else:
        print('python3 animevost.py http://animevost.org/???')
