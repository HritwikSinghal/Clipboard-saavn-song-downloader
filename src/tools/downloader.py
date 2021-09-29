import os
import re
import time
import traceback

import requests
import youtube_dl


class FileDownloader:
    def __init__(self, download_dir, test_bit=0):
        self._download_dir: str = download_dir
        self.keys: dict = {}
        self.test_bit = test_bit
        self._url: str = ''
        self._file_name: str = ''

        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'referer': 'https://www.jiosaavn.com/song/tere-naal/KD8zfAZpZFo',
            'origin': 'https://www.jiosaavn.com'
        }

    # ----------------------------------- #
    def get_url(self) -> str:
        return self._url

    def set_url(self, encrypted_url: str):
        self._url = encrypted_url

    def get_file_name(self) -> str:
        return self._file_name

    def set_file_name(self, title: str):
        self._file_name = title

    def get_download_dir(self) -> str:
        return self._download_dir

    def set_download_dir(self, download_dir: str):
        self._download_dir = download_dir

    # ----------------------------------- #

    def download(self, url: str, file_name: str, file_extension: str) -> str:
        _filename = file_name + '.' + file_extension
        _filename = re.sub(r'[?*<>|/\\":]', '', _filename)

        file_path: str = os.path.join(self._download_dir, _filename)

        print(f"Downloading '{file_name}'.....")
        raw_data = requests.get(url, stream=True, headers=self.headers)
        with open(file_path, "wb") as raw_file:
            for chunk in raw_data.iter_content(chunk_size=2048):
                if chunk:
                    raw_file.write(chunk)

        print("Download Successful")
        return file_path


def _default_hook(d):
    if d['status'] == 'finished':
        file_tuple = os.path.split(os.path.abspath(d['filename']))
        print("Done downloading {}".format(file_tuple[1]))
    if d['status'] == 'downloading':
        print(d['filename'], d['_percent_str'], d['_eta_str'])


class YTDLDownloader:
    """
    Inputs url as str, Downloads the video/audio to download dir
    Returns a code:
            1 = Successfull
            0 = wrong parameter
            -1/None = error
    """

    def __init__(self, download_url='https://www.youtube.com/watch?v=VdyBtGaspss', prefix=''):
        self._download_url: str = download_url
        self._prefix = prefix
        self._save_dir = os.path.expanduser("~/Downloads/Video")
        self._ydl_opts: dict = {
            'progress_hooks': [_default_hook],
            'quiet': True,
            'no_warnings': True,
            'outtmpl': '%(episode_number)s - %(title)s.%(ext)s'
        }

    def set_prefix(self, prefix):
        self._prefix = prefix

    def get_prefix(self):
        return self._prefix

    def set_download_url(self, download_url):
        self._download_url = download_url

    def get_download_url(self):
        return self._download_url

    def set_save_dir(self, save_dir):
        self._save_dir = save_dir

    def get_save_dir(self):
        return self._save_dir

    def start(self):
        os.chdir(self._save_dir)
        print("Saving to ", self._save_dir)

        if self._download_url == '':
            return 0  # means something is wrong with your params

        while True:
            try:
                with youtube_dl.YoutubeDL(self._ydl_opts) as ydl:
                    ydl.download([self._download_url])
            except:
                time.sleep(15)
                traceback.print_exc()
            else:
                return 1
