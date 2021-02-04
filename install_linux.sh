red=$'\e[1;31m'
grn=$'\e[1;32m'
yel=$'\e[1;33m'
blu=$'\e[1;34m'
mag=$'\e[1;35m'
cyn=$'\e[1;36m'
end=$'\e[0m'

printf "\n\n ${red} Installing Requirements ${end} "
pip3 install -r requirements.txt

printf "\n\n ${red} Upgrading requests ${end} "
sudo pip3 install --upgrade requests

printf "\n\n ${red} Insatlling Xsel & Xclip ${end} "
sudo apt install xsel -y
sudo pacman -S xsel --noconfirm

sudo apt install xclip -y
sudo pacman -S xclip --noconfirm

pip3 install gtk
pip3 install PyQt4

sudo chmod +x ./Start_linux.sh

printf "\n ${red} ------------------------------------------------- ${end} "
sudo ln -sf ./Start_linux.sh /usr/local/bin/saavn-downloader

printf "\n All done. Just Type ${grn}saavn-downloader${end} from terminal to launch the program."