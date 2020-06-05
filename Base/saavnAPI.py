import ast
import base64
import json
import os
import re
import traceback
from Base import tools

import requests
import urllib3.exceptions
from bs4 import BeautifulSoup
from pyDes import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

user_agent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'
}


# -------------------------------------------#

def decrypt_url(url):
    des_cipher = des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
    enc_url = base64.b64decode(url.strip())
    dec_url = des_cipher.decrypt(enc_url, padmode=PAD_PKCS5).decode('utf-8')
    dec_url = re.sub('_96.mp4', '_320.mp3', dec_url)
    print(dec_url)

    try:
        aac_url = dec_url[:]
        h_url = aac_url.replace('aac.saavncdn.com', 'h.saavncdn.com')

        # ---------------------------------------------------------#

        # check for 320 mp3 on aac.saavncdn.com
        r = requests.head(aac_url, allow_redirects=True)
        if str(r.status_code) == '200':
            return aac_url

        # check for 320 mp3 on h.saavncdn.com
        r = requests.head(h_url, allow_redirects=True)
        if str(r.status_code) == '200':
            return aac_url

        # ---------------------------------------------------------#

        # check for 160 mp3 on aac.saavncdn.com
        aac_url = aac_url.replace('_320.mp3', '_160.mp3')
        r = requests.head(h_url, allow_redirects=True)
        if str(r.status_code) == '200':
            return aac_url

        # check for 160 mp3 on h.saavncdn.com
        h_url = h_url.replace('_320.mp3', '_160.mp3')
        r = requests.head(h_url, allow_redirects=True)
        if str(r.status_code) == '200':
            return aac_url

        # ---------------------------------------------------------#
        # check for 128 mp3 on aac.saavncdn.com
        aac_url = aac_url.replace('_320.mp3', '.mp3')
        r = requests.head(h_url, allow_redirects=True)
        if str(r.status_code) == '200':
            return aac_url

        # check for 128 mp3 on h.saavncdn.com
        h_url = h_url.replace('_320.mp3', '.mp3')
        r = requests.head(h_url, allow_redirects=True)
        if str(r.status_code) == '200':
            return aac_url

        # ---------------------------------------------------------#
        # ---------------------------------------------------------#
        # ---------------------------------------------------------#
        # now trying for m4a
        # Edit: skipped m4a support as of now

        # aac_url = dec_url[:].replace(".mp3", '.mp4')
        # h_url = aac_url.replace('aac.saavncdn.com', 'h.saavncdn.com')
        #
        # # ---------------------------------------------------------#
        #
        # # check for 320 m4a on aac.saavncdn.com
        # r = requests.head(aac_url, allow_redirects=True)
        # if str(r.status_code) == '200':
        #     return aac_url
        #
        # # check for 320 m4a on h.saavncdn.com
        # r = requests.head(h_url, allow_redirects=True)
        # if str(r.status_code) == '200':
        #     return aac_url
        #
        # # ---------------------------------------------------------#
        #
        # # check for 160 m4a on aac.saavncdn.com
        # aac_url = aac_url.replace('_320.mp4', '_160.mp4')
        # r = requests.head(h_url, allow_redirects=True)
        # if str(r.status_code) == '200':
        #     return aac_url
        #
        # # check for 160 m4a on h.saavncdn.com
        # h_url = h_url.replace('_320.mp4', '_160.mp4')
        # r = requests.head(h_url, allow_redirects=True)
        # if str(r.status_code) == '200':
        #     return aac_url
        #
        # # ---------------------------------------------------------#
        # # check for 128 m4a on aac.saavncdn.com
        # aac_url = aac_url.replace('_320.mp4', '.mp4')
        # r = requests.head(h_url, allow_redirects=True)
        # if str(r.status_code) == '200':
        #     return aac_url
        #
        # # check for 128 m4a on h.saavncdn.com
        # h_url = h_url.replace('_320.mp4', '.mp4')
        # r = requests.head(h_url, allow_redirects=True)
        # if str(r.status_code) == '200':
        #     return aac_url

    except:
        return None


def get_lyrics(url):
    try:
        if '/song/' in url:
            # url = url.replace("/song/", '/lyrics/')
            source = requests.get(url).text
            soup = BeautifulSoup(source, 'html5lib')
            res = soup.find('p', class_='lyrics')
            lyrics = str(res).replace("<br/>", "\n")
            lyrics = lyrics.replace('<p class="lyrics"> ', '')
            lyrics = lyrics.replace("</p>", '')
            return (lyrics)
    except Exception:
        traceback.print_exc()
        return


def start(url, log_file, test=0):
    # returns list of songs from search url.
    # each element of list is a dict in json format with song data

    try:
        res = requests.get(url, headers=user_agent, data=[('bitrate', '320')])

        soup = BeautifulSoup(res.text, "html5lib")
        all_songs_info = soup.find_all('div', attrs={"class": "hide song-json"})

        song_list = []

        for info in all_songs_info:
            try:
                json_data = json.loads(str(info.text))

                #######################
                # print("IN TRY")
                #######################

            except:
                # the error is caused by quotation marks in songs title as shown below
                # (foo bar "XXX")
                # so just remove the whole thing inside parenthesis

                #######################
                # print("IN EXCEPT")
                # print(info.text)
                # x = input()
                #######################

                try:
                    x = re.compile(r'''
                        (
                        [(\]]
                        .*          # 'featured in' or 'from' or any other shit in quotes
                        "(.*)"      # album name
                        [)\]]
                        )
                        ","album.*"
                        ''', re.VERBOSE)

                    rem_str = x.findall(info.text)

                    # old method, dont know why this wont work
                    # json_data = re.sub(rem_str[0][0], '', str(info.text))

                    json_data = info.text.replace(rem_str[0][0], '')

                    #######################
                    # print("IN EXCEPT2")
                    # print(rem_str[0][0])
                    # print(json_data)
                    # a = input()
                    #######################

                    # actually that thing in () is the correct album name, so save it.
                    # since saavn uses song names as album names, this will be useful

                    if len(rem_str[0]) > 1:
                        actual_album = rem_str[0][1]
                    else:
                        actual_album = ''

                except:
                    # old method, if above wont work, this will work 9/10 times.

                    json_data = re.sub(r'.\(\b.*?"\)', "", str(info.text))
                    json_data = re.sub(r'.\[\b.*?"\]', "", json_data)
                    actual_album = ''

                try:
                    json_data = json.loads(str(json_data))
                except:
                    continue

                if actual_album != '':
                    json_data['actual_album'] = actual_album

            fix(json_data)
            json_data = json.dumps(json_data, indent=2)

            song_list.append(json_data)

        return song_list
    except Exception:
        print("invalid url...")
        tools.writeAndPrintLog(log_file, '\nSaavnAPI error, url={}\n'.format(url), test=test)
        return []


def fix(json_data):
    json_data['album'] = tools.removeGibberish(json_data['album']).strip()

    oldArtist = json_data['singers']
    newArtist = tools.removeGibberish(oldArtist)
    newArtist = tools.divideBySColon(newArtist)
    newArtist = tools.removeTrailingExtras(newArtist)
    json_data['singers'] = tools.removeDup(newArtist)

    old_composer = json_data['music']
    new_composer = tools.removeGibberish(old_composer)
    new_composer = tools.divideBySColon(new_composer)
    new_composer = tools.removeTrailingExtras(new_composer)
    json_data['music'] = tools.removeDup(new_composer)

    json_data['title'] = tools.removeGibberish(json_data['title'])
