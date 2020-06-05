from Base import tools
import traceback


def fixAlbum(tags, date, album_name):
    if date != '':
        newAlbumName = album_name + ' (' + date + ')'
    else:
        newAlbumName = album_name

    tools.saveTags('album', newAlbumName, tags)


def start(tags, json_data):
    try:
        if json_data['actual_album'] != '':
            album_name = json_data['actual_album']
        else:
            album_name = json_data['album']
    except KeyError:
        album_name = json_data['album']

    date = json_data['date']
    fixAlbum(tags, date, album_name)
