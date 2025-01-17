import json
import logging
import os
import subprocess
import time
import traceback
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
        self.curr_tag = 0.0
        self.latest_tag = 0.0

    def __set_curr_tag(self):
        # todo: remove this hardcode
        with open(Path.home() / 'Clipboard-saavn-song-downloader' / 'version', 'r') as file:
            curr_tag = json.load(file)['version']
        self.curr_tag = version.parse(curr_tag)

    def __get_latest_version(self):
        # this uses the file "version" to check latest tag.
        # todo: remove this hardcode
        with open(Path.home() / 'Clipboard-saavn-song-downloader' / 'version', 'r') as file:
            latest_version_url = json.load(file)['latest_version_url']

        response = requests.get(latest_version_url, allow_redirects=True)
        latest = json.loads(response.text)['version']
        self.latest_tag = version.parse(latest)

    def __get_latest_tag_github(self):
        # This uses the GitHub url to check latest tag
        # todo: remove this hardcode
        with open(Path.home() / 'Clipboard-saavn-song-downloader' / 'version', 'r') as file:
            github_latest_tag_url = json.load(file)['latest_tag_url']

        response = requests.get(github_latest_tag_url, allow_redirects=True)
        latest = str(response.url).strip().split('/')[-1]
        self.latest_tag = version.parse(latest)

    def __update(self):
        # todo: remove this hardcode
        with open(Path.home() / 'Clipboard-saavn-song-downloader' / 'version', 'r') as file:
            update_command = json.load(file)['update_command']
        subprocess.run(update_command, shell=True)

    def update(self):

        if test_bit:
            print(f"Current version is {self.curr_tag}, github version is {self.latest_tag}")
            time.sleep(0.5)

        else:
            try:
                self.__set_curr_tag()
                # self.__get_latest_tag_github()
                self.__get_latest_version()

                if self.curr_tag < self.latest_tag:
                    _LOGGER.info(f"Found new version {self.latest_tag}, updating..")
                    print(
                        f"{bcolors.HEADER}Current version is {self.curr_tag}, Found new version {self.latest_tag}, updating..{bcolors.ENDC}")
                    time.sleep(0.5)
                    self.__update()
                else:
                    _LOGGER.info("The current version is up to date")
                    print(f"{bcolors.OKGREEN}The current version {self.curr_tag} is up to date.{bcolors.ENDC}")
                    time.sleep(0.5)

            except Exception as e:
                _LOGGER.error(traceback.format_exc())
                print("There was some error in checking for updates. See log file.")
