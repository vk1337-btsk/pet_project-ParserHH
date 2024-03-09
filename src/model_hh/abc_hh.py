from abc import ABC, abstractmethod
import random
import requests


class ABC_model_HH(ABC):

    # Abstract methods
    # @abstractmethod
    # def get_headers(self) -> None:
    #     pass
    #
    # @abstractmethod
    # def get_params(self) -> None:
    #     pass

    # Static method
    @staticmethod
    def get_time_for_sleep() -> float:
        count_second = random.uniform(0.3, 0.5)
        return count_second

    @staticmethod
    def get_response(basic_url: str, headers: dict, params: dict) -> dict or Exception:
        response = requests.get(basic_url, headers=headers, params=params)

        if bool(response):
            return response.json()
        else:
            raise requests.HTTPError('Ошибка. Запрос ответ не с кодом 200. Внутри get_response')