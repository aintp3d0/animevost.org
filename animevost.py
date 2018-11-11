#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# __author__ = 'kira@-築城院 真鍳'

from os import mkdir, chdir, rename, remove, getcwd, environ #---#
from sys import argv #-------------------------------------------#
from bs4 import BeautifulSoup as bs #----------------------------#
from glob import glob #------------------------------------------#
from json import loads #-----------------------------------------#
from time import sleep #-----------------------------------------#
from wget import download #--------------------------------------#
from shutil import move #----------------------------------------#
from os.path import exists, join #-------------------------------#
from selenium import webdriver #---------------------------------#
from multiprocessing import Pool #-------------------------------#
from selenium.webdriver.support import expected_conditions as EC #
from selenium.webdriver.support.ui import WebDriverWait #--------#


"""
I've clicked download buttons before using selenium module
After downloading all i wanted is rename downloaded series,
    it was easy to get data with *curl* (linux thing)
    >>> curl url | grep -i "var data = {" > series.txt
    ### Code in deadtest/deadscr.sh function *_get_data*

If any problems with Selenium (or just download series like me) use line 164 and for loop
"""


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
        self.drn = "geckodriver.exe"
        self.gecko = join(getcwd(), self.drn)
        print('in init')
        self.egeck = exists(self.gecko)
        self.delay = 10
        self.repeat = 0
        print('on getting folder')
        self.get_folder_name()
        print('on running driver')
        self.run_driver()
        print('done with init')
        self.base_path = "html/body/div/div/div/div/div/div/span/div/div/div/*"
        self.iframe_path = "html/body/div/div/div/div/div/div/span/div/div/iframe"

    def run_driver(self):
        """
        Ubuntu and Windows wants *geckodriver* in executable path
        Kali finding *geckodriver* without executable path
        """
        try:
            self.driver = webdriver.Firefox(environ['USERPROFILE'])
        except Exception as e:
            print('in run_driver_exception')
            sleep(1)
            self.move_to_exec_path(e)
        else:
            self.driver.get(argv[1])

    def move_to_exec_path(self, e):
        """
        I've tried to use $PATH variable with linux command:
            system("mv geckodriver $(echo $PATH|cut -d':' -f1)")
        Question was *how i can use this variable if i'm Windows user*:
            https://stackoverflow.com/questions
                /4760215/running-shell-command-from-python-and-capturing-the-output
            but linux commands not working in Windows, after it i remember about *environ*
        """
        env = environ['PATH']
        print('is gecko active:', self.egeck)
        print('in dir:', getcwd())
        sleep(1)
        if self.egeck:
            if ';' not in env:
                move(self.gecko, env.split(':')[0])
            else:
                # needs test, My windows slow as F
                print('in move thing')
                user = environ['USERPROFILE']
                if not exists(join(user, self.drn)):
                    print("Moving *geckodriver* to current User folder")
                    move(self.gecko, user)
                    print("Moved")
        else:
            print("gecko not in dir\n", e)
        # don't play to snake
        print('repeating in', self.repeat)
        if self.repeat == 0:
            self.run_driver()
            self.repeat += 1
        else:
            exit(1)

    def get_multiprocessing(self, hd_or_sd):
        pool = Pool()
        pool.map(download, hd_or_sd)
        pool.close()
        pool.join()

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

    def remove_log(self):
        elog = 'geckodriver.log'
        if exists(elog):
            remove(elog)

    def get_series_url(self):
        """
        Get list of series_url (get buttons)
        Get url and keep in list
        """
        # stackoverflow.com/questions
        # /51175323/switching-back-to-parent-frame-after-its-no-longer-in-dom-in-selenium
        # /26566799/how-to-wait-until-the-page-is-loaded-with-selenium-for-python
        # /47790010/how-to-use-expected-conditions-to-check-for-an-element-in-python-selenium
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
        # catch dublicate urls before downloading
        # before debug script be sure that your browser not showing you 1 url in each series_button
        db = [h.split('.')[-2].split('/')[-1] for h in hd]
        # not tested
        if len(db) != len(set(db)):
            print('Group to download: length > {}, unique length > {}\n'.format(
                    len(db), len(set(db))
                ), db)
            m = input('\nAny dublicates [y/n]: ').lower()
            if m == 'y':
                exit(1)
        # run multi download, if not hd then sd
        try:
            self.get_multiprocessing(hd)
        except Exception:
            self.get_multiprocessing(sd)
        self.remove_log()

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

    def get_page_source(self):
        """
        Get page_(site)_source and unblock series_url by clicking series_button
        """
        page_ready = False
        print('in run')
        while not page_ready:
            print('in while')
            try:
                r = self.driver.page_source
            except Exception:
                print('in get_page_source EXCEPTION')
                sleep(1)
            else:
                page_ready = True
                self.get_series_url()
                nseri = self.get_data(bs(r, 'lxml'))
                # down_seri = "2147397125.mp4", glog = ["2147397125.mp4", ...]
                for down_seri in glob(self.AP4):
                    # nseri = {"2147397125.mp4": 1 серия, ... }
                    rename(down_seri, "{}{}".format(nseri[down_seri.split('.')[0]], self.MP4))


if __name__ == "__main__":
    if len(argv) == 2:
        anime = Animevost()
        anime.get_page_source()
    else:
        print('python3 animevost.py http://animevost.org/???')
