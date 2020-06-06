# Clipboard saavn song downloader

This program is in early stages so it may download wrong song sometimes.

Just run this program and copy Jiosaavn links (like 'https://www.jiosaavn.com/album/bewafai/y3DlZsa6XD0_')
to your clipboard and it will start downloading them. It will dowload Albums, playlists, songs and even
home page or any other page songs!


Installation:

Clone this repository using
```sh
$ git clone https://github.com/HritwikSinghal/Clipboard-saavn-song-downloader
```
Enter the directory and install all the requirements using
```sh
$ pip3 install -r requirements.txt
```
NOTE: If you are on Linux: 

1. upgrade requests using ```sudo pip3 install --upgrade requests```

2. install one of the copy/paste mechanisms:

        sudo apt-get install xsel to install the xsel utility.
        sudo apt-get install xclip to install the xclip utility.
        pip install gtk to install the gtk Python module.
        pip install PyQt4 to install the PyQt4 Python module.


Run the app using
```sh
$ python3 Clipboard-saavn-song-downloader.py
```

and start copying links to download..!
