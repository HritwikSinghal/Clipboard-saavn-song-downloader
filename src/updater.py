import logging
import os
import subprocess
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
        self.update_url = "https://github.com/HritwikSinghal/Clipboard-saavn-song-downloader/releases/latest"
        self.curr_tag = 0.0
        self.latest_tag = 0.0

    def __set_curr_tag(self):
        with open(Path.cwd() / 'version', 'r') as file:
            curr_tag = file.readlines()[0].strip()
        self.curr_tag = version.parse('2.1.0')

    def __get_latest_tag(self):
        response = requests.get(self.update_url, allow_redirects=True)
        latest = str(response.url).strip().split('/')[-1]
        self.latest_tag = version.parse(latest)

    def __update(self):
        subprocess.run(self.update_command, shell=True)

    def update(self):
        try:
            self.__set_curr_tag()
            self.__get_latest_tag()

            if self.curr_tag < self.latest_tag:
                _LOGGER.info(f"Found new version {self.latest_tag}, updating..")
                print(f"{bcolors.OKBLUE}Found new version {self.latest_tag}, updating..{bcolors.ENDC}")
                self.__update()
            else:
                _LOGGER.info("The current version is up to date")
                print(f"{bcolors.OKGREEN}The current version is up to date.{bcolors.ENDC}")

        except Exception as e:
            _LOGGER.error(e)
            print("There was some error in checking for updates. See log file.")
