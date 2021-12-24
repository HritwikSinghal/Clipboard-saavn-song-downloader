import logging
import os
import subprocess
import time
from pathlib import Path

import requests
from packaging import version

from src.tools.colors import bcolors

_LOGGER = logging.getLogger(__name__)

test_bit = int(os.environ.get('DEBUG', default='0'))


class Updater:
    """
    check the url
    it will redirect to latest tag, if its newer than current tag, then update.
    to check the version, read the version file in root dir
    """

    def __init__(self):
        self.update_command = "curl -sSL https://raw.githubusercontent.com/HritwikSinghal/Clipboard-saavn-song-downloader/master/install_linux.sh | bash"
        self.github_latest_tag_url = "https://github.com/HritwikSinghal/Clipboard-saavn-song-downloader/releases/latest"
        self.latest_tag_url = "https://raw.githubusercontent.com/HritwikSinghal/Clipboard-saavn-song-downloader/master/version"
        self.curr_tag = 0.0
        self.latest_tag = 0.0

    def __set_curr_tag(self):
        with open(Path.home() / 'Clipboard-saavn-song-downloader' / 'version', 'r') as file:
            curr_tag = file.readlines()[0].strip()
        self.curr_tag = version.parse(curr_tag)

    def __get_latest_tag(self):
        # this uses the file "version" to check latest tag.
        response = requests.get(self.latest_tag_url, allow_redirects=True)
        latest = str(response.text).strip()
        self.latest_tag = version.parse(latest)

    def __get_latest_tag_github(self):
        # This uses the github url to check latest tag
        response = requests.get(self.github_latest_tag_url, allow_redirects=True)
        latest = str(response.url).strip().split('/')[-1]
        self.latest_tag = version.parse(latest)

    def __update(self):
        subprocess.run(self.update_command, shell=True)

    def update(self):

        if test_bit:
            print(f"Current version is {self.curr_tag}, github version is {self.latest_tag}")
            time.sleep(0.5)

        else:
            try:
                self.__set_curr_tag()
                # self.__get_latest_tag_github()
                self.__get_latest_tag()

                if self.curr_tag < self.latest_tag:
                    _LOGGER.info(f"Found new version {self.latest_tag}, updating..")
                    print(
                        f"{bcolors.HEADER}Current version is {self.curr_tag}, Found new version {self.latest_tag}, updating..{bcolors.ENDC}")
                    self.__update()
                else:
                    _LOGGER.info("The current version is up to date")
                    print(f"{bcolors.OKGREEN}The current version {self.curr_tag} is up to date.{bcolors.ENDC}")
                    time.sleep(0.5)

            except Exception as e:
                _LOGGER.error(e)
                print("There was some error in checking for updates. See log file.")
