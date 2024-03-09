from abc import ABC, abstractmethod
import random
import requests


class abc_model_HH(ABC):
    api_basic_url = 'https://api.hh.ru'

    @staticmethod
    def get_time_for_sleep() -> float:
        count_second = random.uniform(0.3, 0.5)
        return count_second

    def get_response(self, basic_url: str = None, sub_url: str = "", headers: dict = None, params: dict = None)\
            -> dict or Exception:

        if not basic_url:
            basic_url = self.api_basic_url
        if not headers:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                     'Chrome/121.0.0.0 Safari/537.36'}
        response = requests.get(url=basic_url + sub_url, headers=headers, params=params)
        if bool(response):
            return response.json()
        else:
            raise requests.HTTPError('Ошибка. Запрос ответ не с кодом 200. Внутри get_response')
