import os
import requests
from requests.exceptions import HTTPError

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

class Base:
    NESTQUANT_API_ENDPOINT = os.getenv("NESTQUANT_API_ENDPOINT")

    def __init__(self, api_key):
        self._api_key = api_key

    def _get(self, url: str):
        """ Interact with GET request """
        res = requests.get(url)
        if res.status_code != 200:
            raise HTTPError(f"HTTP error status code - {res.status_code}: {res.text}")
        return res
    
    def _delete(self, url: str):
        """ Interact with GET request """
        res = requests.delete(url)
        if res.status_code != 200:
            raise HTTPError(f"HTTP error status code - {res.status_code}: {res.text}")
        return res

    def _post(self, url: str, data: dict):
        """ Interact with GET request """
        res = requests.post(url, data=data)
        if res.status_code != 200:
            raise HTTPError(f"HTTP error status code - {res.status_code}: {res.text}")
        return res