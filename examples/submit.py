import os
import sys
import time
sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..'))

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from src.submit import Submission

def print_dash_line(n: int=50):
    print(''.join(['-']*n))

if __name__ == "__main__":
    s = Submission(api_key=os.getenv('API_KEY'))
    example_data = [{"OPEN_TIME": 1656932400000, "PREDICTION": 0.487618394396533}, {"OPEN_TIME": 1656932400000, "PREDICTION": 0.5362608062847783}]
    
    print_dash_line()
    print("Example submission - Submission time:", s.submit(True, data=example_data, symbol='BTC'))

    # Wait until the system has completed its scoring process.
    time.sleep(5)

    # Get all submission time
    all_rec = s.get_submission_time(is_backtest=True, symbol='BTC')['BTCUSDT']
    
    print_dash_line()
    print("All recorded submission time:", all_rec)

    print_dash_line()
    print("Results:", s.get_result(is_backtest=True, submission_time=int(all_rec[-1]), symbol='BTC'))

    print_dash_line()
    print("Deleted status of lastest record:", s.delete_record(is_backtest=True, submission_time=int(all_rec[-1]), symbol='BTC'))
