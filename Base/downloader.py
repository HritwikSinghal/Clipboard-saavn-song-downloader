import html
import json
import os
import re
import urllib
import urllib.request

import requests
from mutagen.mp4 import *

from Base import saavnAPI
from Base import tools


class SongDownloader:

    def __init__(self, download_dir, url, log_file, test=0):

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
        self.url_type = url.split('/')[3]

        self.log_file = log_file
        self.download_dir = download_dir
        self.url = url
        self.test = test

        self.song_info = {}
        self.keys = {}

    def get_url(self):
        pass

    def run(self):
        songs_json = saavnAPI.start(self.url, self.log_file, test=self.test)

        for song_info in songs_json[self.all_types[self.url_type]]:
            self.song_info = song_info

            # for testing ####
            try:
                if self.test:
                    with open(song_info["title"] + '.txt', 'w+') as ab:
                        json.dump(song_info, ab, indent=4)
            except:
                print("Cannot create Song Details File for debug, check Song title")
            ###################

            self.keys = self.getImpKeys()
            download_location = self.downloadSong(keys)
            self.addtags(download_location, keys)

    def getImpKeys(self):
        keys = {}

        keys["title"] = self.keys["title"]
        keys["primary_artists"] = ", ".join(
            [artist["name"] for artist in self.keys["more_info"]["artistMap"]["primary_artists"]])
        keys["album"] = self.keys["more_info"]["album"]
        keys["singers"] = keys["primary_artists"]
        keys["music"] = self.keys["more_info"]["music"]
        keys["starring"] = ";".join(
            [artist["name"] for artist in self.keys["more_info"]["artistMap"]["artists"] if
             artist['role'] == 'starring'])
        keys['year'] = self.keys['year']
        keys["label"] = self.keys["more_info"]["label"]
        keys['image'] = self.keys['image']
        keys['encrypted_media_url'] = self.keys['more_info']['encrypted_media_url']
        keys["duration"] = self.keys["more_info"]["duration"]

        self.fix()

        return keys

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

        if self.test:
            print(json.dumps(self.keys, indent=2))

    def downloadSong(self, song_info):
        dec_url = saavnAPI.decrypt_url(song_info['encrypted_media_url'], test=self.test)
        filename = song_info['title'] + '.m4a'
        filename = re.sub(r'[?*<>|/\\":]', '', filename)

        location = os.path.join(self.download_dir, filename)

        print("Downloading '{0}'.....".format(song_info['title']))
        raw_data = requests.get(dec_url, stream=True, headers=self.headers)
        with open(location, "wb") as raw_song:
            for chunk in raw_data.iter_content(chunk_size=2048):
                if chunk:
                    raw_song.write(chunk)
        print("Download Successful")

        return location

    def addtags(self, filename, json_data):
        print('Adding Tags.....')

        audio = MP4(filename)

        audio['\xa9nam'] = html.unescape(str(json_data['title']))
        audio['\xa9ART'] = html.unescape(str(json_data['primary_artists']))
        audio['\xa9alb'] = html.unescape(str(json_data['album']))
        audio['aART'] = html.unescape(str(json_data['singers']))
        audio['\xa9wrt'] = html.unescape(str(json_data['music']))
        audio['desc'] = html.unescape(str(json_data['starring']))
        audio['\xa9gen'] = html.unescape(str(json_data['label']))
        audio['\xa9day'] = html.unescape(str(json_data['year']))

        cover_url = str(json_data['image'])
        fd = urllib.request.urlopen(cover_url)
        cover = MP4Cover(fd.read(), getattr(MP4Cover, 'FORMAT_PNG' if cover_url.endswith('png') else 'FORMAT_JPEG'))
        fd.close()
        audio['covr'] = [cover]

        audio.save()

        print("Tags Added Successfully")
