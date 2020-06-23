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

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
    'referer': 'https://www.jiosaavn.com/song/tere-naal/KD8zfAZpZFo',
    'origin': 'https://www.jiosaavn.com'
}


def addtags(filename, json_data, log_file, test=0):
    audio = MP4(filename)

    audio['\xa9nam'] = html.unescape(str(json_data['song']))
    audio['\xa9ART'] = html.unescape(str(json_data['primary_artists']))
    audio['\xa9alb'] = html.unescape(str(json_data['album']))
    audio['aART'] = html.unescape(str(json_data['singers']))
    audio['\xa9wrt'] = html.unescape(str(json_data['music']))
    audio['desc'] = html.unescape(str(json_data['starring']))
    audio['\xa9gen'] = html.unescape(str(json_data['label']))
    audio['\xa9day'] = html.unescape(str(json_data['year']))

    cover_url = str(json_data['image']).replace('-150x150.jpg', '-500x500.jpg')
    fd = urllib.request.urlopen(cover_url)
    cover = MP4Cover(fd.read(), getattr(MP4Cover, 'FORMAT_PNG' if cover_url.endswith('png') else 'FORMAT_JPEG'))
    fd.close()
    audio['covr'] = [cover]

    audio.save()


def downloadSong(song_info, log_file, download_dir, test=0):
    keys = {}

    dec_url = saavnAPI.decrypt_url(song_info['more_info']['encrypted_media_url'], test=test)
    filename = song_info['title'] + '.m4a'
    filename = re.sub(r'[?*<>|/\\":]', '', filename)

    location = os.path.join(download_dir, filename)

    raw_data = requests.get(dec_url, stream=True, headers=headers)
    with open(location, "wb") as raw_song:
        for chunk in raw_data.iter_content(chunk_size=2048):
            if chunk:
                raw_song.write(chunk)

    keys["song"] = song_info["title"]
    keys["primary_artists"] = song_info["more_info"]["artistMap"]["primary_artists"][0]["name"]
    keys["album"] = song_info["more_info"]["album"]
    keys["singers"] = ", ".join(
        [artist["name"] for artist in song_info["more_info"]["artistMap"]["primary_artists"]])
    keys["music"] = song_info["more_info"]["music"]
    keys["starring"] = ""
    keys['year'] = song_info['year']
    keys["label"] = song_info["more_info"]["label"]
    keys['image'] = song_info['image']

    fix(keys)
    return location, keys


def fix(song_info):
    song_info["album"] = tools.removeGibberish(song_info["album"]).strip()

    oldArtist = song_info["primary_artists"]
    newArtist = tools.removeGibberish(oldArtist)
    newArtist = tools.divideBySColon(newArtist)
    newArtist = tools.removeTrailingExtras(newArtist)
    song_info["primary_artists"] = tools.removeDup(newArtist)

    old_composer = song_info["music"]
    new_composer = tools.removeGibberish(old_composer)
    new_composer = tools.divideBySColon(new_composer)
    new_composer = tools.removeTrailingExtras(new_composer)
    song_info["music"] = tools.removeDup(new_composer)

    song_info['song'] = tools.removeGibberish(song_info['song'])

    # albumName.start(tags, song_info)
    # artistName.start(tags, song_info)
    # composerName.start(tags, song_info)
    # songTitle.start(tags, song_info)


def start(download_dir, url, log_file, test=0):
    songs_json = saavnAPI.start(url, log_file, test=test)

    all_types = {
        'artist': 'topSongs',
        'song': 'songs',
        'album': 'list',
        'featured': 'list'
    }
    url_type = url.split('/')[3]

    for song_info in songs_json[all_types[url_type]]:
        # print(song_info)

        # for testing
        if test:
            with open('song.txt', 'w+') as ab:
                json.dump(song_info, ab, indent=4)

        location, keys = downloadSong(song_info, download_dir, log_file, test=test)
        addtags(location, keys, log_file, test=test)
