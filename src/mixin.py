import requests
from bs4 import BeautifulSoup


class Mixin:
    """This is class Mixin. It was implemented to expand the functionality of the Vacancy class."""

    _exchange_rate = None  # Классовый атрибут для хранения курса валют

    @staticmethod
    def get_exchange_rate() -> list[dict, dict, ...]:
        """This method requests the exchange rate from the website of the Central Bank of the Russian Federation
        and creates a class attribute with the current exchange rate:
        :return - list dictionaries with actual exchange rate currently.
        """
        if Mixin._exchange_rate is None:
            headers = {'User-Agent': 'Mozilla/5.0 ...'}
            response = requests.get('https://www.cbr.ru/currency_base/daily/', headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            table = soup.find('div', class_='table').find_all('tr')

            exchange_rate = [info.text.split('\n')[1:-1] for info in table]
            title = ['digit_code', 'letter_code', 'quantity', 'currency', 'rate']
            Mixin._exchange_rate = [dict(zip(title, info_currency)) for info_currency in exchange_rate[1:]]

        return Mixin._exchange_rate
