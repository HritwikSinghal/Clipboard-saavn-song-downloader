import os
import re
import traceback


class GeneralTools:
    pass


# ----------------------------------------------#


def removeBitrate(oldName):
    # old method
    # x = re.compile(r'\s*\[*(\d+(.*kbps|Kbps|KBPS|KBps))\]*')

    x = re.compile(r'''
    \s*-*\s*                            # for foo - bar
    \[*                                 # for foo [bar
    \d*\s*[kK][bB][pP][sS]         # for KBps or KBPS or kbps or Kbps
    \]*                                 # for foo bar]
    ''', re.VERBOSE)

    newName = x.sub('', oldName)
    return newName.strip()


def removeYear(oldName):
    newName = re.sub(r'\s*\(\d*\)', '', oldName)
    return newName.strip()


def removeGibberish(oldName):
    newName = re.sub(r'&quot;|&*amp| - Single', '', oldName)
    return newName.strip()


def removeTrailingExtras(oldName):
    newName = re.sub(r';\s*;\s*', '; ', oldName)
    return newName.strip()


def divideBySColon(oldName):
    namesDivided = re.sub(r'\s*[&/,]\s*', ';', oldName)
    return namesDivided


def removeDup(old_name):
    new_name = old_name.split(';')
    new_name = map(str.strip, new_name)

    new_name = list(set(new_name))
    new_name.sort()
    new_name = ';'.join(new_name)

    return new_name


# ---------------------------------------------#

def writeAndPrintLog(log_file, line, test=0):
    log_file.write(line)
    traceback.print_exc(file=log_file)
    if test:
        traceback.print_exc()


def getLogFile(song_dir):
    os.chdir(song_dir)
    log_file = open('Clipboard-saavn-song-downloader_LOGS.txt', 'a')
    return log_file


def createLogFile(song_dir):
    os.chdir(song_dir)
    with open('Clipboard-saavn-song-downloader_LOGS.txt', 'w+') as log_file:
        log_file.write("This is log file for Clipboard-saavn-song-downloader. SongDir = " + song_dir + "\n\n")

    return getLogFile(song_dir)
