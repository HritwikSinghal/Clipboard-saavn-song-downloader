import logging
import os
import random
import traceback

if os.path.isfile('test_bit'):
    os.environ["DEBUG"] = "1"

from src.saavn_downloader import SaavnDownloader

# --------------------------------------------------------------------------------------------------- #
# Dont use _LOGGER = logging.getLogger(__name__), it will not work.
# See https://stackoverflow.com/questions/47608069/python-logging-multiple-modules
_LOGGER = logging.getLogger()
_LOGGER.setLevel(logging.DEBUG)

_FORMATTER = logging.Formatter(
    '%(asctime)s : [%(levelname)s] :  %(name)s : (%(filename)s).%(funcName)s(%(lineno)d) : %(message)s'
)

_FILE_HANDLER = logging.FileHandler('saavn_downloader.log')
_FILE_HANDLER.setLevel(logging.DEBUG)
_FILE_HANDLER.setFormatter(_FORMATTER)

_STREAM_HANDLER = logging.StreamHandler()
_STREAM_HANDLER.setLevel(logging.DEBUG)
_STREAM_HANDLER.setFormatter(_FORMATTER)

_LOGGER.addHandler(_FILE_HANDLER)
_LOGGER.addHandler(_STREAM_HANDLER)

# --------------------------------------------------------------------------------------------------- #

test_bit = os.environ.get('DEBUG', default='0')


def down_from_file(download_dir):
    if os.path.isfile("songs_list.txt"):
        print('Found "songs_list.txt", downloading songs from it first... ')
        with open('songs_list.txt', 'r+') as song_file:
            song_url_list = [str(x).strip() for x in song_file.readlines() if str(x).strip()]
            my_downloader = SaavnDownloader(download_dir)

            for song_url in song_url_list:
                try:
                    my_downloader.url = song_url
                    my_downloader.run()
                except:
                    if test_bit:
                        traceback.print_exc()
                    continue

            print('Song download from file complete, renaming file and moving to clipboard download...')

        os.rename('songs_list.txt', 'songs_list_DONE_' + str(random.randint(1, 100000)) + '.txt')


def start(test=0):
    # https://stackoverflow.com/questions/23255186/download-under-users-profile-directory
    # download_dir = os.path.expandvars('%userprofile%/Downloads/')  # where to put it

    # https://stackoverflow.com/questions/4028904/how-to-get-the-home-directory-in-python

    download_dir = os.path.expanduser("~/Downloads/Music")

    if not os.path.isdir(download_dir):
        os.mkdir(download_dir)
    print("Songs will be Downloaded to: ", download_dir)

    down_from_file(download_dir)

    try:
        while True:
            my_downloader = SaavnDownloader(download_dir)
            my_downloader.run()

    except:
        if test:
            traceback.print_exc()
        print("\nExiting....")


if __name__ == '__main__':
    _LOGGER.info('Logging Started')

    if test_bit == '1':
        _LOGGER.info('DEBUG mode ON')
        start()
    else:
        _LOGGER.info('DEBUG mode OFF')
        print("""\n

                ░██████╗░█████╗░░█████╗░██╗░░░██╗███╗░░██╗  ░██████╗░█████╗░███╗░░██╗░██████╗░
                ██╔════╝██╔══██╗██╔══██╗██║░░░██║████╗░██║  ██╔════╝██╔══██╗████╗░██║██╔════╝░
                ╚█████╗░███████║███████║╚██╗░██╔╝██╔██╗██║  ╚█████╗░██║░░██║██╔██╗██║██║░░██╗░
                ░╚═══██╗██╔══██║██╔══██║░╚████╔╝░██║╚████║  ░╚═══██╗██║░░██║██║╚████║██║░░╚██╗
                ██████╔╝██║░░██║██║░░██║░░╚██╔╝░░██║░╚███║  ██████╔╝╚█████╔╝██║░╚███║╚██████╔╝
                ╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚══╝  ╚═════╝░░╚════╝░╚═╝░░╚══╝░╚═════╝░

                ██████╗░░█████╗░░██╗░░░░░░░██╗███╗░░██╗██╗░░░░░░█████╗░░█████╗░██████╗░███████╗██████╗░
                ██╔══██╗██╔══██╗░██║░░██╗░░██║████╗░██║██║░░░░░██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
                ██║░░██║██║░░██║░╚██╗████╗██╔╝██╔██╗██║██║░░░░░██║░░██║███████║██║░░██║█████╗░░██████╔╝
                ██║░░██║██║░░██║░░████╔═████║░██║╚████║██║░░░░░██║░░██║██╔══██║██║░░██║██╔══╝░░██╔══██╗
                ██████╔╝╚█████╔╝░░╚██╔╝░╚██╔╝░██║░╚███║███████╗╚█████╔╝██║░░██║██████╔╝███████╗██║░░██║
                ╚═════╝░░╚════╝░░░░╚═╝░░░╚═╝░░╚═╝░░╚══╝╚══════╝░╚════╝░╚═╝░░╚═╝╚═════╝░╚══════╝╚═╝░░╚═╝

                － Ｂｙ Ｈｒｉｔｗｉｋ Ｓｉｎｇｈａｌ
        \n""")

        print("""
                This program will Download songs from Jiosaavn based on the links you copy on your clipboard.
                Just run this program and copy links, it will download them in background.
                For more info, visit https://github.com/HritwikSinghal/Clipboard-saavn-song-downloader
        """)

        print("Starting Program....")
        start()

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

        print("""

                ████████╗██╗░░██╗░█████╗░███╗░░██╗██╗░░██╗  ██╗░░░██╗░█████╗░██╗░░░██╗██╗
                ╚══██╔══╝██║░░██║██╔══██╗████╗░██║██║░██╔╝  ╚██╗░██╔╝██╔══██╗██║░░░██║██║
                ░░░██║░░░███████║███████║██╔██╗██║█████═╝░  ░╚████╔╝░██║░░██║██║░░░██║██║
                ░░░██║░░░██╔══██║██╔══██║██║╚████║██╔═██╗░  ░░╚██╔╝░░██║░░██║██║░░░██║╚═╝
                ░░░██║░░░██║░░██║██║░░██║██║░╚███║██║░╚██╗  ░░░██║░░░╚█████╔╝╚██████╔╝██╗
                ░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚═╝  ░░░╚═╝░░░░╚════╝░░╚═════╝░╚═╝
        """)
        _LOGGER.info('Logging End')

# todo: add colored text : https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
# todo: fix artists and add support for Podcasts (shows)
# todo: write tests
# todo: find about MITM attack and see song file in monuyadav for payload
# todo:
# todo:
