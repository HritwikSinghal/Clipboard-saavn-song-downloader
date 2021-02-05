# Clipboard saavn song downloader

Download songs from Jiosaavn by simply copying the Url of Albums, playlists, songs or even
home page or any other page! to your clipboard.

Just run this program and copy Jiosaavn links (like ```https://www.jiosaavn.com/song/shayad-from-love-aaj-kal/GjIBdCt,UX8```)
to your clipboard, and it will start downloading them.
It will download 320 Kbps m4a of song and save it in ```$HOME/downloads/Music``` Directory.

You can also create a file named ```songs_list.txt``` which contains list of urls separated by newline, 
this program will download all the links from there first and then move to parsing URLs from clipboard.
It will also rename the ```songs_list.txt``` file to ```songs_list_done_randomNumber.txt``` 
to avoid re-downloading songs.
The file ```songs_list.txt``` should be in the same folder as ```clipboard-saavn-song-downloader.py```.

## Screenshots

### Songs

![songs](media/songs.gif)

### Albums
![albums](media/albums.gif)

### Playlists
![playlists](media/playlists.gif)

And more! 

## Installation:

### Clone this repository using
```sh
$ git clone --depth 1 -b master https://github.com/HritwikSinghal/Clipboard-saavn-song-downloader
```

### Enter the directory

```sh
$ cd Clipboard-saavn-song-downloader/
```

##### Now there are two methods of Installation, ```Method 1``` and ```Method 2``` . **Windows users should follow only ```Method 2```**. While Linux Users can follow either ```Method 1``` or ```Method 2``` 


### Method 1 (Easy Install, ONLY FOR LINUX)

1. Run ```chmod +x ./install_linux.sh``` to make shell script executable.

2. Now type ```saavn-downloader``` from terminal to run the program. (You can run this from any directory!)


### Method 2 (For Both Linux and Windows.)


#### Install all the requirements.

```sh
$ pip3 install -r requirements.txt
``` 

1. Upgrade requests using ```sudo pip3 install --upgrade requests```

2. install one of the copy/paste mechanisms:

    1. xsel utility.
	```
	sudo apt install xsel			# For debian based Distros
	sudo pacman -S xsel --noconfirm			# For Arch based Distros
	```

	2. xclip utility
	```
	sudo apt install xclip			# For Debian based Distros
	sudo pacman -S xclip --noconfirm			# For Arch based Distros
 	```
 	3. gtk Python module
	```
	pip3 install gtk
	```
 
    4. PyQt4 Python module
	```
	pip3 install PyQt4
	```

### Running the app

#### Linux Users: (If you followed Method 1, then you don't need this section. The steps to run are given there only)
```sh
$ python3 clipboard-saavn-song-downloader.py
```
or you can create a symbolic link to the script ```Start_linux.sh``` in your ```/usr/local/bin``` and type ```saavn-downloader``` from terminal to run the program. (You can run this from any directory!)

#### Windows Users:
```
Simply click on "Start_Widows" bat file.
```

**And start copying links to download.!***

**Note: This program is in early stages, so some bugs are expected. Open an issue on github if you find one.**