import os

from Base import main


def start(test=0):
    if test:
        main.start(1)
    else:
        print("""
            This program will Download songs from Jiosaavn based on the links you copy on your clipboard. 
            Just run this program and copy links, it will download them in background.
            For more info, visit https://github.com/HritwikSinghal/Clipboard-saavn-song-downloader
        """)

        print('''
            Warning: This program is in early stages so it may download wrong song sometimes.
                        Enter 1 TO RUN OR 0 TO EXIT
        ''')

        x = input()

        if x == '1':
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
        else:
            print("Exiting....")
            exit(0)


if os.path.isfile('Base/test_bit.py'):
    test = 1
else:
    test = 0

start(test=test)
