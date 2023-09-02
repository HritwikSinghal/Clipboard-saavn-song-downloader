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

# if running as root user then set current user as sudo user
if [ "$EUID" -ne 0 ]
then
    export $USER=$SUDO_USER
    export $HOME=USER_HOME=$(getent passwd $SUDO_USER | cut -d: -f6)
fi

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
－ Ｂｙ Ｈｒｉｔｗｉｋ Ｓｉｎｇｈａｌ

"

printf "\n\n ${grn} Installing git, python3, pipenv ${end} "
if has_command apt; then
  apt update -y
  apt install git python3 python3-pip pipenv -y
elif has_command pacman; then
  pacman -S git python3 python-pip python-pipenv --noconfirm --needed
fi

python3 -m keyring --disable

printf "\n\n ${grn} Cloning Repo ${end} "
cd $HOME || exit
rm -rf $HOME/Clipboard-saavn-song-downloader/
git clone --depth 1 -b master https://github.com/HritwikSinghal/Clipboard-saavn-song-downloader $HOME/Clipboard-saavn-song-downloader/
cd $HOME/Clipboard-saavn-song-downloader/ || exit
rm -rf .git/ .gitignore
chown -R $USER:$USER ./* .

printf "\n\n ${grn} Installing xclip, gpaste ${end} "
if has_command apt; then
  apt install xclip gpaste -y
elif has_command pacman; then
  pacman -S xclip gpaste --noconfirm --needed
fi

#printf "\n\n ${grn} Installing Xsel, Xclip, wl-clipboard, gpaste ${end} "
#if has_command apt; then
#  apt install xsel xclip wl-clipboard gpaste -y
#elif has_command pacman; then
#  pacman -S xsel xclip wl-clipboard gpaste --noconfirm --needed
#fi

printf "\n\n ${grn} Installing pyenv ${end} "
if ! has_command pyenv; then
    if has_command apt; then
        curl https://pyenv.run | bash
        export PYENV_ROOT="$HOME/.pyenv"
        command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
        eval "$(pyenv init -)"
        eval "$(pyenv virtualenv-init -)"
    elif has_command pacman; then
      pacman -S pyenv --noconfirm --needed
    fi
fi

printf "\n ${grn} ------------------------------------------------- ${end} "
cd $HOME/Clipboard-saavn-song-downloader/ || exit
chmod +x ./clipboard-saavn-song-downloader.py || exit
echo "cd $HOME/Clipboard-saavn-song-downloader/" > /usr/local/bin/saavn-downloader
echo "pipenv install" >> /usr/local/bin/saavn-downloader
echo "pipenv run ./clipboard-saavn-song-downloader.py" >> /usr/local/bin/saavn-downloader
chmod +x /usr/local/bin/saavn-downloader
#ln -sf $HOME/Clipboard-saavn-song-downloader/clipboard-saavn-song-downloader.py /usr/local/bin/saavn-downloader

echo -e "


  ██████╗░░█████╗░███╗░░██╗███████╗
  ██╔══██╗██╔══██╗████╗░██║██╔════╝
  ██║░░██║██║░░██║██╔██╗██║█████╗░░
  ██║░░██║██║░░██║██║╚████║██╔══╝░░
  ██████╔╝╚█████╔╝██║░╚███║███████╗
  ╚═════╝░░╚════╝░╚═╝░░╚══╝╚══════╝

"

printf "\n\n All done. Just Type ${grn}saavn-downloader${end} from terminal to launch the program.\n\n"
