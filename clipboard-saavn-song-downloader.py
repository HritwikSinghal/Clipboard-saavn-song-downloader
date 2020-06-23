import os

from Base import main


def start(test=0):
    if test:
        main.start(test=1)
    else:
        print("""
            This program will Download songs from Jiosaavn based on the links you copy on your clipboard. 
            Just run this program and copy links, it will download them in background.
            For more info, visit https://github.com/HritwikSinghal/Clipboard-saavn-song-downloader
        """)

        print("Starting Program....")
        main.start(test)

        print("""
                If there were errors during running this program, please upload log file
                named 'Clipboard-saavn-song-downloader_LOGS.txt' in each dir and open an issue on github
                you can find those log files by using default search in folders or by manually
                finding each.
            """)
        print('''
                Thank you for Using this program....
                By Hritwik
                https://github.com/HritwikSinghal
            ''')


if os.path.isfile('Base/test_bit.py'):
    test = 1
else:
    test = 0

start(test=test)

# todo: add log support
# todo: update lyrics function in saavnApi
# todo: find about MITM attack and see song file in monuyadav for payload
# todo:
