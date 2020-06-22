import html
import json
import os
import urllib
import urllib.request
import urllib.request

import requests
from mutagen.mp4 import MP4
from mutagen.mp4 import MP4Cover

from Base import saavnAPI

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

    return location, keys


# def downloadSong(download_dir, log_file, song_info, test=0):
#     os.chdir(download_dir)
#     name = re.sub(r'[?*<>|/\\":]', '', song_info['title'])
#
#     name_with_path = os.path.join(download_dir, name + '.mp3')
#
#     # check if song name already exists in download folder
#     if os.path.isfile(name_with_path):
#         old_name_with_path = os.path.join(download_dir, name + '_OLD.mp3')
#
#         try:
#             os.rename(name_with_path, old_name_with_path)
#             print('Song already exists, renaming it to "' + name + '_OLD.mp3"')
#         except FileExistsError:
#             os.remove(old_name_with_path)
#             os.rename(name_with_path, old_name_with_path)
#
#     # Download Song
#     try:
#         dec_url = saavnAPI.decrypt_url(song_info['url'])
#
#         if dec_url is None:
#             return '-1'
#
#         print("Downloading '{0}'.....".format(name))
#
#         raw_data = requests.get(dec_url, stream=True, headers=headers)
#         with open(name_with_path, "wb") as raw_song:
#             for chunk in raw_data.iter_content(chunk_size=2048):
#                 # writing one chunk at a time to mp3 file
#                 if chunk:
#                     raw_song.write(chunk)
#
#         print("Song download successful.")
#         return name_with_path
#
#     except:
#         print("Song download failed...")
#         tools.writeAndPrintLog(log_file, "\nSong download failed...\n", test=test)
#
#         if os.path.isfile(name_with_path):
#             os.remove(name_with_path)
#
#         return '-1'


# addDateLenOrg.start(tags, song_info)
# albumName.start(tags, song_info)
# artistName.start(tags, song_info)
# composerName.start(tags, song_info)
# songTitle.start(tags, song_info)
# albumArt.start(song_info, download_dir, downloaded_song_name_with_path)


def start(download_dir, url, log_file, test=0):
    # list_of_songs_with_info = saavnAPI.start(url, log_file, test=test)
    songs_json = saavnAPI.start(url, log_file, test=test)

    url_type = url.split('/')[3]
    all_types = {
        'artist': 'topSongs',
        'song': 'songs',
        'album': 'list',
        'featured': 'list'
    }

    for song_info in songs_json[all_types[url_type]]:
        print(song_info)
        # for testing

        if test:
            with open('song.txt', 'w+') as ab:
                json.dump(song_info, ab, indent=4)

        location, keys = downloadSong(song_info, download_dir, log_file, test=test)

        print(location)
        print(keys)
        x = input()

        addtags(location, keys, log_file, test=test)
