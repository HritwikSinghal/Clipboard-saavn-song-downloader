# Clipboard saavn song downloader

Download songs from Jiosaavn by simply copying the Url of Albums, playlists, songs or even
home page or any other page! to your clipboard.

Just run this program and copy Jiosaavn links (like ```https://www.jiosaavn.com/song/shayad-from-love-aaj-kal/GjIBdCt,UX8```)
to your clipboard, and it will start downloading them.
It will download 320 Kbps m4a of song and save it in ```$HOME/downloads/Music``` Directory.

If you have a file named ```songs_list.txt``` which contains list of urls separated by newline, 
this program will download all of them first and then move to parsing URLs from clipboard.
It will also rename the ```songs_list.txt``` file to ```songs_list_done_randomNumber.txt``` 
to avoid re-downloading songs.
The file ```songs_list.txt``` should be in the same folder as ```clipboard-saavn-song-downloader.py```.

## Installation:

### Clone this repository using
```sh
$ git clone https://github.com/HritwikSinghal/Clipboard-saavn-song-downloader
```

### Enter the directory and install all the requirements using
```sh
$ pip3 install -r requirements.txt
```
**NOTE: If you are on Linux:** 

1. Upgrade requests using ```sudo pip3 install --upgrade requests```

2. install one of the copy/paste mechanisms:

    1. xsel utility.
	```
	sudo apt install xsel			# For debian based Distros
	sudo pacman -S xsel			# For Arch based Distros
	```

	2. xclip utility
	```
	sudo apt install xclip			# For Debian based Distros
	sudo pacman -S xclip			# For Arch based Distros
 	```
 	3. gtk Python module
	```
	pip install gtk
	```
 
    4. PyQt4 Python module
	```
	pip install PyQt4
	```

### Running the app:

#### Linux & macOS:
```sh
$ python3 clipboard-saavn-song-downloader.py
```

#### Windows:
```sh
- Simply click on "Start_Widows" bat file.
```

**And start copying links to download.!***


**Note: This program is in early stages, so some bugs are expected. Open an issue on github if you find one.**