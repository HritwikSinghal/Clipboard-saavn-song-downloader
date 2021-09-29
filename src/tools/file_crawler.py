import os
import re


class File_Crawler:
    """
    Class to list all files in a directory.
    Will take
        "file_dir": directory that we want to crawl
        "recursive_flag": If true, will recursively crawl 'file_dir'
        "exclude_dirs": directories which we want to skip. Is a dict
    returns "file_list": List of absolute path of files in crawl folder (and sub-dirs). each entry is str
    """

    def __init__(self, file_dir: str = '', exclude_dirs: dict = None, recursive_crawl_flag: bool = False):
        """
        :param file_dir: Absolute path of Directory to crawl
        :param recursive_crawl_flag: If True, then crawls the directory recursively

        :param exclude_dirs:
                A dict of type {'dir_name': 'recursive_exclude_flag'} (where dir_name is relative)
                if recursive_exclude_flag is True, it will skip all sub-dirs of 'dir_name' including files in 'dir_name'
                otherwise it will skip files only in 'dir_name' but will search for files in its sub-dirs.
        """

        self._file_dir: str = file_dir
        self.recursive_flag = recursive_crawl_flag
        self._exclude_dirs: dict = exclude_dirs

        self._init_func()

    def _init_func(self):
        """
        This will call some methods on class initialization
        :return:
        """
        self._set_file_dir()

    def _set_file_dir(self):
        """
        Sets 'self._file_dir' to directory path
        """

        while not self._file_dir:
            input_dir = input("Enter folder from where to crawl:  ")

            if not os.path.isdir(input_dir):
                print("No such folder exists, Please enter folder path again...")
            else:
                self._file_dir = input_dir
        print("folder to crawl: ", self._file_dir)

    def _get_file_list(self, folder_name: str):
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
        all_file_list = [
            file
            for file in os.listdir(folder_name)
            if os.path.isfile(os.path.join(folder_name, file))
        ]

        file_list = []

        # Todo : remove hard code
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

        # return sorted
        return sorted(file_list)

    def get_files(self):

        file_list = []
        if not self.recursive_flag:
            file_list.extend(self._get_file_list(self._file_dir))
        else:
            print("Doing recursive search...")
            print("Walking down ", self._file_dir, "\b...\n")
            for (curr_dir, sub_dirs, files) in os.walk(self._file_dir, topdown=True):
                file_list.extend(self._get_file_list(curr_dir))

        return file_list
