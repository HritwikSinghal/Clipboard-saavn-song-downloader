import html
import json
import re
import urllib
import urllib.request

from mutagen.mp4 import *

from src import tools


class Tagger:
    """
    File should be m4a

    if you are providing keys directly from saavn, there is a function 'get_imp_keys' to covert them.
    saavn keys should be of type
        {
            'id' : 'MceJXmLX'
            'title' : 'Barsaat'
            'subtitle' : 'Armaan Malik - Barsaat'
            'header_desc' : 'Track from Armaan Malik from album Barsaat.'
            'type' : 'song'
            'perma_url' : 'https://www.jiosaavn.com/song/barsaat/PQsOeyxde2s'
            'image' : 'http://c.saavncdn.com/576/Barsaat-Hindi-2021-20210914181320-500x500.jpg'
            'language' : 'hindi'
            'year' : '2021'
            'play_count' : '210756'
            'explicit_content' : '0'
            'list_count' : '0'
            'list_type' : ''
            'list' : ''
            'more_info' : '{'music': 'Amaal Mallik', 'album_id': '29661242', 'album': 'Barsaat', 'label': 'MWM Entertainment', 'origin': 'album', 'is_dolby_content': False, '320kbps': 'true', 'encrypted_media_url': 'iPPGVzyogeiPwpro65A0eUaQggN+8+J4scA6AZdnzNIa1///O1rucKUF2RGKzmX1ue3pOy1P3YJAYMBiucJ0M4PzFaL/aK97', 'encrypted_cache_url': '', 'album_url': 'https://www.jiosaavn.com/album/barsaat/ec5Qo6AymJE_', 'duration': '221', 'rights': {'code': '0', 'cacheable': 'true', 'delete_cached_object': 'false', 'reason': ''}, 'cache_state': '', 'has_lyrics': 'true', 'lyrics_snippet': 'फिर आज है दिल रो रहाँ, सब कह रहें बरसात है', 'starred': 'false', 'copyright_text': '© 2021 MWM Entertainment', 'artistMap': {'primary_artists': [{'id': '464656', 'name': 'Armaan Malik', 'role': 'primary_artists', 'image': 'https://c.saavncdn.com/artists/Armaan_Malik_150x150.jpg', 'type': 'artist', 'perma_url': 'https://www.jiosaavn.com/artist/armaan-malik-/1iZ7Gi0bi1Y_'}], 'featured_artists': [], 'artists': [{'id': '743637', 'name': 'Amaal Mallik', 'role': 'music', 'image': 'https://c.saavncdn.com/artists/Amaal_Mallik_002_20191206162803_150x150.jpg', 'type': 'artist', 'perma_url': 'https://www.jiosaavn.com/artist/amaal-mallik-/hZrw5p6a5Sk_'}, {'id': '464656', 'name': 'Armaan Malik', 'role': 'singer', 'image': 'https://c.saavncdn.com/artists/Armaan_Malik_150x150.jpg', 'type': 'artist', 'perma_url': 'https://www.jiosaavn.com/artist/armaan-malik-/1iZ7Gi0bi1Y_'}, {'id': '10469457', 'name': 'Kunal Vermaa', 'role': 'lyricist', 'image': '', 'type': 'artist', 'perma_url': 'https://www.jiosaavn.com/artist/kunal-vermaa-/XpsNQWA02D8_'}]}, 'release_date': '2021-09-23', 'label_url': '/label/mwm-entertainment-albums/jGij7Uy4qkI_', 'vcode': '010911261418935', 'vlink': 'https://jiotunepreview.jio.com/content/Converted/010911261374760.mp3', 'triller_available': False, 'lyrics_id': ''}'
            'primary_artists' : 'Armaan Malik'
            'album' : 'Barsaat (2021)'
            'singers' : 'Armaan Malik'
            'music' : 'Amaal Mallik'
            'starring' : ''
            'label' : 'MWM Entertainment'
            'encrypted_media_url' : 'iPPGVzyogeiPwpro65A0eUaQggN+8+J4scA6AZdnzNIa1///O1rucKUF2RGKzmX1ue3pOy1P3YJAYMBiucJ0M4PzFaL/aK97'
            'duration' : '221'
        }

    """

    def __init__(self, file_location: str, keys: dict, test_bit=0):
        self._keys = keys
        self._file_location: str = file_location
        self.test_bit = test_bit

    # -------------------------------------------------------- #

    def get_keys(self):
        return self._keys

    def set_keys(self, keys: dict):
        self._keys = keys

    def get_file_location(self):
        return self._file_location

    def set_file_location(self, file_location: str):
        self._file_location = file_location

    # -------------------------------------------------------- #

    def fix_title(self):
        # Fix title
        new_title = self._keys['title'].replace('&quot;', '#')
        if new_title != self._keys['title']:
            self._keys['title'] = new_title
            self._keys['title'] = tools.removeGibberish(self._keys['title'])

            x = re.compile(r'''
                                    (
                                    [(\[]
                                    .*          # 'featured in' or 'from' or any other shit in quotes
                                    \#(.*)\#      # album name
                                    [)\]]
                                    )
                                    ''', re.VERBOSE)

            album_name = x.findall(self._keys['title'])
            self._keys['title'] = self._keys['title'].replace(album_name[0][0], '').strip()

            self._keys['album'] = album_name[0][1]

            # old method, if above wont work, this will work 9/10 times.
            # json_data = re.sub(r'.\(\b.*?"\)', "", str(info.text))
            # json_data = re.sub(r'.\[\b.*?"\]', "", json_data)
            # actual_album = ''
        self._keys['title'] = tools.removeGibberish(self._keys['title'])
        return self._keys['title']

    # todo: remove tools dependency, create a new class for it and import it wherever needed
    def fix(self):
        oldArtist = self._keys["primary_artists"].replace('&#039;', '')
        newArtist = tools.removeGibberish(oldArtist)
        newArtist = tools.divideBySColon(newArtist)
        newArtist = tools.removeTrailingExtras(newArtist)
        self._keys['primary_artists'] = tools.removeDup(newArtist)

        self._keys["singers"] = self._keys['primary_artists']

        old_composer = self._keys["music"]
        new_composer = tools.removeGibberish(old_composer)
        new_composer = tools.divideBySColon(new_composer)
        new_composer = tools.removeTrailingExtras(new_composer)
        self._keys["music"] = tools.removeDup(new_composer)

        self._keys['image'] = self._keys['image'].replace('-150x150.jpg', '-500x500.jpg')

        self.fix_title()

        self._keys["album"] = tools.removeGibberish(self._keys["album"]).strip()
        self._keys["album"] = self._keys["album"] + ' (' + self._keys['year'] + ')'

        if self.test_bit:
            print(json.dumps(self._keys, indent=2))

    def convert_saavn_keys(self):
        """
        converts keys from saavn format to the one used by this module
        :return: none
        """
        self._keys["title"] = self._keys["title"]
        self._keys["primary_artists"] = ", ".join(
            [artist["name"] for artist in self._keys["more_info"]["artistMap"]["primary_artists"]])
        self._keys["album"] = self._keys["more_info"]["album"]
        self._keys["singers"] = self._keys["primary_artists"]
        self._keys["music"] = self._keys["more_info"]["music"]
        self._keys["starring"] = ";".join(
            [artist["name"] for artist in self._keys["more_info"]["artistMap"]["artists"] if
             artist['role'] == 'starring'])
        self._keys['year'] = self._keys['year']
        self._keys["label"] = self._keys["more_info"]["label"]
        self._keys['image_url'] = self._keys['image']
        self._keys['encrypted_media_url'] = self._keys['more_info']['encrypted_media_url']
        self._keys["duration"] = self._keys["more_info"]["duration"]

    def add_tags(self):
        print('Adding Tags.....')

        self.fix()
        audio = MP4(self.get_file_location())

        audio['\xa9nam'] = html.unescape(str(self._keys['title']))
        audio['\xa9ART'] = html.unescape(str(self._keys['primary_artists']))
        audio['\xa9alb'] = html.unescape(str(self._keys['album']))
        # audio['aART'] = html.unescape(str(self._keys['singers']))                # Album Artist

        audio['\xa9wrt'] = html.unescape(str(self._keys['music']))
        audio['desc'] = html.unescape(str(self._keys['starring']))
        audio['\xa9gen'] = html.unescape(str(self._keys['label']))
        audio['\xa9day'] = html.unescape(str(self._keys['year']))

        cover_url = str(self._keys['image_url'])
        fd = urllib.request.urlopen(cover_url)
        cover = MP4Cover(fd.read(), getattr(MP4Cover, 'FORMAT_PNG' if cover_url.endswith('png') else 'FORMAT_JPEG'))
        fd.close()
        audio['covr'] = [cover]

        audio.save()
        print("Tags Added Successfully\n")
