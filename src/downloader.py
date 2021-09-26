import os
import re

import requests


class Downloader:
    def __init__(self, download_dir, test_bit=0):
        self._download_dir: str = download_dir
        self.keys: dict = {}
        self.test_bit = test_bit

        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'referer': 'https://www.jiosaavn.com/song/tere-naal/KD8zfAZpZFo',
            'origin': 'https://www.jiosaavn.com'
        }

    # ----------------------------------- #
    def get_url(self):
        return self._url

    def set_url(self, encrypted_url: str):
        self._url = encrypted_url

    def get_file_name(self):
        return self._file_name

    def set_file_name(self, title: str):
        self._file_name = title

    def get_download_dir(self):
        return self._download_dir

    def set_download_dir(self, download_dir: str):
        self._download_dir = download_dir

    # ----------------------------------- #

    def download(self, url: str, file_name: str, file_extension: str):
        _filename = file_name + '.' + file_extension
        _filename = re.sub(r'[?*<>|/\\":]', '', _filename)

        file_path = os.path.join(self._download_dir, _filename)

        print(f"Downloading '{file_name}'.....")
        raw_data = requests.get(url, stream=True, headers=self.headers)
        with open(file_path, "wb") as raw_file:
            for chunk in raw_data.iter_content(chunk_size=2048):
                if chunk:
                    raw_file.write(chunk)

        print("Download Successful")
        return file_path
