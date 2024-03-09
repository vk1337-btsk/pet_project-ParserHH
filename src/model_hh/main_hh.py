from config import settings
import requests
from src.model_hh.abc_hh import abc_model_HH
from src.model_hh.get_data import GetDataFromUser


class ModelHH(abc_model_HH):
    """Этот класс осуществляет все действия с API HH"""
    api_basic_url = 'https://api.hh.ru'

    def __init__(self):
        # Основные данные
        # self.params_api_hh = settings.params_api_hh
        # self.api_client_id = self.params_api_hh['client_id']
        # self.api_client_secret = self.params_api_hh['client_secret']
        # self.api_redirect_uri = self.params_api_hh['redirect_uri']
        # self.api_assert_token = self.params_api_hh['api_assert_token']
        # self.api_refresh_token = self.params_api_hh['api_refresh_token']
        # self.api_authorization_code = self.params_api_hh['api_authorization_code']

        self.list_command = None

    #
    #
    # Блок функций для получения данных по умолчанию с HH
    def get_default_data(self) -> dict[str, list]:
        # Если не передано ничего, то нужно получить все стандартные данные
        dictionary_default_data = {}

        response = super().get_response(sub_url='/areas')
        dict_areas = {'areas': response}
        dictionary_default_data.update(dict_areas)

        response = super().get_response(sub_url='/dictionaries')
        dictionary_params = {'vacancy_type': response['vacancy_type'], 'schedule': response['schedule'],
                             'experience': response['experience'], 'employment': response['employment']}
        dictionary_default_data.update(dictionary_params)

        return dictionary_default_data

    def get_data_employer(self):
        response = super().get_response(sub_url='')


    #
    #
    # Блок функций для команды 1
    def parse_vacancies_from_the_site(self) -> list:
        params = {
                # Parameters for parsing
                'page': 0,  # Number page site
                'per_page': 100,  # Number of requests on page            #################################
        }
        criteria_for_search = GetDataFromUser().get_criteria_from_user()
        params.update(criteria_for_search)

        list_vacancies = []
        print('Пожалуйста, подождите. Загружаем вакансии с сайта HeadHunter.ru')
        while True:
            try:
                response = super().get_response(sub_url='/vacancies', params=params)
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

    def parse_vacancies_employer(self, id_employer: list):
        params = {
                # Parameters for parsing
                'page': 0,  # Number page site
                'per_page': 100,
                'employer_id': id_employer # Number of requests on page            #################################
        }
        list_vacancies = []
        print('Пожалуйста, подождите. Загружаем вакансии с сайта HeadHunter.ru')
        while True:
            try:
                response = super().get_response(sub_url='/vacancies', params=params)
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
        return list_vacancies

