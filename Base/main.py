import os
import traceback

import pyperclip

from Base import DownloadSong
from Base import tools


def start(test=0):
    # download_dir = os.path.expandvars('%userprofile%/Downloads/')  # where to put it
    # https://stackoverflow.com/questions/23255186/download-under-users-profile-directory

    download_dir = os.path.expanduser("~/Downloads/Music/Downloaded-Songs")
    if not os.path.isdir(download_dir):
        os.mkdir(download_dir)
    print("Songs will be Downloaded to: ", download_dir)
    # https://stackoverflow.com/questions/4028904/how-to-get-the-home-directory-in-python

    log_file = tools.createLogFile(download_dir)
    try:
        while True:
            print('\nWaiting for url from clipboard....')
            url = pyperclip.waitForPaste()
            pyperclip.copy('')

            if str(url).startswith('https://www.jiosaavn.com'):
                print('got url: ', url)
                DownloadSong.start(download_dir, url, log_file, test=test)
    except:
        if test:
            traceback.print_exc()
        print("Exiting....")
        exit(0)
