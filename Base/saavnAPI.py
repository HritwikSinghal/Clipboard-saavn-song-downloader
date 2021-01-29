import base64
import json
import re
import traceback

import requests
import urllib3.exceptions
from pyDes import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
    'referer': 'https://www.jiosaavn.com/song/tere-naal/KD8zfAZpZFo',
    'origin': 'https://www.jiosaavn.com'
}

api_url = {
    'artist': 'https://www.jiosaavn.com/api.php?__call=webapi.get&token={0}&type=artist&p=&n_song=10&n_album=14&sub_type=&category=&sort_order=&includeMetaTags=0&ctx=web6dot0&api_version=4&',
    'album': 'https://www.jiosaavn.com/api.php?__call=webapi.get&token={0}&type=album&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0',
    'featured': 'https://www.jiosaavn.com/api.php?__call=webapi.get&token={0}&type=playlist&p=1&n=20&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0',
    'song': 'https://www.jiosaavn.com/api.php?__call=webapi.get&token={0}&type=song&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0',
    'top_search_results': 'https://www.jiosaavn.com/api.php?__call=content.getTopSearches&ctx=web6dot0&api_version=4&_format=json&_marker=0'
}


def getId(url):
    id = str(url).split('/')[-1]
    return id


def decrypt_url(url, test=0):
    des_cipher = des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
    enc_url = base64.b64decode(url.strip())
    dec_url = des_cipher.decrypt(enc_url, padmode=PAD_PKCS5).decode('utf-8')

    dec_url = str(dec_url).replace('_96.mp4', '_320.mp4').replace('http', 'https')

    # if test:
    #     print(dec_url)
    #     print("NOTE: SEE SaavnAPI, it is returning this url without checking....\n" * 5)
    #     return dec_url

    try:
        aac_url = dec_url[:]
        h_url = aac_url.replace('aac.saavncdn.com', 'h.saavncdn.com')

        # ---------------------------------------------------------#

        # check for 320 m4a on aac.saavncdn.com
        r = requests.head(aac_url, allow_redirects=True, headers=headers)
        if str(r.status_code) == '200':
            return aac_url

        # check for 320 m4a on h.saavncdn.com
        r = requests.head(h_url, allow_redirects=True, headers=headers)
        if str(r.status_code) == '200':
            return h_url

        # ---------------------------------------------------------#

        # check for 160 m4a on aac.saavncdn.com
        aac_url = aac_url.replace('_320.mp4', '_160.mp4')
        r = requests.head(aac_url, allow_redirects=True, headers=headers)
        if str(r.status_code) == '200':
            return aac_url

        # check for 160 m4a on h.saavncdn.com
        h_url = h_url.replace('_320.mp4', '_160.mp4')
        r = requests.head(h_url, allow_redirects=True, headers=headers)
        if str(r.status_code) == '200':
            return h_url

        # ---------------------------------------------------------#
        # check for 128 m4a on aac.saavncdn.com
        aac_url = aac_url.replace('_320.mp4', '.mp4')
        r = requests.head(aac_url, allow_redirects=True, headers=headers)
        if str(r.status_code) == '200':
            return aac_url

        # check for 128 m4a on h.saavncdn.com
        h_url = h_url.replace('_320.mp4', '.mp4')
        r = requests.head(h_url, allow_redirects=True, headers=headers)
        if str(r.status_code) == '200':
            return h_url

        return None
    except:
        if test:
            traceback.print_exc()
        return None


def fixContent(data):
    # old
    # data = re.sub(r'<!DOCTYPE html>\s*<.*>?', '', data)
    # return data

    fixed_json = [x for x in data.splitlines() if x.strip().startswith('{')][0]
    return fixed_json


def start(url, log_file, test=0):
    url_type = url.split('/')[3]
    url = api_url[url_type].format(getId(url))
    res = requests.get(url, headers=headers)

    data = str(res.text).strip()

    try:
        data = json.loads(data)
    except:
        data = fixContent(data)
        data = json.loads(data)

    return data
