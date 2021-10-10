import logging
import os
import time
import traceback
from concurrent.futures.process import ProcessPoolExecutor

import requests
# import youtube_dl
import yt_dlp

_LOGGER = logging.getLogger(__name__)

test_bit = int(os.environ.get('DEBUG', default='0'))


class FileDownloader:
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'referer': 'https://www.jiosaavn.com/song/tere-naal/KD8zfAZpZFo',
            'origin': 'https://www.jiosaavn.com'
        }

    def _download(self, data) -> None:
        url, filename, file_path = data

        print(f"Downloading '{filename}'.....")
        raw_data = requests.get(url, stream=True, headers=self.headers)
        with open(file_path, "wb") as raw_file:
            for chunk in raw_data.iter_content(chunk_size=2048):
                if chunk:
                    raw_file.write(chunk)

        print(f"'{filename}' Downloaded successfully")

    def download(self, data_list: list[tuple]) -> None:
        """
        :param data_list: list[tuple]: a list of tuples.
                            Each tuple contains (url: str, filename: str, filename: str, download_file_path: str)
        :return: None
        """

        # Parallel download files
        with ProcessPoolExecutor(max_workers=4) as executor:
            executor.map(self._download, data_list)


def _default_hook(d: dict) -> None:
    if d['status'] == 'finished':
        file_tuple = os.path.split(os.path.abspath(d['filename']))
        print(f"Done downloading {file_tuple[1]}")
    if d['status'] == 'downloading':
        print(d['filename'], d['_percent_str'], d['_eta_str'])


class YTDLDownloader:
    """Input a list of urls and download them parallely in download dir."""

    def __init__(self, prefix='', save_dir: str = '', ydl_opts=None):
        self._prefix: str = prefix
        self._save_dir: str = os.path.expanduser("~/Downloads/Video") if save_dir == '' else save_dir
        self._ydl_opts: dict = {
            'progress_hooks': [_default_hook],
            'quiet': True,
            'no_warnings': True,
            'outtmpl': '%(episode_number)s - %(title)s.%(ext)s'
        } if ydl_opts is None else ydl_opts

    def set_prefix(self, prefix):
        self._prefix = prefix

    def get_prefix(self) -> str:
        return self._prefix

    def set_save_dir(self, save_dir):
        self._save_dir = save_dir

    def get_save_dir(self) -> str:
        return self._save_dir

    def __get_urls_from_playlist(self, playlist_url) -> list[str]:
        """Get the url of every video in a playlist
        :param playlist_url: url of playlist
        :return: list: list of urls of all videos in that playlist
        """
        return_list = []

        base_url = 'https://youtube.com/watch?v='
        with yt_dlp.YoutubeDL(self._ydl_opts) as ydl:
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
                myfile.writelines(x + '\n')

        return new_list

    def _download(self, download_url) -> None:
        while True:
            try:
                with yt_dlp.YoutubeDL(self._ydl_opts) as ydl:
                    ydl.download([download_url])
            except:
                time.sleep(15)
                _LOGGER.debug(traceback.format_exc())

    def download(self, download_url_list: list[str], max_workers=4) -> None:
        """Input a list of urls and download them parallely in download dir.
        :param download_url_list: list[str] : list of urls
        :return: None
        """
        if not len(download_url_list) > 0:
            _LOGGER.error("Input list has length <= 0")
            return None

        # Get individual videos from a playlist and download them also in parallel
        download_url_list = self.__check_for_playlist(download_url_list)

        os.chdir(self._save_dir)
        print("Saving to ", self._save_dir)

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            executor.map(self._download, download_url_list)
