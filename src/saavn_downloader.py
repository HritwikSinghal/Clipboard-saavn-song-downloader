import json
import logging
import os
import traceback

import pyperclip

from src.tools import downloader, saavn_API
from src.tools.saavn_API import SaavnUrlDecrypter
from src.tools.tagger import Tagger

_LOGGER = logging.getLogger(__name__)

test_bit = os.environ.get('DEBUG', default='0')


class SaavnDownloader:

    def __init__(self, download_dir: str):

        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'referer': 'https://www.jiosaavn.com/song/tere-naal/KD8zfAZpZFo',
            'origin': 'https://www.jiosaavn.com'
        }

        self.all_types = {
            'song': 'songs',
            'album': 'list',
            'artist': 'topSongs',
            'featured': 'list'
        }
        self.url: str = ''

        self.download_dir: str = download_dir

        self.keys: dict = {}
        self._download_location: str = ''

    def __get_url(self) -> None:
        print('\nWaiting for url from clipboard....')

        if not test_bit:
            url = pyperclip.waitForPaste()
            _LOGGER.debug(f"Got {url} from clipboard")
        else:
            url = 'https://www.jiosaavn.com/song/shayad-from-love-aaj-kal/GjIBdCt,UX8'
            _LOGGER.debug("Testing, so Set url to " + url)

        pyperclip.copy('')

        if str(url).startswith('https://www.jiosaavn.com'):
            print('got url: ', url)

            self.url = url
            _LOGGER.debug("Got url = " + self.url)

    def __download_song(self) -> None:
        _LOGGER.debug("Downloading song")

        # todo: Fix title & use tools class for this
        temp = self.keys.copy()
        title = Tagger(file_location='', keys=temp).fix_title()
        _LOGGER.debug("title = " + title)

        encrypted_url: str = self.keys['more_info']['encrypted_media_url']
        _LOGGER.debug(encrypted_url)
        dec_url: str = SaavnUrlDecrypter(test=test_bit).get_decrypted_url(url=encrypted_url)
        _LOGGER.debug(dec_url)

        my_downloader = downloader.FileDownloader(download_dir=self.download_dir, test_bit=test_bit)
        self._download_location = my_downloader.download(url=dec_url,
                                                         file_name=title,
                                                         file_extension='m4a')

        _LOGGER.debug("download_location = " + self._download_location)

    def __add_tags(self) -> None:
        _LOGGER.debug("Adding tags")
        my_tagger = Tagger(file_location=self._download_location, keys=self.keys)

        # since we are supplying keys from saavn
        _LOGGER.debug("Converting saavn keys")
        my_tagger.convert_saavn_keys()

        my_tagger.add_tags()
        _LOGGER.debug("Adding tags Done")

    def run(self) -> None:
        while not self.url:
            self.__get_url()
        else:
            url_type = self.url.split('/')[3]
            _LOGGER.debug("url type = " + url_type)

        songs_json: dict = saavn_API.API(test_bit=test_bit).fetch_details(url=self.url)
        _LOGGER.debug(songs_json)

        # todo: add check if 'songs_json' is empty or not
        try:
            for song_info in songs_json[self.all_types[url_type]]:
                self.keys = song_info

                # ############## for testing ##############
                if test_bit == '1':
                    try:
                        os.chdir(self.download_dir)  # So that below text files are saved in download dir.

                        with open(song_info["title"] + '.txt', 'w+') as ab:
                            json.dump(song_info, ab, indent=4)
                    except:
                        _LOGGER.error("Cannot create Song Details File for debug, check Song title")
                        _LOGGER.error(traceback.format_exc())
                # ############# ############# #############

                self.__download_song()
                self.__add_tags()

        except Exception as e:
            _LOGGER.error(traceback.format_exc())
