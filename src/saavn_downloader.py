import json
import os
import traceback

import pyperclip

from src import downloader
from src import saavn_API
from src.saavn_API import decrypter
from src.tagger import Tagger


class SongDownloader:

    def __init__(self, download_dir, log_file, test=0):

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
        self.url = ''
        self.url_type = ''

        self.download_dir = download_dir
        self.log_file = log_file
        self.test_bit = test

        self.keys = {}
        self._download_location = ''

    def set_url(self, url):
        self.url = url

    def get_url(self):
        print('\nWaiting for url from clipboard....')

        # url = pyperclip.waitForPaste()
        url = 'https://www.jiosaavn.com/song/shayad-from-love-aaj-kal/GjIBdCt,UX8'
        pyperclip.copy('')

        if str(url).startswith('https://www.jiosaavn.com'):
            print('got url: ', url)

            self.set_url(url)
            self.url_type = self.url.split('/')[3]

    def __download_song(self):
        # Fix title
        temp = self.keys.copy()
        title = Tagger(file_location='', keys=temp).fix_title()

        encrypted_url = self.keys['more_info']['encrypted_media_url']
        dec_url = decrypter(test=self.test_bit).get_decrypted_url(url=encrypted_url)

        my_downloader = downloader.Downloader(download_dir=self.download_dir, test_bit=self.test_bit)
        self._download_location = my_downloader.download(url=dec_url,
                                                         file_name=title,
                                                         file_extension='m4a')

    def __add_tags(self):
        my_tagger = Tagger(file_location=self._download_location, keys=self.keys)

        # since we are supplying keys from saavn
        my_tagger.convert_saavn_keys()
        my_tagger.add_tags()

    def run(self):
        while not self.url:
            self.get_url()
        else:
            self.url_type = self.url.split('/')[3]

        songs_json = saavn_API.API(test_bit=self.test_bit).run(url=self.url)

        # todo: add check if 'songs_json' is empty or not
        try:
            for song_info in songs_json[self.all_types[self.url_type]]:
                self.keys = song_info

                # ############## for testing ##############
                try:
                    if self.test_bit:
                        os.chdir(self.download_dir)  # So that below text files are saved in download dir.

                        with open(song_info["title"] + '.txt', 'w+') as ab:
                            json.dump(song_info, ab, indent=4)
                except:
                    print("Cannot create Song Details File for debug, check Song title")
                # ############# ############# #############
                self.__download_song()
                self.__add_tags()


        except:
            if self.test_bit:
                traceback.print_exc()
                self.url = ''
