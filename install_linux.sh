red=$'\e[1;31m'
grn=$'\e[1;32m'
yel=$'\e[1;33m'
blu=$'\e[1;34m'
mag=$'\e[1;35m'
cyn=$'\e[1;36m'
end=$'\e[0m'

# from https://stackoverflow.com/questions/4774054/reliable-way-for-a-bash-script-to-get-the-full-path-to-itself
SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
SCRIPT_PATH=$(dirname $(realpath -s $0))


printf "\n\n ${grn} Cloning Repo ${end} "
rm -rf ~/Clipboard-saavn-song-downloader/
git clone --depth 1 -b master https://github.com/HritwikSinghal/Clipboard-saavn-song-downloader ~/Clipboard-saavn-song-downloader
cd ~/Clipboard-saavn-song-downloader/
rm -rf .git/

printf "\n\n ${grn} Installing Requirements ${end} "
pip3 install -r requirements.txt

printf "\n\n ${grn} Upgrading requests ${end} "
sudo pip3 install --upgrade requests

printf "\n\n ${grn} Insatlling Xsel & Xclip ${end} "
sudo apt install xsel -y
sudo pacman -S xsel --noconfirm

sudo apt install xclip -y
sudo pacman -S xclip --noconfirm

sudo chmod +x ./Start_linux.sh

printf "\n ${grn} ------------------------------------------------- ${end} "
sudo ln -sf ${SCRIPTPATH}/Start_linux.sh /usr/local/bin/saavn-downloader
# We also need to create a soft link to "clipboard-saavn-song-downloader.py" in user's home dir since 
# the "Start_linux" will run in home dir by install script and "python3" in it will search for file in home dir.
sudo ln -sf ${SCRIPTPATH}/clipboard-saavn-song-downloader.py ~/clipboard-saavn-song-downloader.py

printf "\n All done. Just Type ${grn}saavn-downloader${end} from terminal to launch the program."