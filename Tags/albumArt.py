# method 1 link: https://stackoverflow.com/questions/42473832/embed-album-cover-to-mp3-with-mutagen-in-python-3
# method 2 link: https://stackoverflow.com/questions/42665036/python-mutagen-add-image-cover-doesnt-work

import os
import shutil
import traceback

import mutagen
import requests
from mutagen.id3 import APIC
from mutagen.id3 import ID3
from mutagen.id3 import TIT2

from Base import tools


def addAlbumArt(json_data, songNameWithPath):
    img_url = json_data['image_url'].strip()

    # Download AlbumArt
    response = requests.get(img_url, stream=True)
    with open('img.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

    print("Adding Album Art...")

    audio = ID3(songNameWithPath)
    with open('img.jpg', 'rb') as albumart:
        # method 1

        audio.delall("APIC")  # Delete every APIC tag (Cover art)
        audio['APIC'] = APIC(
            encoding=3,
            mime='image/jpeg',
            type=3, desc='Cover (Front)',
            data=albumart.read()
        )
        audio.save(v2_version=3)

        # if we use 'audio.save()', win explorer wont recognize albumArt
        # since it uses v2.3 tags and ID3 saves v2.4.

        # # method 2
        # audio.add(APIC(
        #     encoding=3,
        #     mime='image/jpeg',
        #     type=3,
        #     desc='Cover',
        #     data=albumart)
        # )
        # audio.add(TIT2(
        #     encoding=3,
        #     text='title')
        # )
        # audio.save(v2_version=3)

    print("Album Art Added.")
    os.remove('img.jpg')


def start(json_data, songDir, songNameWithPath):
    os.chdir(songDir)
    addAlbumArt(json_data, songNameWithPath)
