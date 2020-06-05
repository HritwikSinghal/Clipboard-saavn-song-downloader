import json
import re
import traceback
import os

import mutagen
from mutagen.mp3 import MP3

import requests
from mutagen.easyid3 import EasyID3 as easyid3

from Base import saavnAPI
from Base import tools
from Tags import addDateLenOrg
from Tags import albumArt
from Tags import albumName
from Tags import artistName
from Tags import composerName
from Tags import songTitle


def getCertainKeys(song_info):
    # these are the keys which are useful to us

    rel_keys = [
        'title',
        'album',
        'singers',
        'music',
        'url',

        'year',
        'label',
        'duration',

        'e_songid',
        'image_url',
        'tiny_url',
        'actual_album'
    ]

    json_data = json.loads(song_info)

    #########################
    # print(song_info)
    # x = input()
    #########################

    # this will store all relevant keys and their values
    rinfo = {}

    # for k, v in json_data.items():
    #     print(k, ':', v)

    for key in json_data:

        if key in rel_keys:
            if key == 'singers':
                rinfo['artist'] = json_data[key].strip()
            elif key == 'music':
                rinfo['composer'] = json_data[key].strip()
            elif key == 'year':
                rinfo['date'] = json_data[key].strip()
            elif key == 'duration':
                rinfo['length'] = json_data[key].strip()
            elif key == 'label':
                rinfo['organization'] = json_data[key].strip()
            elif key == 'image_url':
                rinfo['image_url'] = tools.fixImageUrl(json_data[key])
            elif key == 'tiny_url':
                rinfo['lyrics_url'] = json_data[key].replace("/song/", '/lyrics/')
            # elif key == 'url':
            #     rinfo['url'] = saavnAPI.decrypt_url(json_data[key])
            # elif key == 'lyrics':
            #     rinfo['lyrics'] = saavnAPI.get_lyrics(json_data['tiny_url'])
            else:
                rinfo[key] = json_data[key].strip()

    return rinfo


def downloadSong(download_dir, log_file, song_info, test=0):
    os.chdir(download_dir)
    name = re.sub(r'[?*<>|/\\":]', '', song_info['title'])

    name_with_path = os.path.join(download_dir, name + '.mp3')

    # check if song name already exists in download folder
    if os.path.isfile(name_with_path):
        old_name_with_path = os.path.join(download_dir, name + '_OLD.mp3')

        try:
            os.rename(name_with_path, old_name_with_path)
            print('Song already exists, renaming it to "' + name + '_OLD.mp3"')
        except FileExistsError:
            os.remove(old_name_with_path)
            os.rename(name_with_path, old_name_with_path)

    # Download Song
    try:
        dec_url = saavnAPI.decrypt_url(song_info['url'])
        if dec_url is None:
            return '-1'

        print("Downloading '{0}'.....".format(name))

        raw_data = requests.get(dec_url, stream=True)
        with open(name_with_path, "wb") as raw_song:
            for chunk in raw_data.iter_content(chunk_size=2048):
                # writing one chunk at a time to mp3 file
                if chunk:
                    raw_song.write(chunk)

        print("Song download successful.")
        return name_with_path

    except:
        print("Song download failed...")
        tools.writeAndPrintLog(log_file, "\nSong download failed...\n", test=test)

        if os.path.isfile(name_with_path):
            os.remove(name_with_path)

        return '-1'


def addTags(downloaded_song_name_with_path, download_dir, log_file, song_info, test=0):
    os.chdir(download_dir)
    try:
        tags = easyid3(downloaded_song_name_with_path)
    except:
        print("This Song has no tags. Creating tags...")

        tags = mutagen.File(downloaded_song_name_with_path, easy=True)
        tags.add_tags()
        print("Tags created.")

    addDateLenOrg.start(tags, song_info)
    albumName.start(tags, song_info)
    artistName.start(tags, song_info)
    composerName.start(tags, song_info)
    songTitle.start(tags, song_info)
    albumArt.start(song_info, download_dir, downloaded_song_name_with_path)


def start(download_dir, url, log_file, test=0):
    list_of_songs_with_info = saavnAPI.start(url, log_file, test=test)
    # tools.printList(list_of_songs_with_info)

    for song in list_of_songs_with_info:
        song_info = getCertainKeys(song)
        if song_info is None:
            return None

        # print(song_info)
        # x = input()

        downloaded_song_name_with_path = downloadSong(download_dir, log_file, song_info, test=test)
        if downloaded_song_name_with_path == '-1':
            continue

        addTags(downloaded_song_name_with_path, download_dir, log_file, song_info, test=test)
        print()
