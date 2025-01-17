import logging
import os
import re

_LOGGER = logging.getLogger(__name__)

test_bit = int(os.environ.get('DEBUG', default='0'))


class GeneralTools:
    def __init__(self):
        """Various tools i use on strings."""
        pass

    def remove_bitrate(self, old_name: str) -> str:
        """Remove bitrate if in string. bitrate should be enclosed by []
        :param old_name: str: string to perform operation
        :return: str: updated string
        """

        # old method
        # x = re.compile(r'\s*\[*(\d+(.*kbps|Kbps|KBPS|KBps))\]*')

        x = re.compile(r'''
        \s*-*\s*                            # for foo - bar
        \[*                                 # for foo [bar
        \d*\s*[kK][bB][pP][sS]         # for KBps or KBPS or kbps or Kbps
        \]*                                 # for foo bar]
        ''', re.VERBOSE)

        new_name: str = x.sub('', old_name)
        return new_name.strip()

    def remove_year(self, old_name: str) -> str:
        """ Removes year from str. The year should be enclosed by ()
        :param old_name: str: string to perform operation
        :return: str: updated string
        """

        new_name: str = re.sub(r'\s*\(\d*\)', '', old_name)
        return new_name.strip()

    def remove_gibberish(self, old_name: str) -> str:
        """ Removes gibberish from str like '&quot;' or '&*amp|' or ' - Single'
        :param old_name: str: string to perform operation
        :return: str: updated string
        """

        new_name: str = re.sub(r'&quot;|&*amp| - Single', '', old_name)
        return new_name.strip()

    def remove_trailing_extras(self, old_name: str) -> str:
        """ Removes trailing extras from str like ';;', '; ;' etc
        :param old_name: str: string to perform operation
        :return: str: updated string
        """

        new_name: str = re.sub(r';\s*;\s*', '; ', old_name)
        return new_name.strip()

    def divide_artists(self, old_name: str) -> str:
        """ Divides the string using '[&/,' and merge them using ';'
        :param old_name: str: string to perform operation
        :return: str: updated string
        """

        names_divided: str = re.sub(r'\s*[&/,]\s*', ';', old_name)
        return names_divided

    def remove_duplicates(self, old_name: str) -> str:
        """ Removes Duplicates from str. Will split the str using ';' and then check
        :param old_name: str: string to perform operation
        :return: str: updated string
        """

        new_name: list = old_name.split(';')
        new_name = list(map(str.strip, new_name))

        new_name = list(set(new_name))
        new_name.sort()
        new_name: str = ';'.join(new_name)

        return new_name
