import os
import re
from os.path import isdir
from os.path import isfile

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
    print("Download dir =", download_dir, '\n')

    DownloadSong.start(song_name, song_with_path, download_dir, log_file, test=test)
