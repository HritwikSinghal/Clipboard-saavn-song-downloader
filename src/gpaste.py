import ctypes
import os
import subprocess
import time

import pyperclip

ENCODING = 'utf-8'


# Exceptions
class PyperclipException(RuntimeError):
    pass


class PyperclipTimeoutException(PyperclipException):
    pass


class PyperclipWindowsException(PyperclipException):
    def __init__(self, message):
        message += " (%s)" % ctypes.WinError()
        super(PyperclipWindowsException, self).__init__(message)


def _stringifyText(text):
    acceptedTypes = (str, int, float, bool)
    if not isinstance(text, acceptedTypes):
        raise PyperclipException(
            f'only str, int, float, and bool values can be copied to the clipboard, not {text.__class__.__name__}')
    return str(text)


copy, paste = pyperclip.copy, pyperclip.paste


# ------------------------------------------------------------------------------------------- #

def start_client_gpaste():
    args = ['gpaste-client daemon-reexec & exit']
    result = subprocess.run(args, capture_output=True, text=True, shell=True)
    args = ["gpaste-client start & exit"]
    result = subprocess.run(args, capture_output=True, text=True, shell=True)


def copy_gpaste(text):
    text = _stringifyText(text)  # Converts non-str values to str.
    args = ["gpaste-client"]
    if not text:
        args.append('delete-history')
        subprocess.check_call(args, close_fds=True)
    else:
        args.append('add')
        p = subprocess.Popen(args, stdin=subprocess.PIPE, close_fds=True)
        p.communicate(input=text.encode(ENCODING))


def paste_gpaste():
    args = ["gpaste-client history --raw & exit"]
    result = subprocess.run(args, capture_output=True, text=True, shell=True)
    while True:
        try:
            last_item_in_history = [str(x).strip() for x in result.stdout.splitlines()][0]
        except IndexError:
            pyperclip.copy("temp_str")
            # if the clipboard history is empty
            continue
        else:
            return last_item_in_history


# ------------------------------------------------------------------------------------------- #


def waitForPaste(not_str: str, timeout=None):
    """This function call blocks until a non-empty text string exists on the
        clipboard. It returns this text.

        This function raises PyperclipTimeoutException if timeout was set to
        a number of seconds that has elapsed without non-empty text being put on
        the clipboard."""
    startTime = time.time()
    while True:
        clipboardText = paste()
        if clipboardText != not_str:
            # print(clipboardText)
            return clipboardText
        time.sleep(0.01)

        if timeout is not None and time.time() > startTime + timeout:
            raise PyperclipTimeoutException('waitForPaste() timed out after ' + str(timeout) + ' seconds.')


def set_clipboard():
    global copy, paste
    if 'gnome' in os.getenv('XDG_CURRENT_DESKTOP').lower() and os.getenv('XDG_SESSION_TYPE') == 'wayland':
        copy = copy_gpaste
        paste = paste_gpaste

        start_client_gpaste()
    else:
        copy = pyperclip.copy
        paste = pyperclip.paste


set_clipboard()
