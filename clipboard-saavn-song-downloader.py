# for bat file "https://datatofish.com/batch-python-script/"


import os
import traceback

import pyperclip

from Base.downloader import SongDownloader
from Base import tools


def start(test=0):
    # https://stackoverflow.com/questions/23255186/download-under-users-profile-directory
    # download_dir = os.path.expandvars('%userprofile%/Downloads/')  # where to put it

    # https://stackoverflow.com/questions/4028904/how-to-get-the-home-directory-in-python
    download_dir = os.path.expanduser("~/Downloads/Music")
    if not os.path.isdir(download_dir):
        os.mkdir(download_dir)
    print("Songs will be Downloaded to: ", download_dir)

    log_file = tools.createLogFile(download_dir)

    # todo: add code to first check if 'songs_list.txt' file is there, if so first download all from it and then proceed
    # todo: also rename to it to 'songs_list_done_randomNumber.txt' to avoid re downloading songs

    if os.path.isfile("songs_list.txt"):
        pass

    try:
        while True:
            my_downloader = SongDownloader(download_dir, log_file, test=test)
            my_downloader.run()

    except:
        if test:
            traceback.print_exc()
        print("Exiting....")
        exit(0)


if __name__ == '__main__':
    test = 1 if os.path.isfile('test_bit.py') else 0

    if test:
        start(test)
    else:
        print("""
            This program will Download songs from Jiosaavn based on the links you copy on your clipboard. 
            Just run this program and copy links, it will download them in background.
            For more info, visit https://github.com/HritwikSinghal/Clipboard-saavn-song-downloader
        """)

        print("Starting Program....")
        start(test)

        print("""
                If there were errors during running this program, please upload log file
                named 'Clipboard-saavn-song-downloader_LOGS.txt' in each dir and open an issue on github
                you can find those log files by using default search in folders or by manually
                finding each.
            """)
        print('''
                Thank you for Using this program....
                By Hritwik
                https://github.com/HritwikSinghal
            ''')

# todo: add log support (use logger)
# todo: use OOP
# todo: update lyrics function in saavnApi
# todo: find about MITM attack and see song file in monuyadav for payload
# todo:
