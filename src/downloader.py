import html
import json
import os
import re
import traceback
import urllib
import urllib.request

import pyperclip
import requests
from mutagen.mp4 import *

from src import jio_saavn_API
from src import tools


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
        self.download_location = ''

        self.fix_done = False
        self.song_downloaded = False
        self.tags_added = False

    def set_url(self, url):
        self.url = url

    def run(self):
        while not self.url:
            self.get_url()
        else:
            self.url_type = self.url.split('/')[3]

        saavn_api_obj = jio_saavn_API.API(self.url, self.log_file, self.test_bit)
        songs_json = saavn_api_obj.run()

        # todo: add check if 'songs_json' is empty or not
        try:
            for song_info in songs_json[self.all_types[self.url_type]]:
                self.keys = song_info

                # for testing ####
                try:
                    if self.test_bit:
                        os.chdir(self.download_dir)  # So that below text files are saved in download dir.

                        with open(song_info["title"] + '.txt', 'w+') as ab:
                            json.dump(song_info, ab, indent=4)
                except:
                    print("Cannot create Song Details File for debug, check Song title")
                ###################

                self.get_imp_keys()
                if self.fix_done:
                    self.download_song()
                if self.song_downloaded:
                    self.add_tags()
        except:
            if self.test_bit:
                traceback.print_exc()
                self.url = ''

    def get_url(self):
        print('\nWaiting for url from clipboard....')

        url = pyperclip.waitForPaste()
        # url = 'https://www.jiosaavn.com/song/shayad-from-love-aaj-kal/GjIBdCt,UX8'
        pyperclip.copy('')

        if str(url).startswith('https://www.jiosaavn.com'):
            print('got url: ', url)

            self.url = url
            self.url_type = self.url.split('/')[3]

    def get_imp_keys(self):

        self.keys["title"] = self.keys["title"]
        self.keys["primary_artists"] = ", ".join(
            [artist["name"] for artist in self.keys["more_info"]["artistMap"]["primary_artists"]])
        self.keys["album"] = self.keys["more_info"]["album"]
        self.keys["singers"] = self.keys["primary_artists"]
        self.keys["music"] = self.keys["more_info"]["music"]
        self.keys["starring"] = ";".join(
            [artist["name"] for artist in self.keys["more_info"]["artistMap"]["artists"] if
             artist['role'] == 'starring'])
        self.keys['year'] = self.keys['year']
        self.keys["label"] = self.keys["more_info"]["label"]
        self.keys['image'] = self.keys['image']
        self.keys['encrypted_media_url'] = self.keys['more_info']['encrypted_media_url']
        self.keys["duration"] = self.keys["more_info"]["duration"]

        self.fix()

    def fix(self):
        oldArtist = self.keys["primary_artists"].replace('&#039;', '')
        newArtist = tools.removeGibberish(oldArtist)
        newArtist = tools.divideBySColon(newArtist)
        newArtist = tools.removeTrailingExtras(newArtist)
        self.keys['primary_artists'] = tools.removeDup(newArtist)

        self.keys["singers"] = self.keys['primary_artists']

        old_composer = self.keys["music"]
        new_composer = tools.removeGibberish(old_composer)
        new_composer = tools.divideBySColon(new_composer)
        new_composer = tools.removeTrailingExtras(new_composer)
        self.keys["music"] = tools.removeDup(new_composer)

        self.keys['image'] = self.keys['image'].replace('-150x150.jpg', '-500x500.jpg')

        # ---------------------------------------------------------------#

        new_title = self.keys['title'].replace('&quot;', '#')
        if new_title != self.keys['title']:
            self.keys['title'] = new_title
            self.keys['title'] = tools.removeGibberish(self.keys['title'])

            x = re.compile(r'''
                                    (
                                    [(\[]
                                    .*          # 'featured in' or 'from' or any other shit in quotes
                                    \#(.*)\#      # album name
                                    [)\]]
                                    )
                                    ''', re.VERBOSE)

            album_name = x.findall(self.keys['title'])
            self.keys['title'] = self.keys['title'].replace(album_name[0][0], '').strip()

            self.keys['album'] = album_name[0][1]

            # old method, if above wont work, this will work 9/10 times.
            # json_data = re.sub(r'.\(\b.*?"\)', "", str(info.text))
            # json_data = re.sub(r'.\[\b.*?"\]', "", json_data)
            # actual_album = ''

        self.keys['title'] = tools.removeGibberish(self.keys['title'])
        self.keys["album"] = tools.removeGibberish(self.keys["album"]).strip()
        self.keys["album"] = self.keys["album"] + ' (' + self.keys['year'] + ')'

        self.fix_done = True

        if self.test_bit:
            print(json.dumps(self.keys, indent=2))

    def download_song(self):
        my_decrypter = jio_saavn_API.decryter(self.keys['encrypted_media_url'], test=self.test_bit)
        dec_url = my_decrypter.decrypt_url()

        filename = self.keys['title'] + '.m4a'
        filename = re.sub(r'[?*<>|/\\":]', '', filename)

        location = os.path.join(self.download_dir, filename)

        print("Downloading '{0}'.....".format(self.keys['title']))
        raw_data = requests.get(dec_url, stream=True, headers=self.headers)
        with open(location, "wb") as raw_song:
            for chunk in raw_data.iter_content(chunk_size=2048):
                if chunk:
                    raw_song.write(chunk)

        self.song_downloaded = True
        if self.song_downloaded:
            print("Download Successful")

        self.download_location = location

    def add_tags(self):
        print('Adding Tags.....')

        audio = MP4(self.download_location)

        audio['\xa9nam'] = html.unescape(str(self.keys['title']))
        audio['\xa9ART'] = html.unescape(str(self.keys['primary_artists']))
        audio['\xa9alb'] = html.unescape(str(self.keys['album']))
        # audio['aART'] = html.unescape(str(self.keys['singers']))                # Album Artist
        audio['\xa9wrt'] = html.unescape(str(self.keys['music']))
        audio['desc'] = html.unescape(str(self.keys['starring']))
        audio['\xa9gen'] = html.unescape(str(self.keys['label']))
        audio['\xa9day'] = html.unescape(str(self.keys['year']))

        cover_url = str(self.keys['image'])
        fd = urllib.request.urlopen(cover_url)
        cover = MP4Cover(fd.read(), getattr(MP4Cover, 'FORMAT_PNG' if cover_url.endswith('png') else 'FORMAT_JPEG'))
        fd.close()
        audio['covr'] = [cover]

        audio.save()
        print("Tags Added Successfully\n")
