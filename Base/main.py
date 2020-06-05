import os
import re
from os.path import isdir
from os.path import isfile

import pyperclip
from Base import DownloadSong
from Base import tools


def inputDownloadDir(test=0):
    while True:
        if test == 1:
            songDir = r'C:\Users\hritwik\Pictures\Camera Roll'
        else:
            songDir = input("Enter Download dir:  ")

        if isdir(songDir):
            print("Download dir is: ", songDir)
            return songDir
        else:
            print("No such Dir exist, Please enter Dir again...")


def start(test=0):
    download_dir = inputDownloadDir(test)

    log_file = tools.createLogFile(download_dir)

    while True:
        print('\nWaiting for url from clipboard....')
        url = pyperclip.waitForPaste()
        pyperclip.copy('')

        if str(url).startswith('https://www.jiosaavn.com'):
            print('got url: ', url)
            DownloadSong.start(download_dir, url, log_file, test=test)
