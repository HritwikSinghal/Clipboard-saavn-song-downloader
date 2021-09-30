import json
import logging
import os
import time
import traceback

import requests

_LOGGER = logging.getLogger(__name__)

test_bit = int(os.environ.get('DEBUG', default='0'))


def _pp_dict(json_dict: dict):
    print(json.dumps(json_dict, indent=4))


class SearX:
    """
    Class to search on SearX instances.
    Just call the function with 'search_query' and it will fetch them to you in json format.

    Returns a dict containing Results from SearX (in Json format)
    """

    def __init__(self):
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
            'Referer': 'searx.garudalinux.org/',
            'Origin': 'searx.garudalinux.org',
        }

        self._general_params = {
            'category_general': '1',
            'pageno': '1',
            'time_range': 'None',
            'language': 'en',
            'format': 'json'
        }

        self.searx_instances_base_url = {
            'garuda': 'https://searx.garudalinux.org/search',
        }

    def get_results(self, search_query: str) -> dict:
        """
        :param search_query: String to search on SearX
        :return: A dict containing Results from SearX in Json format
        """
        base_url = self.searx_instances_base_url['garuda']
        params = {
                     'q': search_query
                 } | self._general_params

        response = ''
        while response == '':
            try:
                response = requests.post(base_url, data=params, headers=self._headers, allow_redirects=True)
            except Exception as e:
                time.sleep(15)
                _LOGGER.warning(traceback.format_exc())
            # print(response.url)
            # self._pp_dict(response.json())

        return response.json()
