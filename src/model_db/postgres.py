from src.model_db.database import DataBase
import sqlalchemy_utils
from src.model_db.models import (Base, VacancyTypeOrm, VacanciesOrm, ScheduleTypeOrm, AreasOrm, ExperienceTypeOrm,
                                 EmploymentTypeOrm)
from src.mixin import Mixin


class PostgresORM(Mixin):

    def __init__(self) -> None:
        self.db = DataBase()
        self.exchange_rate = Mixin.get_exchange_rate()

    # Методы для начала работы с БД, а также основные методы для работы с ней
    def check_exist_db(self):
        return sqlalchemy_utils.database_exists(self.db.url_sync)

    def create_db(self):
        try:
            sqlalchemy_utils.create_database(url=self.db.url_sync, encoding='UTF-8', template=None)
        except Exception:
            print('БД уже создана (или возникла ошибка на этапе создания БД)')
        else:
            print('Создали БД')

    def drop_db(self):
        try:
            sqlalchemy_utils.drop_database(url=self.db.url_sync)
        except Exception:
            print('Возникла ошибка на этапе удаления БД')
        else:
            print('БД удалена')

    #
    # Метод связанный с созданием и заполнением таблиц
    def create_tables(self):
        Base.metadata.drop_all(self.db.sync_engine)
        Base.metadata.create_all(self.db.sync_engine)

    def fill_tables(self, default_data: dict[str, list]):
        self.fill_areas(default_data['areas'])
        self.fill_vacancy_type(default_data['vacancy_type'])
        self.fill_schedule_type(default_data['schedule'])
        self.fill_experience_type(default_data['experience'])
        self.fill_employment_type(default_data['employment'])

    def fill_areas(self, table_data: list):
        areas = []

        for dict_country in table_data:
            parent_id_country, parent_name_country, parent_id_region, parent_name_region = None, None, None, None

            areas.append({'id_areas': dict_country['id'], 'name_areas': dict_country['name'], 'code_areas': 1,
                          'parent_id_country': parent_id_country, 'parent_name_country': parent_name_country,
                          'parent_id_region': parent_id_region, 'parent_name_region': parent_name_region})

            parent_id_country = dict_country['id']
            parent_name_country = dict_country['name']
            for dict_region in dict_country['areas']:
                areas.append({'id_areas': dict_region['id'], 'name_areas': dict_region['name'], 'code_areas': 2,
                              'parent_id_country': parent_id_country, 'parent_name_country': parent_name_country,
                              'parent_id_region': parent_id_region, 'parent_name_region': parent_name_region})

                parent_id_region = dict_region['id']
                parent_name_region = dict_region['name']
                for dict_city in dict_region['areas']:
                    areas.append({'id_areas': dict_city['id'], 'name_areas': dict_city['name'], 'code_areas': 3,
                                  'parent_id_country': parent_id_country, 'parent_name_country': parent_name_country,
                                  'parent_id_region': parent_id_region, 'parent_name_region': parent_name_region})

        with self.db.session_factory() as session:
            areas = sorted(areas,
                           key=lambda x: (x['parent_name_country'] if not x['parent_name_country'] is None else "A",
                                          x['parent_name_region'] if not x['parent_name_region'] is None else "A",
                                          x['name_areas']))

            areas = [AreasOrm(id_areas=data['id_areas'], name_areas=data['name_areas'],
                              code_areas=data['code_areas'], parent_id_country=data['parent_id_country'],
                              parent_name_country=data['parent_name_country'],
                              parent_id_region=data['parent_id_region'], parent_name_region=data['parent_name_region'])
                     for data in areas]
            session.add_all(areas)
            session.flush()
            session.commit()

    def fill_employment_type(self, table_data: list):
        with self.db.session_factory() as session:
            experience_type = [EmploymentTypeOrm(employment_id=data['id'], employment_name=data['name'])
                               for data in table_data]
            session.add_all(experience_type)
            session.flush()
            session.commit()

    def fill_experience_type(self, table_data: list):
        with self.db.session_factory() as session:
            experience_type = [ExperienceTypeOrm(experience_id=data['id'], experience_name=data['name'])
                               for data in table_data]
            session.add_all(experience_type)
            session.flush()
            session.commit()

    def fill_vacancy_type(self, table_data: list):
        with self.db.session_factory() as session:
            vacancy_type = [VacancyTypeOrm(type_id=data['id'], type_name=data['name'])
                            for data in table_data]
            session.add_all(vacancy_type)
            session.flush()
            session.commit()

    def fill_schedule_type(self, table_data: list):
        with self.db.session_factory() as session:
            vacancy_type = [ScheduleTypeOrm(schedule_id=data['id'], schedule_name=data['name'])
                            for data in table_data]
            session.add_all(vacancy_type)
            session.flush()
            session.commit()

    def fill_vacancies(self, table_data: list):
        with self.db.session_factory() as session:
            existing_ids = {row.vacancy_id for row in session.query(VacanciesOrm).all()}

            vacancy = [VacanciesOrm(
                # Main information
                vacancy_id=int(data['id']),
                name=data['name'],

                # Information - salary
                salary_from=None if not data.get('salary') else data['salary'].get('from', None),
                salary_to=None if not data.get('salary') else data['salary'].get('to', None),
                salary_currency=None if not data.get('salary') else 'RUB'
                if data['salary'].get('currency', None) == 'RUR' else 'BYN'
                if data['salary'].get('currency', None) == 'BYR' else data['salary'].get('currency', None),
                salary_gross=None if not data.get('salary') else data['salary'].get('gross', None),

                # Information - address
                id_areas=int(data['area']['id']),
                address_city=None if not data.get('address') else data['address'].get('city', None),
                address_raw=None if not data.get('address') else data['address'].get('raw', None),
                address_street=None if not data.get('address') else data['address'].get('street', None),
                address_building=None if not data.get('address') else data['address'].get('building', None),
                address_lat=None if not data.get('address') else data['address'].get('lat', None),
                address_lng=None if not data.get('address') else data['address'].get('lng', None),
                address_description=None if not data.get('address') else data['address'].get('description', None),
                address_id=None if not data.get('address') else data['address'].get('id', None),

                # Main criteria
                type_id=data['type']['id'],
                schedule_id=data['schedule']['id'],
                experience_id=data['experience']['id'],
                employment_id=data['employment']['id'],

                # Information - employer
                employer_id=int(data['employer']['id']),
                employer_url=data['employer']['url'],
                employer_alternate_url=data['employer']['alternate_url'],
                employer_logo_urls=data['employer']['alternate_url'],
                employer_vacancies_url=data['employer']['vacancies_url'],
                employer_accredited_it_employer=data['employer']['accredited_it_employer'],
                employer_trusted=data['employer']['trusted'],

                # Information - metro
                # address_metro_station_name=None if not data.get('address') else None
                # if not data['address'].get('metro') else data['address']['metro'].get('station_name', None),
                # address_metro_line_name=None if not data.get('address') else None
                # if not data['address'].get('metro') else data['address']['metro'].get('line_name', None),
                # address_metro_station_id=None if not data.get('address') else None
                # if not data['address'].get('metro') else data['address']['metro'].get('station_id', None)
                # if data['address']['metro'].get('station_id', None) else
                # data['address']['metro'].get('station_id', None),
                # address_metro_line_id=None if not data.get('address') else None
                # if not data['address'].get('metro') else data['address']['metro'].get('line_id', None)
                # if data['address']['metro'].get('line_id', None) else
                # data['address']['metro'].get('line_id', None),
                # address_metro_lat=None if not data.get('address') else None
                # if not data['address'].get('metro') else data['address']['metro'].get('lat', None)
                # if data['address']['metro'].get('lat', None) else
                # data['address']['metro'].get('lat', None),
                # address_metro_lng=None if not data.get('address') else None
                # if not data['address'].get('metro') else data['address']['metro'].get('lng', None)
                # if data['address']['metro'].get('lng', None) else
                # data['address']['metro'].get('lng', None),

                # has_test=data['has_test'],
                # response_letter_required=data['response_letter_required'],

                # response_url=data['response_url'],
                # sort_point_distance=data['response_url'],
                # published_at=data['published_at'],   ##############тут время исо 8601. как его передавать?
                # created_at=data['created_at'],   ##############тут время исо 8601. как его передавать?
                # archived=data['archived'],
                # apply_alternate_url=data['apply_alternate_url'],
                # # show_logo_in_search=data['show_logo_in_search'],
                # insider_interview_id=None if not data.get('insider_interview')
                # else data['insider_interview'].get('id', None),
                # insider_interview_url=None if not data.get('insider_interview')
                # else data['insider_interview'].get('url', None),
                # url=data['url'],
                # alternate_url=data['alternate_url'],
                # relations=data['relations'],   ############## тут список. как его передавать?
                #

                #
                # snippet_requirement=None if not data.get('snippet') else data['snippet'].get('requirement', None),
                # snippet_responsibility=None if not data.get('snippet')
                # else data['snippet'].get('responsibility', None),
                #
                # contacts_call_tracking_enabled=None if not data.get('contacts')
                # else data['contacts'].get('call_tracking_enabled', None),
                # contacts_email=None if not data.get('contacts') else data['contacts'].get('email', None),
                # contacts_name=None if not data.get('contacts') else data['contacts'].get('name', None),
                # contacts_phones_city=None if not data.get('contacts') else None
                # if not data['contacts'].get('phones') else data['contacts']['phones'].get('city', None),
                # contacts_phones_comment=None if not data.get('contacts') else None
                # if not data['contacts'].get('phones') else data['contacts']['phones'].get('comment', None),
                # contacts_phones_country=None if not data.get('contacts') else None
                # if not data['contacts'].get('phones') else data['contacts']['phones'].get('country', None),
                # contacts_phones_formatted=None if not data.get('contacts') else None
                # if not data['contacts'].get('phones') else data['contacts']['phones'].get('formatted', None),
                # contacts_phones_number=None if not data.get('contacts') else None
                # if not data['contacts'].get('phones') else data['contacts']['phones'].get('number', None),
                #
                #
                # accept_temporary=data['accept_temporary'],
                # accept_incomplete_resumes=data['accept_incomplete_resumes'],
                # department_id=None if not data.get('department') else data['department'].get(['id'], None),
                # department_name=None if not data.get('department') else data['department'].get(['name'], None),
                # premium=data['premium'],

            )
                            for data in table_data if int(data['id']) not in existing_ids]
            session.add_all(vacancy)
            session.flush()
            session.commit()

    def get_top_vacancies(self, count_top: int = None) -> list:
        """Метод получает с БД список сохранённых вакансий"""
        with self.db.session_factory() as session:
            if not count_top:
                list_vacancies = session.query(VacanciesOrm).all()
            else:
                list_vacancies = session.query(VacanciesOrm).limit(count_top).all()
        return list_vacancies

    def get_average_salary_from_db(self):
        with self.db.session_factory() as session:
            list_salary = [{'salary_from': row.salary_from, 'salary_to': row.salary_to,
                            'salary_currency': row.salary_currency} for row in session.query(VacanciesOrm).all()]

        avg_min_salary = []
        avg_max_salary = []
        avg_salary = []

        for salary_info in list_salary:
            if salary_info['salary_currency'] and salary_info['salary_currency'] != "RUB":
                if not salary_info['salary_from'] is None:
                    salary_info['salary_from'] = self.convert_currency(
                        salary_info['salary_from'], salary_info['salary_currency'])

                if not salary_info['salary_to'] is None:
                    salary_info['salary_to'] = self.convert_currency(
                        salary_info['salary_to'], salary_info['salary_currency'])

            if salary_info['salary_from'] is None and salary_info['salary_to']:
                avg_max_salary.append(salary_info['salary_to'])
            elif salary_info['salary_from'] and salary_info['salary_to'] is None:
                avg_min_salary.append(salary_info['salary_from'])
            elif salary_info['salary_from'] and salary_info['salary_to']:
                avg_salary.append((salary_info['salary_from'] + salary_info['salary_to']) / 2)

        not_salary = len(list_salary) - len(avg_min_salary) - len(avg_max_salary) - len(avg_salary)
        avg_min_salary = sum(avg_min_salary) / len(avg_min_salary) if len(avg_min_salary) else 0
        avg_max_salary = sum(avg_max_salary) / len(avg_max_salary) if len(avg_max_salary) else 0
        avg_salary = sum(avg_salary) / len(avg_salary) if len(avg_salary) else 0

        return {'avg_min_salary': int(avg_min_salary), 'avg_salary': int(avg_salary),
                'avg_max_salary': int(avg_max_salary), 'not_salary': not_salary}

    def convert_currency(self, salary: float or int, currency: str) -> float or int:
        """This method converts salary from foreign currency into rubles."""
        for dict_ in self.exchange_rate:
            if dict_['letter_code'] == currency:
                my_dict = dict_
                new_salary = salary * float(my_dict['rate'].replace(',', '.')) / int(my_dict['quantity'])
                return new_salary

    def get_vacancies_where_salary_more_avg_salary(self, dict_avg):
        with self.db.session_factory() as session:
            list_vacancies = session.query(VacanciesOrm).filter(VacanciesOrm.salary_currency.isnot(None)).all()

        vacancies_avg_min_salary = []
        vacancies_avg_max_salary = []
        vacancies_avg_salary = []

        for vac in list_vacancies:

            if bool(vac.salary_from) and vac.salary_to is None:
                if vac.salary_currency == "RUB":
                    if vac.salary_from >= dict_avg['avg_min_salary']:
                        vacancies_avg_min_salary.append(vac)
                else:
                    if self.convert_currency(vac.salary_from, vac.salary_currency) >= dict_avg['avg_min_salary']:
                        vacancies_avg_min_salary.append(vac)

            elif vac.salary_from is None and bool(vac.salary_to):
                if vac.salary_currency == "RUB":
                    if vac.salary_to >= dict_avg['avg_max_salary']:
                        vacancies_avg_max_salary.append(vac)
                else:
                    if self.convert_currency(vac.salary_to, vac.salary_currency) >= dict_avg['avg_min_salary']:
                        vacancies_avg_max_salary.append(vac)

            elif bool(vac.salary_from) and bool(vac.salary_to):
                if vac.salary_currency == "RUB":
                    if int((vac.salary_from + vac.salary_to) / 2) >= dict_avg['avg_salary']:
                        vacancies_avg_salary.append(vac)
                else:
                    if (int((self.convert_currency(vac.salary_from, vac.salary_currency) +
                             self.convert_currency(vac.salary_to, vac.salary_currency)) / 2) >=
                            dict_avg['avg_salary']):
                        vacancies_avg_salary.append(vac)

        return {'vacancies_avg_min_salary': vacancies_avg_min_salary,
                'vacancies_avg_max_salary': vacancies_avg_max_salary, 'vacancies_avg_salary': vacancies_avg_salary}
