import requests
from src.mixin import Mixin
from src.classes_hh.abc_hh import ABC_model_HH
from src.classes_hh.c_get_data import GetDataFromUser


class ModelHH(ABC_model_HH, Mixin):
    """Этот класс осуществляет все действия с API HH"""
    api_basic_url = 'https://api.hh.ru'

    def __init__(self):
        # Основные данные
        self.params_api_hh = super().get_data_from_config('params_api_hh')
        self.api_client_id = self.params_api_hh['client_id']
        self.api_client_secret = self.params_api_hh['client_secret']
        self.api_redirect_uri = self.params_api_hh['redirect_uri']
        self.api_assert_token = self.params_api_hh['api_assert_token']
        self.api_refresh_token = self.params_api_hh['api_refresh_token']
        self.api_authorization_code = self.params_api_hh['api_authorization_code']

    # Главные функции
    def choice_command(self, number_command):
        self.list_command = \
            {
                1: ['Получить список вакансий с сайта HeadHunter', self.parse_vacancies_from_the_site],
                2: ['Авторизация пользователя', print],
                3: ['Просмотр резюме авторизованного пользователя', print],
                4: ['Просмотр избранных вакансий авторизованного пользователя', print]
            }

        current_function = self.list_command[number_command][1]
        return current_function()

    #
    # Вспомогательные функции
    @staticmethod
    def get_response(basic_url: str, headers: dict, params: dict) -> dict or Exception:
        """This method sends a request to a specific site and returns a response in case of a positive response
        (response with status 200 or raises an exception in case of an error)
        :param basic_url: url website which the requests sent;
        :param headers: headers requests
        :param params: parameters requests
        :return: server response with list vacancies in format json or raise Exception
        """
        response = requests.get(basic_url, headers=headers, params=params)

        if bool(response):
            return response.json()
        else:
            raise requests.HTTPError('Ошибка. Запрос ответ не с кодом 200. Внутри get_response')

    #
    # Блок функций для команды 1
    def parse_vacancies_from_the_site(self) -> list:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/121.0.0.0 Safari/537.36'}
        params = {
                # Parameters for parsing
                'page': 0,  # Number page site
                'per_page': 5,  # Number of requests on page            #################################
        }
        criteria_for_search = GetDataFromUser().get_criteria_from_user()
        params.update(criteria_for_search)

        print(params)

        url_for_parsing = self.api_basic_url + '/vacancies'

        list_vacancies = []
        print('Пожалуйста, подождите. Загружаем вакансии с сайта HeadHunter.ru')
        while True:
            try:
                response = super().get_response(basic_url=url_for_parsing, headers=headers, params=params)
                response_list_vacancies = response['items']
                last_page = response['pages']
                params['page'] += 1
                super().get_time_for_sleep()
                for vacancy in response_list_vacancies:
                    list_vacancies.append(vacancy)

                if last_page == params['page']:
                    break
            except requests.HTTPError:
                break

            break

        return list_vacancies


