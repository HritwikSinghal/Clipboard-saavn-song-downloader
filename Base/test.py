import html
import json
import traceback
import urllib.request
import urllib.request

import requests
import urllib3.exceptions
from mutagen.mp4 import MP4
from mutagen.mp4 import MP4Cover

from .saavnAPI import decrypt_url

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# OLD
# def old_getAlbumId(url):
#     res = requests.get(url, headers=headers, data=[('bitrate', '320')])
#     id = re.findall(r'"album_id":"(.*?)"', res.text)
#     return id[0]
#
#
# def old_get_artist_playlist_song_id(url):
#     res = requests.get(url, headers=headers, data=[('bitrate', '320')])
#     id = re.findall(r'"id":"(.+?)"', res.text)
#     return id[1]

###########################################################################################

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
    'referer': 'https://www.jiosaavn.com/song/tere-naal/KD8zfAZpZFo',
    'origin': 'https://www.jiosaavn.com'
}

api_url = {
    'artist': 'https://www.jiosaavn.com/api.php?__call=webapi.get&token={0}&type=artist&p=&n_song=10&n_album=14&sub_type=&category=&sort_order=&includeMetaTags=0&ctx=web6dot0&api_version=4&',
    'album': 'https://www.jiosaavn.com/api.php?__call=webapi.get&token={0}&type=album&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0',
    'playlist': 'https://www.jiosaavn.com/api.php?__call=webapi.get&token={0}&type=playlist&p=1&n=20&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0',
    'song': 'https://www.jiosaavn.com/api.php?__call=webapi.get&token={0}&type=song&includeMetaTags=0&ctx=web6dot0&api_version=4&_format=json&_marker=0',
    'top_search_results': 'https://www.jiosaavn.com/api.php?__call=content.getTopSearches&ctx=web6dot0&api_version=4&_format=json&_marker=0'
}


###########################################################################################
def downloadSongs(songs_json, album_name='songs', artist_name='Non-Artist'):
    for song in songs_json['songs']:
        try:
            dec_url = decrypt_url(song['encrypted_media_url'])
            filename = song['song']
        except:
            traceback.print_exc()
        try:
            location = get_download_location(artist_name, album_name, filename)
            has_downloaded = start_download(filename, location, dec_url)
            if has_downloaded:
                try:
                    name = songs_json['name'] if ('name' in songs_json) else songs_json['listname']
                except:
                    name = ''
                try:
                    addtags(location, song, name)
                except Exception as e:
                    print("============== Error Adding Meta Data ==============")
                    print("Error : {0}".format(e))
                print('\n')
        except Exception as e:
            traceback.print_exc()


def addtags(filename, json_data, playlist_name):
    audio = MP4(filename)

    audio['\xa9nam'] = html.unescape(str(json_data['song']))
    audio['\xa9ART'] = html.unescape(str(json_data['primary_artists']))
    audio['\xa9alb'] = html.unescape(str(json_data['album']))
    audio['aART'] = html.unescape(str(json_data['singers']))
    audio['\xa9wrt'] = html.unescape(str(json_data['music']))
    audio['desc'] = html.unescape(str(json_data['starring']))
    audio['\xa9gen'] = html.unescape(str(playlist_name))

    # audio['cprt'] = track['copyright'].encode('utf-8')
    # audio['disk'] = [(1, 1)]
    # audio['trkn'] = [(int(track['track']), int(track['maxtracks']))]

    audio['\xa9day'] = html.unescape(str(json_data['year']))
    audio['cprt'] = html.unescape(str(json_data['label']))

    # if track['explicit']:
    #    audio['rtng'] = [(str(4))]

    cover_url = json_data['image'][:-11] + '500x500.jpg'
    fd = urllib.request.urlopen(cover_url)
    cover = MP4Cover(fd.read(), getattr(MP4Cover, 'FORMAT_PNG' if cover_url.endswith('png') else 'FORMAT_JPEG'))
    fd.close()
    audio['covr'] = [cover]
    audio.save()


###########################################################################################


def getId(url):
    id = str(url).split('/')[-1]
    return id


def getAlbumDetails(url):
    id = getId(url)
    url = api_url['album'].format(id)

    res = requests.get(url, headers=headers)
    data = json.loads(str(res.text).strip())

    with open('song.txt', 'w+') as ab:
        json.dump(data, ab, indent=2)


def getArtistDetails(url):
    id = getId(url)
    url = api_url['artist'].format(id)

    res = requests.get(url, headers=headers)
    data = json.loads(str(res.text).strip())

    with open('song.txt', 'w+') as ab:
        json.dump(data, ab, indent=2)


def getPlaylistDetails(url):
    id = getId(url)
    url = api_url['playlist'].format(id)

    res = requests.get(url, headers=headers)
    data = json.loads(str(res.text).strip())

    with open('song.txt', 'w+') as ab:
        json.dump(data, ab, indent=2)


def getSongDetails(url):
    id = getId(url)
    url = api_url['song'].format(id)
    res = requests.get(url, headers=headers)

    data = json.loads(str(res.text).strip())
    with open('song.txt', 'w+') as ab:
        json.dump(data, ab, indent=2)

    return data


############################################

def fixContent(data):
    # old
    # data = re.sub(r'<!DOCTYPE html>\s*<.*>?', '', data)
    # return data

    fixed_json = [x for x in data.splitlines() if x.strip().startswith('{')][0]
    return fixed_json


def test(url):
    res = requests.get(url, headers=headers)
    data = str(res.text).strip()

    try:
        data = json.loads(data)
    except:
        data = fixContent(data)
        data = json.loads(data)

    with open('song.txt', 'w+') as ab:
        json.dump(data, ab, indent=4)


def start():
# url = 'https://www.jiosaavn.com/song/meri-aashiqui/RV4pdS5obh4'
#
# if 'featured' in url:
#     url.replace('featured', 'playlist')
#
# type = url.split('/')[3]
# url = api_url[type].format(getId(url))
# test(url)
