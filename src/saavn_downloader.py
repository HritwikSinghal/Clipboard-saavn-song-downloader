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

    def __init__(self, download_dir):

        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'referer': 'https://www.jiosaavn.com/song/tere-naal/KD8zfAZpZFo',
            'origin': 'https://www.jiosaavn.com'
        }

        self.all_types = {
            'artist': 'topSongs',
            'song': 'songs',
            'album': 'list',
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
        else:
            url = 'https://www.jiosaavn.com/song/shayad-from-love-aaj-kal/GjIBdCt,UX8'

        pyperclip.copy('')

        if str(url).startswith('https://www.jiosaavn.com'):
            print('got url: ', url)

            self.url = url
            _LOGGER.debug("url= " + self.url)

    def __download_song(self) -> None:
        # Fix title
        # todo: use tools class for this
        temp = self.keys.copy()
        title = Tagger(file_location='', keys=temp).fix_title()

        encrypted_url = self.keys['more_info']['encrypted_media_url']
        dec_url = SaavnUrlDecrypter(test=test_bit).get_decrypted_url(url=encrypted_url)

        my_downloader = downloader.FileDownloader(download_dir=self.download_dir, test_bit=test_bit)
        self._download_location = my_downloader.download(url=dec_url,
                                                         file_name=title,
                                                         file_extension='m4a')

    def __add_tags(self) -> None:
        my_tagger = Tagger(file_location=self._download_location, keys=self.keys)

        # since we are supplying keys from saavn
        my_tagger.convert_saavn_keys()
        my_tagger.add_tags()

    def run(self) -> None:
        while not self.url:
            self.__get_url()
        else:
            url_type = self.url.split('/')[3]

        input()
        exit(0)

        songs_json = saavn_API.API(test_bit=test_bit).fetch_details(url=self.url)

        # todo: add check if 'songs_json' is empty or not
        try:
            for song_info in songs_json[self.all_types[url_type]]:
                self.keys = song_info

                # ############## for testing ##############
                try:
                    if test_bit:
                        os.chdir(self.download_dir)  # So that below text files are saved in download dir.

                        with open(song_info["title"] + '.txt', 'w+') as ab:
                            json.dump(song_info, ab, indent=4)
                except:
                    print("Cannot create Song Details File for debug, check Song title")
                # ############# ############# #############
                self.__download_song()
                self.__add_tags()


        except:
            if test_bit:
                traceback.print_exc()
                self.url = ''
