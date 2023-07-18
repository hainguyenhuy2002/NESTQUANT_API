import os
import requests

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import zipfile, io
from src.base import Base

class Crawler(Base):
    def __init__(self, api_key):
        super().__init__(api_key=api_key)
        self._get_download_link_url = Crawler.NESTQUANT_API_ENDPOINT + 'data/api/download_link?category=%s&symbol=%s&api_key=' + self._api_key
        self._get_lastest_data_url = Crawler.NESTQUANT_API_ENDPOINT + 'data/api/lastest?category=%s&symbol=%s&api_key=' + self._api_key
    
    def _check_location(self, location: str):
        """ Verify the presence of a folder and create it if it is absent. """
        try:
            os.makedirs(location)
        except FileExistsError:
            print(f"Folder '{location}' already exists")
    
    def _get_data_response(
        self,
        category: str,
        symbol: str,
        get_historical_data: bool
    ) -> requests.Response:
        """ 
            Retrieve the data response by generating the URL for the query procedure.

            Parameters
            -----------
                category: str,
                    data category
                symbol: str,
                    data symbol, be careful that the symbol is case sensitive
                get_historical_data: bool
                    if the value is True, retrieve the historical data in a compressed zip format
                    if the value is False, return the 10 most recent data entries.

            Returns
            ----------
                a Response object
        """
        if get_historical_data:
            download_link = self._get_download_link_url % (category, symbol)
            url = self._get(download_link).text[1:-1]
        else:
            url = self._get_lastest_data_url % (category, symbol)
        return self._get(url)

    def download_historical_data(
        self,
        category: str,
        symbol: str,
        location: str
    ):
        """ 
            Download and extract the historical data, then save it to the specified 'location'.

            Parameters
            -----------
                category: str,
                    data category
                symbol: str,
                    data symbol, be careful that the symbol is case sensitive
                location: str
                    the destination where the data should be saved.
        """
        data_response = self._get_data_response(category, symbol, get_historical_data=True)
        location = os.path.join(location, data_response.headers['content-disposition'].split(';')[1].split('=')[1].split('.')[0])
        self._check_location(location)
        z = zipfile.ZipFile(io.BytesIO(data_response.content))
        z.extractall(location)

    def get_lastest_data(
        self,
        category: str,
        symbol: str
    ) -> dict:
        """ 
            Retrieve the lastest data in JSON format.

            Parameters
            -----------
                category: str,
                    data category
                symbol: str,
                    data symbol, be careful that the symbol is case sensitive

            Returns
            -----------
                data in dict format
        """
        data_response = self._get_data_response(category, symbol, get_historical_data=False)
        return data_response.json()
