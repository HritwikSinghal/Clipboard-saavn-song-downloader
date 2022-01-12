import base64
import json
import logging
import os
import traceback

import requests
import urllib3.exceptions
from pyDes import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_LOGGER = logging.getLogger(__name__)

test_bit = int(os.environ.get('DEBUG', default='0'))


class API:

    def __init__(self):
        # To create a get request with payload as a dict, requests.get(url, params=payload)
        # To create a post request with payload as a dict, requests.get(url, data=payload)
        # payload = {"a" : 1, "b" : 2}

        self._api_url = 'https://www.jiosaavn.com/api.php'

        self._token_payload: dict = {
            "song": {
                '__call': 'webapi.get',
                'token': '',
                'type': 'song',
                'includeMetaTags': '0',
                'ctx': 'web6dot0',
                'api_version': '4',
                '_format': 'json',
                '_marker': '0',
            },

            "album": {
                '__call': 'webapi.get',
                'token': '',
                'type': 'album',
                'includeMetaTags': '0',
                'ctx': 'web6dot0',
                'api_version': '4',
                '_format': 'json',
                '_marker': '0',
            },

            "artist": {
                '__call': 'webapi.get',
                'token': '',
                'type': 'artist',
                'p': '1',
                'n_song': '30',
                'n_album': '14',
                'sub_type': '',
                'category': '',
                'sort_order': '',
                'includeMetaTags': '0',
                'ctx': 'web6dot0',
                'api_version': '4',
                '_format': 'json',
            },

            "featured": {
                '__call': 'webapi.get',
                'token': '',
                'type': 'playlist',
                'p': '1',
                'n': '20',
                'includeMetaTags': '0',
                'ctx': 'web6dot0',
                'api_version': '4',
                '_format': 'json',
                '_marker': '0',
            },

            "top_search_results": {
                '__call': 'content.getTopSearches',
                'ctx': 'web6dot0',
                'api_version': '4',
                '_format': 'json',
                '_marker': '0',
            },

            "lyrics": {
                '__call': 'lyrics.getLyrics',
                'lyrics_id': 'jZjE_NfL',  # Need to find how this ID is generated
                'ctx': 'web6dot0',
                'api_version': 4,
                '_format': 'json',
                '_marker': '0'
            },

            "playlist": {
                '__call': 'webapi.get',
                'token': '',
                'type': 'playlist',
                'includeMetaTags': '0',
                'ctx': 'web6dot0',
                'api_version': '4',
                '_format': 'json',
                '_marker': '0',
            },

        }

        self._payload = {
            "playlist": {
                '__call': 'playlist.getDetails',
                '_format': 'json',
                'listid': int,
            },
        }

        self._headers: dict = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
            'referer': 'https://www.jiosaavn.com/song/tera-mera-rishta/GVkMdDYCYXU',
            'origin': 'https://www.jiosaavn.com'
        }

        self._data: str = ''

    def _fix_content(self, data: str) -> None:
        """Fixes the response returned by API if the response contains additional HTML tags."""
        # old
        # data = re.sub(r'<!DOCTYPE html>\s*<.*>?', '', data)
        # return data

        # this is fixed_json
        data = [
            x for x in data.splitlines()
            if x.strip().startswith('{')
        ]

        self._data = data[0]

    def _fetch_lyrics(self) -> None:
        pass

    def _get_id(self) -> str:
        return ''

    def fetch_details(self, url: str) -> dict:
        """ Returns the details of song/playlist/album in a dict.
        :param url: str: url of song/playlist/album etc.
        :return: dict: contains "songs" as key and a list as value. The list contain details of each song
        """

        url = url.replace(r'\?autoplay=enabled', '')
        url_type: str = url.split('/')[3]  # song, album, artist etc
        if url_type == 's':
            url_type = url.split('/')[4]  # playlist

        token: str = str(url).split('/')[-1]

        if url_type == 'playlist':
            payload: dict = self._token_payload[url_type]
            payload['token'] = token
            id: int = requests.get(self._api_url, params=payload, headers=self._headers, allow_redirects=True).json()[
                'id']

            payload: dict = self._payload[url_type]
            payload['listid'] = int(id)
        else:
            payload: dict = self._token_payload[url_type]
            payload['token'] = token

        res = requests.get(self._api_url, params=payload, headers=self._headers, allow_redirects=True)
        data: str = str(res.text).strip()

        try:
            self._data = json.loads(data)
            # _LOGGER.debug(json.dumps(self._data, indent=2))

        except Exception as e:
            _LOGGER.warning("Some error in loading data returned by Saavn to json")
            _LOGGER.warning(traceback.format_exc())

            self._fix_content(data)
            self._data: dict = json.loads(self._data)

        _LOGGER.debug("data = " + str(self._data))
        return self._data


class SaavnUrlDecrypter:

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
            'referer': 'https://www.jiosaavn.com/song/tere-naal/KD8zfAZpZFo',
            'origin': 'https://www.jiosaavn.com'
        }

    def get_decrypted_url(self, url: str) -> str:
        """Takes encrypted URL string from saavn, and returns the decrypted URL
        :param url: str: encrypted url from saavn
        :return: str: decrypted url
        """
        des_cipher = des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
        enc_url = base64.b64decode(url.strip())
        dec_url: str = des_cipher.decrypt(enc_url, padmode=PAD_PKCS5).decode('utf-8')

        dec_url = dec_url.replace('_96.mp4', '_320.mp4').replace('http://', 'https://')

        try:
            aac_url = dec_url[:]
            h_url = aac_url.replace('aac.saavncdn.com', 'h.saavncdn.com')

            # ---------------------------------------------------------#

            # check for 320 m4a on aac.saavncdn.com
            r = requests.head(aac_url, allow_redirects=True, headers=self.headers)
            if str(r.status_code) == '200':
                return aac_url

            # check for 320 m4a on h.saavncdn.com
            r = requests.head(h_url, allow_redirects=True, headers=self.headers)
            if str(r.status_code) == '200':
                return h_url

            # ---------------------------------------------------------#

            # check for 160 m4a on aac.saavncdn.com
            aac_url = aac_url.replace('_320.mp4', '_160.mp4')
            r = requests.head(aac_url, allow_redirects=True, headers=self.headers)
            if str(r.status_code) == '200':
                return aac_url

            # check for 160 m4a on h.saavncdn.com
            h_url = h_url.replace('_320.mp4', '_160.mp4')
            r = requests.head(h_url, allow_redirects=True, headers=self.headers)
            if str(r.status_code) == '200':
                return h_url

            # ---------------------------------------------------------#
            # check for 128 m4a on aac.saavncdn.com
            aac_url = aac_url.replace('_320.mp4', '.mp4')
            r = requests.head(aac_url, allow_redirects=True, headers=self.headers)
            if str(r.status_code) == '200':
                return aac_url

            # check for 128 m4a on h.saavncdn.com
            h_url = h_url.replace('_320.mp4', '.mp4')
            r = requests.head(h_url, allow_redirects=True, headers=self.headers)
            if str(r.status_code) == '200':
                return h_url

            return ''
        except:
            _LOGGER.error(traceback.format_exc())
            return ''
