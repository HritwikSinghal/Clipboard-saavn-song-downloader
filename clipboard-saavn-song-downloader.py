#!/usr/bin/env python3

import argparse
import logging
import os
import pathlib
import subprocess
import traceback
# import click

# noinspection PyUnresolvedReferences
import set_debug
from src.saavn_downloader import SaavnDownloader
from src.updater import Updater
from src.tools.colors import bcolors

# --------------------------------------------------------------------------------------------------- #
# Dont use _LOGGER = logging.getLogger(__name__) in root module, it will not work.
# See https://stackoverflow.com/questions/47608069/python-logging-multiple-modules
_LOGGER = logging.getLogger()
_LOGGER.setLevel(logging.DEBUG)

_FORMATTER = logging.Formatter(
    '[%(levelname)s] : %(asctime)s : %(name)s : (%(filename)s).%(funcName)s(%(lineno)d) : %(message)s'
)

# Print all Log messages to file for debugging
_FILE_HANDLER = logging.FileHandler('saavn_downloader.log')
_FILE_HANDLER.setLevel(logging.DEBUG)
_FILE_HANDLER.setFormatter(_FORMATTER)

# Print only Log messages upper than warning to output since we dont want user to see debug messages
_STREAM_HANDLER = logging.StreamHandler()
_STREAM_HANDLER.setLevel(logging.WARNING)
_STREAM_HANDLER.setFormatter(_FORMATTER)

_LOGGER.addHandler(_FILE_HANDLER)
_LOGGER.addHandler(_STREAM_HANDLER)

# --------------------------------------------------------------------------------------------------- #

test_bit = int(os.environ.get('DEBUG', default=0))


def cmd_parser():
    parser = argparse.ArgumentParser(description='File containing links')
    parser.add_argument('-f', '--file', type=str, help="absolute path of File containing links", required=False)
    parser.add_argument('-v', '--version', help="Program Version", required=False, action="store_true")
    parser.add_argument('-r', '--reset', help="Reset and reinstall the program", required=False, action="store_true")
    args = parser.parse_args()
    return args


def down_from_file(download_dir: str, old_file_name: str) -> None:
    file_name = os.path.expanduser(old_file_name)
    if os.path.isfile(file_name):
        print(f'Found {file_name}, downloading songs from it first....')

        with open(file_name, 'r+') as song_file:
            song_url_list = [str(x).strip() for x in song_file.readlines() if str(x).strip()]
            my_downloader = SaavnDownloader(download_dir)

            for song_url in song_url_list:
                try:
                    my_downloader.url = song_url
                    my_downloader.run()
                except Exception as e:
                    _LOGGER.warning(traceback.format_exc())
                    continue

            print(f'Song download from {old_file_name} complete, renaming file and moving to clipboard download...')
    else:
        _LOGGER.warning(f"No file named '{old_file_name}'.")


def start(args):
    # Update check
    _LOGGER.info('Checking for Updates')
    print('Checking for Updates...')
    Updater().update()

    # Check for download dir
    download_dir = os.path.expanduser("~/Downloads/Music")
    if not os.path.isdir(download_dir):
        os.makedirs(download_dir)
    print("Songs will be Downloaded to: ", download_dir)

    # Check if a file containing song links is provided
    if args.file:
        _LOGGER.info("Found Songs FIle = " + str(args.file))
        try:
            down_from_file(download_dir, args.file)
        except KeyboardInterrupt:
            exit()

    # Proceed with usual
    try:
        while True:
            my_downloader = SaavnDownloader(download_dir)
            my_downloader.run()

    except Exception as e:
        _LOGGER.error(traceback.format_exc())
        exit("\nExiting....")


if __name__ == '__main__':
    _LOGGER.info('Logging Started')

    args = cmd_parser()
    if args.reset:
        print(f"{bcolors.FAIL}Resetting Program...{bcolors.ENDC}")
        reset_command = "curl -sSL https://raw.githubusercontent.com/HritwikSinghal/Clipboard-saavn-song-downloader/master/install_linux.sh | bash"
        subprocess.run(reset_command, shell=True)
        exit("Program Reset Done")

    if args.version:
        # todo:  maybe remove this hardcoded path
        version_path = pathlib.Path.home() / "Clipboard-saavn-song-downloader" / "version"
        with open(version_path) as file:
            print(file.read())
        exit()

    if test_bit == 1:
        _LOGGER.info('DEBUG mode ON')
        start(args=args)
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

        # see https://stackoverflow.com/questions/7073268/remove-traceback-in-python-on-ctrl-c
        try:
            start(args=args)
        except KeyboardInterrupt:
            _LOGGER.debug(f"Keyboard Interrupt, {traceback.format_exc()}")

        print("""
        If there were errors while running this program, Please open an issue on github
        and upload log file named 'saavn-downloader.log' there.
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

# todo: see monuyadav impl of playlist and other downloads

# todo : log is saved in ~ instead of project dir
# todo : fix hardcoded paths and try to find a soln for working with paths in this project
# todo: use loguru
# todo: make this asynchronous
# Todo : fix gnome wayland bug
# todo: add colored text : https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
# todo: fix artists and add support for Podcasts (shows)
# todo: write tests
# todo: find about MITM attack and see song file in monuyadav for payload
