from typing import List

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from src.base import Base

class Submission(Base):
    def __init__(self, api_key):
        super().__init__(api_key=api_key)
        self._cur_round = self._get(Submission.NESTQUANT_API_ENDPOINT + 'competition/nestquant_tournament_2023/current-round').json()['Current round']
        self._records_url = Submission.NESTQUANT_API_ENDPOINT + f'competition/nestquant_tournament_2023/records/api?api_key=' + self._api_key
        self._result_url = Submission.NESTQUANT_API_ENDPOINT + f'competition/nestquant_tournament_2023/result/api?&api_key=' + self._api_key
        self._submit_url = Submission.NESTQUANT_API_ENDPOINT + f'competition/nestquant_tournament_2023/submit/api?api_key=' + self._api_key
    
    def __convert_dict_to_url_str(
        self,
        d: List[dict]
    ) -> str:
        """
            Convert list of dictionary to string - this is a helper function for submit method

            Parameters
            -----------
                d: List[dict],
                    data in list of dictionary format

            Returns
            ----------
                data in string format
        """
        return str(d).replace("'", '"')

    def submit(
        self,
        is_backtest: bool,
        data: List[dict],
        symbol: str=None
    ) -> int:
        """
            Submit model's output

            Parameters
            -----------
                is_backtest: bool,
                    whether we choose to submit for backtesting or not
                data: List[dict],
                    data in list of dictionary format
                symbol: str, default None,
                    provided symbol, exclusively utilized for the purpose of backtesting

            Returns
            ----------
                submission_time: int
                    recorded submission time
        """
        if is_backtest:
            res = self._post(self._submit_url + f'&submission_type=backtest&symbol={symbol}', data=self.__convert_dict_to_url_str(data))
        else:
            res = self._post(self._submit_url + f'&submission_type={self._cur_round}', data=self.__convert_dict_to_url_str(data))
        submission_time = res.json()['Submisstion time']
        return submission_time

    def get_submission_time(
        self,
        is_backtest: bool, 
        symbol: str=None
    ) -> dict:
        """
            Get all the recorded submission time

            Parameters
            -----------
                is_backtest: bool,
                    whether we choose to submit for backtesting or not
                symbol: str, default None,
                    provided symbol, exclusively utilized for the purpose of backtesting

            Returns
            ----------
                res: dict
                    all recorded submission time
        """
        if is_backtest:
            res = self._get(self._records_url + f'&submission_type=backtest&symbol={symbol}')
        else:
            res = self._get(self._records_url + f'&submission_type={self._cur_round}')
        return res.json()

    def get_result(
        self,
        is_backtest: bool, 
        submission_time: int,
        symbol: str = None
    ) -> dict:
        """
            Get model's performance

            Parameters
            -----------
                is_backtest: bool,
                    whether we choose to submit for backtesting or not
                submission_time: int,
                    recorded submission time
                symbol: str, default None,
                    provided symbol, exclusively utilized for the purpose of backtesting

            Returns
            ----------
                res: dict
                    all scores of the model
        """
        if is_backtest:
            res = self._get(self._result_url + f'&submission_type=backtest&symbol={symbol}&submission_time={submission_time}')
        else:
            res = self._get(self._result_url + f'&submission_type={self._cur_round}&submission_time={submission_time}')
        return res.json()
    
    def delete_record(
        self,
        is_backtest: bool, 
        submission_time: int,
        symbol: str=None
    ) -> str:
        """
            Delete model's record

            Parameters
            -----------
                is_backtest: bool,
                    whether we choose to submit for backtesting or not
                submission_time: int,
                    recorded submission time
                symbol: str, default None,
                    provided symbol, exclusively utilized for the purpose of backtesting

            Returns
            ----------
                If successful, return "Delete record successfully"
        """
        if is_backtest:
            res = self._delete(self._records_url + f'&submission_type=backtest&symbol={symbol}&submission_time={submission_time}')
        else:
            res = self._delete(self._records_url + f'&submission_type={self._cur_round}&submission_time={submission_time}')
        return res.text
