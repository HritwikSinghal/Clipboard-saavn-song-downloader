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

        self.download_dir = download_dir
        self.url = url
        self.log_file = log_file
        self.test = test

        self.keys = {}
        self.download_location = ''

    def get_url(self):
        pass

    def run(self):
        songs_json = saavnAPI.start(self.url, self.log_file, test=self.test)

        for song_info in songs_json[self.all_types[self.url_type]]:
            self.keys = song_info

            # for testing ####
            try:
                if self.test:
                    with open(song_info["title"] + '.txt', 'w+') as ab:
                        json.dump(song_info, ab, indent=4)
            except:
                print("Cannot create Song Details File for debug, check Song title")
            ###################

            self.getImpKeys()
            self.downloadSong()
            self.addtags()

    def getImpKeys(self):

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

        if self.test:
            print(json.dumps(self.keys, indent=2))

    def downloadSong(self):
        dec_url = saavnAPI.decrypt_url(self.keys['encrypted_media_url'], test=self.test)
        filename = self.keys['title'] + '.m4a'
        filename = re.sub(r'[?*<>|/\\":]', '', filename)

        location = os.path.join(self.download_dir, filename)

        print("Downloading '{0}'.....".format(self.keys['title']))
        raw_data = requests.get(dec_url, stream=True, headers=self.headers)
        with open(location, "wb") as raw_song:
            for chunk in raw_data.iter_content(chunk_size=2048):
                if chunk:
                    raw_song.write(chunk)
        print("Download Successful")

        self.download_location = location

    def addtags(self):
        print('Adding Tags.....')

        audio = MP4(self.download_location)

        audio['\xa9nam'] = html.unescape(str(self.keys['title']))
        audio['\xa9ART'] = html.unescape(str(self.keys['primary_artists']))
        audio['\xa9alb'] = html.unescape(str(self.keys['album']))
        audio['aART'] = html.unescape(str(self.keys['singers']))
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

        print("Tags Added Successfully")