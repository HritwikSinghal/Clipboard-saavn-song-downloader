import argparse
import logging
import os
import traceback

if os.path.isfile('test_bit'):
    os.environ["DEBUG"] = "1"

from src.saavn_downloader import SaavnDownloader

# --------------------------------------------------------------------------------------------------- #
# Dont use _LOGGER = logging.getLogger(__name__) in root module, it will not work.
# See https://stackoverflow.com/questions/47608069/python-logging-multiple-modules
_LOGGER = logging.getLogger()
_LOGGER.setLevel(logging.DEBUG)

_FORMATTER = logging.Formatter(
    '%(asctime)s : [%(levelname)s] :  %(name)s : (%(filename)s).%(funcName)s(%(lineno)d) : %(message)s'
)

# Print all Log messages to file for debugging
_FILE_HANDLER = logging.FileHandler('saavn_downloader.log')
_FILE_HANDLER.setLevel(logging.DEBUG)
_FILE_HANDLER.setFormatter(_FORMATTER)

# Print only Log messages upper than warning to output since we dont want user to see debug messages
_STREAM_HANDLER = logging.StreamHandler()
_STREAM_HANDLER.setLevel(logging.WARNING)
_STREAM_HANDLER.setFormatter(_FORMATTER)

_LOGGER.addHandler(_FILE_HANDLER)
_LOGGER.addHandler(_STREAM_HANDLER)

# --------------------------------------------------------------------------------------------------- #

test_bit = int(os.environ.get('DEBUG', default='0'))


def down_from_file(download_dir: str, file_name: str) -> None:
    if os.path.isfile(file_name):
        print(f'Found {file_name}, downloading songs from it first....')
        with open(file_name, 'r+') as song_file:
            song_url_list = [str(x).strip() for x in song_file.readlines() if str(x).strip()]
            my_downloader = SaavnDownloader(download_dir)

            for song_url in song_url_list:
                try:
                    my_downloader.url = song_url
                    my_downloader.run()
                except:
                    _LOGGER.warning(traceback.format_exc())
                    continue

            print('Song download from file complete, renaming file and moving to clipboard download...')


def start(test=0):
    # Check for download dir
    download_dir = os.path.expanduser("~/Downloads/Music")
    if not os.path.isdir(download_dir):
        os.mkdir(download_dir)
    print("Songs will be Downloaded to: ", download_dir)

    # Check if a file containing song links is provided
    parser = argparse.ArgumentParser(description='File containing links')
    parser.add_argument('-f', '--file', type=str, help="absolute path of File containing links", required=False)
    args = parser.parse_args()

    if args.file:
        _LOGGER.info("Found Songs FIle = " + str(args.file))
        down_from_file(download_dir, args.file)

    # Proceed with usual
    try:
        while True:
            my_downloader = SaavnDownloader(download_dir)
            my_downloader.run()

    except Exception as e:
        _LOGGER.error(traceback.format_exc())
        print("\nExiting....")
        exit(0)


if __name__ == '__main__':
    _LOGGER.info('Logging Started')

    if test_bit == 1:
        _LOGGER.info('DEBUG mode ON')
        start()
    else:
        _LOGGER.info('DEBUG mode OFF')
        print("""\n

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
        \n""")

        print("""
                This program will Download songs from Jiosaavn based on the links you copy on your clipboard.
                Just run this program and copy links, it will download them in background.
                For more info, visit https://github.com/HritwikSinghal/Clipboard-saavn-song-downloader
        """)

        print("Starting Program....")
        start()

        print("""
                If there were errors while running this program, Please open an issue on github
                and upload log file named 'saavn-downloader.log' there.
            """)
        print('''
                Thank you for Using this program....
                By Hritwik
                https://github.com/HritwikSinghal
            ''')

        print("""

                ████████╗██╗░░██╗░█████╗░███╗░░██╗██╗░░██╗  ██╗░░░██╗░█████╗░██╗░░░██╗██╗
                ╚══██╔══╝██║░░██║██╔══██╗████╗░██║██║░██╔╝  ╚██╗░██╔╝██╔══██╗██║░░░██║██║
                ░░░██║░░░███████║███████║██╔██╗██║█████═╝░  ░╚████╔╝░██║░░██║██║░░░██║██║
                ░░░██║░░░██╔══██║██╔══██║██║╚████║██╔═██╗░  ░░╚██╔╝░░██║░░██║██║░░░██║╚═╝
                ░░░██║░░░██║░░██║██║░░██║██║░╚███║██║░╚██╗  ░░░██║░░░╚█████╔╝╚██████╔╝██╗
                ░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚═╝  ░░░╚═╝░░░░╚════╝░░╚═════╝░╚═╝
        """)
        _LOGGER.info('Logging End')

# Todo : fix gnome wayland bug
# todo: add colored text : https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
# todo: fix artists and add support for Podcasts (shows)
# todo: write tests
# todo: find about MITM attack and see song file in monuyadav for payload
# todo:
# todo:
