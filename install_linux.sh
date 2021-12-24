#!/usr/bin/env bash

trap "exit" INT
red=$'\e[1;31m'
grn=$'\e[1;32m'
yel=$'\e[1;33m'
blu=$'\e[1;34m'
mag=$'\e[1;35m'
cyn=$'\e[1;36m'
end=$'\e[0m'

# from https://stackoverflow.com/questions/4774054/reliable-way-for-a-bash-script-to-get-the-full-path-to-itself
SCRIPTPATH="$(
  cd "$(dirname "$0")" >/dev/null 2>&1
  pwd -P
)"
SCRIPT_PATH=$(dirname $(realpath -s $0))

# Check command availability
function has_command() {
  command -v $1 >/dev/null
}

echo -e "


			░██████╗░█████╗░░█████╗░██╗░░░██╗███╗░░██╗  ░██████╗░█████╗░███╗░░██╗░██████╗░
			██╔════╝██╔══██╗██╔══██╗██║░░░██║████╗░██║  ██╔════╝██╔══██╗████╗░██║██╔════╝░
			╚█████╗░███████║███████║╚██╗░██╔╝██╔██╗██║  ╚█████╗░██║░░██║██╔██╗██║██║░░██╗░
			░╚═══██╗██╔══██║██╔══██║░╚████╔╝░██║╚████║  ░╚═══██╗██║░░██║██║╚████║██║░░╚██╗
			██████╔╝██║░░██║██║░░██║░░╚██╔╝░░██║░╚███║  ██████╔╝╚█████╔╝██║░╚███║╚██████╔╝
			╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚══╝  ╚═════╝░░╚════╝░╚═╝░░╚══╝░╚═════╝░

			██████╗░░█████╗░░██╗░░░░░░░██╗███╗░░██╗██╗░░░░░░█████╗░░█████╗░██████╗░███████╗██████╗░
			██╔══██╗██╔══██╗░██║░░██╗░░██║████╗░██║██║░░░░░██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
			██║░░██║██║░░██║░╚██╗████╗██╔╝██╔██╗██║██║░░░░░██║░░██║███████║██║░░██║█████╗░░██████╔╝
			██║░░██║██║░░██║░░████╔═████║░██║╚████║██║░░░░░██║░░██║██╔══██║██║░░██║██╔══╝░░██╔══██╗
			██████╔╝╚█████╔╝░░╚██╔╝░╚██╔╝░██║░╚███║███████╗╚█████╔╝██║░░██║██████╔╝███████╗██║░░██║
			╚═════╝░░╚════╝░░░░╚═╝░░░╚═╝░░╚═╝░░╚══╝╚══════╝░╚════╝░╚═╝░░╚═╝╚═════╝░╚══════╝╚═╝░░╚═╝

"

echo -e "
			－ Ｂｙ Ｈｒｉｔｗｉｋ Ｓｉｎｇｈａｌ
"

printf "\n\n ${grn} Installing git, python3 ${end} "
sudo apt-get install git python3 -y
sudo pacman -S git python3 --noconfirm --needed
python3 -m keyring --disable

printf "\n\n ${grn} Cloning Repo ${end} "
rm -rf ~/Clipboard-saavn-song-downloader/
git clone --depth 1 -b master https://github.com/HritwikSinghal/Clipboard-saavn-song-downloader ~/Clipboard-saavn-song-downloader/
cd ~/Clipboard-saavn-song-downloader/ || exit
rm -rf .git/

printf "\n\n ${grn} Installing Python and pip3 ${end} "
sudo apt-get install python3-pip -y
sudo pacman -S python-pip --noconfirm --needed

printf "\n\n ${grn} Installing Requirements ${end} "
cd ~/Clipboard-saavn-song-downloader/ || exit
pip3 install -r ./requirements.txt

printf "\n\n ${grn} Upgrading requests ${end} "
sudo pip3 install --upgrade requests
pip3 install --upgrade requests

printf "\n\n ${grn} Insatlling Xsel, Xclip, wl-clipboard, gpaste ${end} "
if has_command apt-get; then
  sudo apt-get install xsel xclip wl-clipboard gpaste -y
elif has_command pacman; then
  sudo pacman -S xsel xclip wl-clipboard gpaste --noconfirm --needed
fi

printf "\n ${grn} ------------------------------------------------- ${end} "
cd ~/Clipboard-saavn-song-downloader/ || exit
#echo "#!/usr/bin/env bash" > ~/Clipboard-saavn-song-downloader/start_linux.sh
#echo "\n" >> ~/Clipboard-saavn-song-downloader/start_linux.sh
#echo "python3 ~/Clipboard-saavn-song-downloader/clipboard-saavn-song-downloader.py" >> ~/Clipboard-saavn-song-downloader/start_linux.sh
sudo chmod +x ./clipboard-saavn-song-downloader.py || exit
sudo ln -sf ~/Clipboard-saavn-song-downloader/clipboard-saavn-song-downloader.py /usr/local/bin/saavn-downloader

echo -e "


			██████╗░░█████╗░███╗░░██╗███████╗
			██╔══██╗██╔══██╗████╗░██║██╔════╝
			██║░░██║██║░░██║██╔██╗██║█████╗░░
			██║░░██║██║░░██║██║╚████║██╔══╝░░
			██████╔╝╚█████╔╝██║░╚███║███████╗
			╚═════╝░░╚════╝░╚═╝░░╚══╝╚══════╝

"

printf "\n\n All done. Just Type ${grn}saavn-downloader${end} from terminal to launch the program.\n\n"
