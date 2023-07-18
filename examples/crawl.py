import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..'))

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from src.crawl import Crawler

if __name__ == "__main__":
    crawler = Crawler(api_key=os.getenv('API_KEY')) # Put your API key in .env file
    crawler.download_historical_data(category="crypto", symbol="DYDX", location='./data')
    print("Lastest data: ", crawler.get_lastest_data(category="crypto", symbol="BTCUSDT"))