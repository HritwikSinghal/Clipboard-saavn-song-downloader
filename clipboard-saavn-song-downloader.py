import os

from Base import main, saavnAPI, DownloadSong


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

# start(test=test)

# DownloadSong.start('/home/hritwik/Videos', 'https://www.jiosaavn.com/song/tum-hi-ho/EToxUyFpcwQ', 'x', test=test)
DownloadSong.start('/home/hritwik/Videos', 'https://www.jiosaavn.com/album/aashiqui-2/-iNdCmFNV9o_', 'x', test=test)
# DownloadSong.start('/home/hritwik/Videos', 'https://www.jiosaavn.com/featured/monday-mania---hindi/tjgzzaeg32xuOxiEGmm6lQ__', 'x', test=test)
# DownloadSong.start('/home/hritwik/Videos', 'https://www.jiosaavn.com/artist/arijit-singh-/LlRWpHzy3Hk_', 'x', test=test)

# todo: use https instead of http in decrypt_url in saavnApi
# todo: update lyrics function in saavnApi
# todo: find about MITM attack and see song file in monuyadav for payload
# todo:
