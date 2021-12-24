# Clipboard saavn song downloader

Download songs from Jiosaavn by simply copying the Url of Albums, playlists, songs or even home page or any other page!
to your clipboard.

Just run this program and copy Jiosaavn links (
like ```https://www.jiosaavn.com/song/shayad-from-love-aaj-kal/GjIBdCt,UX8```)
to your clipboard, and it will start downloading them. It will download 320 Kbps m4a of song and save it
in ```$HOME/downloads/Music``` Directory.

You can also create a file named ```songs_list.txt``` in home directory which contains list of urls separated by
newline, this program will download all the links from there first and then move to parsing URLs from clipboard. It will
also rename the ```songs_list.txt``` file to ```songs_list_done_randomNumber.txt```
to avoid re-downloading songs. Use ```--help``` for more info.

## Screenshots

### Songs

![songs](media/songs.gif)

### Albums

![albums](media/albums.gif)

### Playlists

![playlists](media/playlists.gif)

And more!

## Installation:

### Method 1 (Easy Install, only for debian and arch based distros)

#### Install the app

Those who want to get started quickly and conveniently may install using the following command

* Install ```curl``` before installing.

* ```curl -sSL https://raw.githubusercontent.com/HritwikSinghal/Clipboard-saavn-song-downloader/master/install_linux.sh | bash```

#### Run the app

Just run ```saavn-downloader``` from terminal to launch the program. (You can run this from any directory!)

### Method 2 (For Both Linux and Windows.)

1. #### Clone this repository and enter
    ```sh
    git clone --depth 1 -b master https://github.com/HritwikSinghal/Clipboard-saavn-song-downloader
    ```
    ```
    cd Clipboard-saavn-song-downloader/
    ```

2. #### Install all the requirements.

    ```sh
    pip3 install -r requirements.txt
    ``` 

    * Upgrade requests using ```pip3 install --upgrade requests```

    * install one of the copy/paste mechanisms:

        1. For X11, xclip utility
        ```
        sudo apt install xclip			                    # For Debian based Distros
        sudo pacman -S xclip --noconfirm --needed			# For Arch based Distros
         ```

        2. For NON-GNOME Wayland (KDE, sway), Install wl-clipboard
       ```
        sudo apt install wl-clipboard			                    # For debian based Distros
        sudo pacman -S wl-clipboard --noconfirm --needed			# For Arch based Distros
        ```

        3. For GNOME-Wayland (ubuntu and others), install gpaste
        ```
        sudo apt install gpaste			                    # For debian based Distros
        sudo pacman -S gpaste --noconfirm --needed			# For Arch based Distros
        ```

        4. Totally Optional xsel utility.
        ```
        sudo apt install xsel			                    # For debian based Distros
        sudo pacman -S xsel --noconfirm --needed			# For Arch based Distros
        ```

#### Running the app

- ##### Linux Users:

    - cd into the directory where the program is cloned
    - ```sh
      ./clipboard-saavn-song-downloader.py   
      ```
      or you can create a symbolic link to the script ```Start_linux.sh``` in your ```/usr/local/bin``` 
      and type ```saavn-downloader``` from terminal to run the program from any directory!

- ##### Windows Users:
  - ```
    Simply click on "Start_Widows" bat file.
    ```
    You can create this file's shortcut on desktop for easy access.

**And start copying links to download!.**

**Note: This program is in early stages, so some bugs are expected. Open an issue on Github if you find one.**

## License

[GPLv3](/LICENSE)