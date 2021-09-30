import logging
import os
import re
import time
import traceback
from concurrent.futures.process import ProcessPoolExecutor

import requests
import youtube_dl

_LOGGER = logging.getLogger(__name__)

test_bit = os.environ.get('DEBUG', default='0')


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
    """

    def __init__(self, prefix='', save_dir: str = '', ydl_opts=None):
        self._prefix = prefix
        self._save_dir = os.path.expanduser("~/Downloads/Video") if save_dir == '' else save_dir
        self._ydl_opts: dict = {
            'progress_hooks': [_default_hook],
            'quiet': True,
            'no_warnings': True,
            'outtmpl': '%(episode_number)s - %(title)s.%(ext)s'
        } if ydl_opts is None else ydl_opts

    def set_prefix(self, prefix):
        self._prefix = prefix

    def get_prefix(self):
        return self._prefix

    def set_save_dir(self, save_dir):
        self._save_dir = save_dir

    def get_save_dir(self):
        return self._save_dir

    def __get_urls_from_playlist(self, playlist_url) -> list[str]:
        """Get the url of every video in a playlist
        :param playlist_url: url of playlist
        :return: list: list of urls of all videos in that playlist
        """
        return_list = []

        base_url = 'https://youtube.com/watch?v='
        with youtube_dl.YoutubeDL(self._ydl_opts) as ydl:
            result = ydl.extract_info(playlist_url, download=False)
            if 'entries' in result:
                # Can be a playlist or a list of videos
                video = result['entries']

                # loops entries to grab each video_url
                for i, item in enumerate(video):
                    video = result['entries'][i]
                    # print(base_url + video['id'])
                    return_list.append(str(base_url + video['id']))

                    """
                    Other things we can extract
                    result['entries'][i]['webpage_url']  # url of video
                    result['entries'][i]['title']  # title of video
                    result['entries'][i]['uploader']  # username of uploader
                    result['entries'][i]['playlist']  # name of the playlist
                    result['entries'][i]['playlist_index']  # order number of video
                    """

        return return_list

    def __check_for_playlist(self, list_of_download_url: list) -> list[str]:
        """Check if any url in list is a playlist url and extend old list with them
        :param list_of_download_url: list: list of all urls
        :return: list: new list concatenating the urls af individual videos of playlists
        """
        new_list = []
        for url in list_of_download_url:
            if url.startswith("https://www.youtube.com") and ('playlist' in url or '&list=' in url):
                new_list.extend(self.__get_urls_from_playlist(url))
            else:
                new_list.append(url)

        os.chdir(self._save_dir)
        with open('url_list.txt', 'w+') as myfile:
            for x in new_list:
                myfile.writelines(x)

        return new_list

    def _download(self, download_url):
        while True:
            try:
                with youtube_dl.YoutubeDL(self._ydl_opts) as ydl:
                    ydl.download([download_url])
            except:
                time.sleep(15)
                _LOGGER.debug(traceback.format_exc())

    def download(self, download_url_list: list[str] = None) -> None:
        if not len(download_url_list) > 0:
            _LOGGER.error("Input list has length <= 0")
            return None

        # Get individual videos from a playlist and download them also in parallel
        download_url_list = self.__check_for_playlist(download_url_list)

        os.chdir(self._save_dir)
        print("Saving to ", self._save_dir)

        # for x in download_url_list:
        #     print(x)
        # input()

        with ProcessPoolExecutor(max_workers=4) as executor:
            executor.map(self._download, download_url_list)
