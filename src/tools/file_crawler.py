import logging
import os
import re

_LOGGER = logging.getLogger(__name__)

test_bit = os.environ.get('DEBUG', default='0')


def _check_file_dir(file_dir: str) -> None:
    """
    check if file_dir is valid path or not
    """

    if not os.path.isdir(file_dir):
        _LOGGER.error("No such folder exists, Please enter folder path again...")
        raise NotADirectoryError

    print("folder to crawl: ", file_dir)


class File_Crawler:
    """
    Class to list all files in a directory.
    Will take
        "file_dir": directory that we want to crawl
        "recursive_flag": If true, will recursively crawl 'file_dir'
        "exclude_dirs": directories which we want to skip. Is a dict
    returns "file_list": List of absolute path of files in crawl folder (and sub-dirs). each entry is str
    """

    def __init__(self):
        self._exclude_dirs: dict = {}

    def _get_file_list(self, folder_name: str) -> list:
        """
        :param folder_name: str : Folder name where files are stored, absolute path
        :return file_list : list : List of files in that folder,
                stores a tuple = (absolute path of file's folder : str, name of file : str, downloaded: bool)
        """

        """
        _exclude_dirs is a dict of type {'dir_name': 'recursive_flag'}
        where dir_name is relative
        if recursive_flag is True, it will also skip all sub-dirs of 'dir_name' 
            otherwise it will skip files only in 'dir_name' but will search for files in its sub-dirs
        """

        # Skip the excluded directories
        for (ex_dir, rec_flag) in self._exclude_dirs.items():
            if rec_flag == '1':
                if str(ex_dir) in folder_name:
                    print("Rec Skipping files in ", folder_name)
                    return []
            else:
                if str(folder_name).endswith(ex_dir):
                    print("Skipping files in ", folder_name)
                    return []

        print('Now in ', folder_name)
        # all_file_list = [
        #     file
        #     for file in os.listdir(folder_name)
        #     if os.path.isfile(os.path.join(folder_name, file))
        # ]

        # List all files in that dir
        all_file_list = []
        for (dirpath, dirnames, filenames) in os.walk(folder_name):
            all_file_list.extend(filenames)
            break

        file_list = []

        # Todo : remove hard code, take input from user which file types to return
        for file in all_file_list:
            x = re.findall(
                r'(.+\.[mM][pP]4)|'
                r'(.+\.[mM][kK][vV])|'
                r'(.+\.[wW][eE][bB][mM])',
                file
            )

            """
            x is a list which contains a tuple with 3 values with 2 values empty.
            so x can be
             [('', '', 'foobar.webm')] --> case of webm, or  
             [('', 'foobar.mkv', '')] --> case of mkv, or  
             [('foobar.mp4', '', '')] --> case of mp4
            """

            if len(x) != 0:
                for file_name in range(len(x[0])):
                    if os.path.isfile(os.path.join(folder_name, x[0][file_name])):
                        file_list.append(os.path.join(folder_name, x[0][file_name]))

        # Todo: test what is returned
        # return sorted
        return sorted(file_list)

    def get_files(self, file_dir: str, exclude_dirs: dict = None, recursive_crawl_flag: bool = False) -> list:
        """
        :param file_dir: str: Absolute path of Directory to crawl
        :param recursive_crawl_flag: bool: If True, then crawls the directory recursively

        :param exclude_dirs: dict:
                A dict of type {'dir_name': 'recursive_exclude_flag'} (where dir_name is relative)
                if recursive_exclude_flag is True, it will skip all sub-dirs of 'dir_name' including files in 'dir_name'
                otherwise it will skip files only in 'dir_name' but will search for files in its sub-dirs.
        :return: list: List of files in the file_dir,
                stores a tuple = (absolute path of file's folder : str, name of file : str, downloaded: bool)
        """

        self._exclude_dirs: dict = exclude_dirs
        _check_file_dir(file_dir)

        file_list: list = []
        if not recursive_crawl_flag:
            file_list.extend(self._get_file_list(file_dir))
        else:
            print("Doing recursive search...")
            print("Walking down ", file_dir, "\b...\n")
            for (curr_dir, sub_dirs, files) in os.walk(file_dir, topdown=True):
                file_list.extend(self._get_file_list(curr_dir))

        return file_list
