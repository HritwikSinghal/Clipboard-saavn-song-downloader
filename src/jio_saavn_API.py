import base64
import json
import traceback

import requests
import urllib3.exceptions
from pyDes import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class API:

    def __init__(self, url, log_file, test_bit=0):
        self.log_file = log_file
        self.url = url
        self.test = test_bit

        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
            'referer': 'https://www.jiosaavn.com/song/tera-mera-rishta/GVkMdDYCYXU',
            'origin': 'https://www.jiosaavn.com'
        }

        self.all_api_url = {
            'artist': 'https://www.jiosaavn.com/api.php?__call=webapi.get&token={0}&type=artist&p=&n_song=10&n_album=14&sub_type=&category=&sort_order=&includeMetaTags=0&ctx=web6dot0&api_version=4&',
            'album': 'https://www.jiosaavn.com/api.php?__call=webapi.get&token={0}&type=album&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0',
            'featured': 'https://www.jiosaavn.com/api.php?__call=webapi.get&token={0}&type=playlist&p=1&n=20&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0',
            'song': 'https://www.jiosaavn.com/api.php?__call=webapi.get&token={0}&type=song&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0',
            'top_search_results': 'https://www.jiosaavn.com/api.php?__call=content.getTopSearches&ctx=web6dot0&api_version=4&_format=json&_marker=0'
        }

        self.id = ''
        self.url_type = ''
        self.api_url = ''
        self.data = {}

    def run(self):
        self.url_type = self.url.split('/')[3]

        self.getID()
        self.api_url = self.all_api_url[self.url_type].format(self.id)
        res = requests.get(self.api_url, headers=self.headers, allow_redirects=True)

        data = str(res.text).strip()

        try:
            self.data = json.loads(data)
        except:
            self.fixContent()
            self.data = json.loads(self.data)

        return self.data

    def getID(self):
        self.id = str(self.url).split('/')[-1]

    def fixContent(self):
        # old
        # data = re.sub(r'<!DOCTYPE html>\s*<.*>?', '', data)
        # return data

        # this is fixed_json
        self.data = [x for x in self.data.splitlines() if x.strip().startswith('{')][0]


class decryter:

    def __init__(self, url, test=0):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'referer': 'https://www.jiosaavn.com/song/tere-naal/KD8zfAZpZFo',
            'origin': 'https://www.jiosaavn.com'
        }

        self.url = url
        self.test = test

    def decrypt_url(self):
        des_cipher = des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
        enc_url = base64.b64decode(self.url.strip())
        dec_url = des_cipher.decrypt(enc_url, padmode=PAD_PKCS5).decode('utf-8')

        dec_url = str(dec_url).replace('_96.mp4', '_320.mp4').replace('http', 'https')

        # if self.test:
        #     print(dec_url)
        #     print("NOTE: SEE SaavnAPI, it is returning this url without checking....\n" * 5)
        #     return dec_url

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

            return None
        except:
            if self.test:
                traceback.print_exc()
            return None
