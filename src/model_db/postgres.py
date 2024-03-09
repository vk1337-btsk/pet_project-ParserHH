from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, inspect
from sqlalchemy import MetaData, Table, String, Integer, Column, Text, Boolean
from sqlalchemy import PrimaryKeyConstraint, ForeignKeyConstraint

import sqlalchemy_utils as sql_utils
from src.mixin import Mixin
from src.model_db.abc_db_manager import ManagerDB


class ModelPostgresSQL(ManagerDB, Mixin):
    engine_db = None
    metadata = None
    session_maker = None
    inspector = None
    basic_tables = None

    def __init__(self) -> None:
        self.name_section_params_db = 'database_vacancies'
        self.db_type = 'postgresql'
        self.driver_db = 'psycopg2'
        self.params_db = super().get_data_from_config(self.name_section_params_db)
        self.dbname = self.params_db['dbname']
        self.host = self.params_db['host']
        self.user = self.params_db['user']
        self.password = self.params_db['password']
        self.port = self.params_db['port']
        self.url = (f'{self.db_type}+{self.driver_db}://'
                    f'{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}')

    #
    #
    # Initialization database and basic methods
    def initialization_db(self) -> None:
        """Это комплексный метод инициализации БД. Метод ничего не возвращает. Алгоритм работы:
        - Проверка БД на существование:
            - не существует -> создать БД
            - существует -> осуществляем подключение к БД и создание основных атрибутов
        - Проверка таблиц и их строения на корректность:
            - таблицы не существуют -> создаём таблицы
            - таб"""
        try:
            # Проверяем, существует БД или нет
            if not self.check_exist_db():
                self.create_db()    # БД не существует - Создаём БД
            self.connect_to_db()    # Подключение и создание основных объектов для работы с БД



        except Exception:
            raise f'Возникла ошибка во время проверки на существование БД и/или создания БД {self.dbname}.'

    def check_tables(self):

        # Создаём атрибут (словарь) в формате: название таблицы -> объект таблицы
        self.basic_tables = self.get_basic_tables(self.metadata)

        # Проверяем, существуют ли наши таблицы и той ли они формы (получаем словарь название - bool)
        dict_flags: dict[str, bool] = self.check_correct_tables(self.basic_tables)

        # Если есть хотя бы одна таблица, которая отсутствует или не соответствует требованию
        if not all(dict_flags.values()):
            # Проходим по словарю, проверяя флаг, если True, то ничего не делаем, если False, пересоздаём таблицу
            for name_table, flag_table in dict_flags.items():
                if not flag_table:
                    self.drop_table(name_table)
                    self.create_table(self.basic_tables[name_table])

    def connect_to_db(self):
        try:
            if not (self.engine_db and self.metadata and self.session_maker and self.inspector):
                # Создаю движок (echo=True -> для отладки)
                self.engine_db: object = create_engine(url=self.url, echo=False, pool_size=3, max_overflow=5)
                # Создаю объект MetaData для хранения информации о таблицах
                self.metadata: object = MetaData()
                # Создаю объект session-maker
                self.session_maker: object = sessionmaker(self.engine_db)
                # Создаю объект типа Inspector
                self.inspector: object = inspect(self.engine_db)
                # Создаю объект типа Connection
                self.engine_db.connect()
        except Exception:
            raise Exception('Возникла ошибка во подключения к БД.')

    def create_db(self):
        try:
            sql_utils.functions.create_database(url=self.url, encoding='UTF-8', template=None)
        except Exception:
            print('БД уже создана (или возникла ошибка на этапе создания БД')
        else:
            print('Создали БД')

    def drop_db(self):
        try:
            sql_utils.functions.drop_database(url=self.url)
        except Exception:
            print('Возникла ошибка на этапе удаления БД')
        else:
            print('БД удалена')

    def check_exist_db(self):
        try:
            db_is_exist = sql_utils.functions.database_exists(url=self.url)
            return db_is_exist
        except Exception:
            print('Возникла ошибка во время проверки существования БД')
            return False

    def check_correct_tables(self, dict_tables_obj: dict[str, object]) -> dict[str, bool]:
        """Этот метод получает в аргументы словарь формата: {<Название таблицы>: <Объект таблицы>}
        и сравнивает таблицы с аналогичными таблицами в БД.
        :return - {<Название таблицы>: <Булево выражение, таблица существует и параметры столбцов соответствуют>}
        """
        # Получаем список названий таблиц из БД
        list_names_form_db = self.inspector.get_table_names()

        # Создаём словарь <Название таблицы>: <Булево выражение>
        dict_flags_tables_is_correct = dict().fromkeys(list(dict_tables_obj), False)

        for name_table, flag_table in dict_flags_tables_is_correct.items():
            if name_table in list_names_form_db:
                # тут должна быть проверка на сходство столбцов!
                # columns = self.inspector.get_columns('vacancies')
                x = True
                dict_flags_tables_is_correct[name_table] = x

        return dict_flags_tables_is_correct

    def create_table(self, table_object: object):
        table_for_create = [table_object]
        self.metadata.create_all(self.engine_db, table_for_create)

    def clear_tables(self):
        pass

    def drop_table(self, name_table):
        try:
            table = Table(name_table, self.metadata, autoload=True)
            table.drop(bind=self.engine_db)
        except Exception:
            print(f'Возникла ошибка на этапе удаления таблицы {name_table}')
        else:
            print('БД удалена')

    # def create_table(self, table_name: str, table_object: object) -> None:
    #     table_object.create(bind=self.engine_db)

    def add_data_to_db(self, *args):
        # session = sqlalchemy.orm.Session()
        """
        list_vacancies = []
        # for vacancy in args:
        #     my_vacancy = Vacancy(id=vacancy['id'],
        #                          premium=vacancy['premium'],
        #                          name=vacancy['name'],
        #                          has_test=vacancy['has_test'],
        #                          premium=vacancy['premium'],
        #                          name=vacancy['name'],
        #                          has_test=vacancy['has_test'],
        #                          response_letter_required=vacancy['response_letter_required'],
        #                          area_id=vacancy['area']['id'],
        #                          area_name=vacancy['area']['name'],
        #                          area_url=vacancy['area']['url'],
        #                          salary_from=vacancy['salary']['from'],
        #                          salary_to=vacancy['salary']['to'],
        #                          salary_currency=vacancy['salary']['currency'],
        #                          salary_gross=vacancy['salary']['gross'],
        #                          type_id=vacancy['type']['id'],
        #                          type_name=vacancy['type']['name'],
        #                          address_city=0 if not vacancy.get('address') else vacancy['address'].get('city', 0),
        #                          address_street=0 if not vacancy.get('address') else vacancy['address'].get('street',
         0),
        #                          address_building=0 if not vacancy.get('address') else vacancy['address'].
        get('building', 0),
        #                          address_lat=0 if not vacancy.get('address') else vacancy['address'].get('lat', 0),
        #                          address_lng=0 if not vacancy.get('address') else vacancy['address'].get('lng', 0),
        #                          address_description=0 if not vacancy.get('address') else vacancy['address'].get(
        'description', 0),
        #                          address_metro=0 if not vacancy.get('address') else vacancy['address'].get('metro',
        0),
        #                          address_lng=0 if not vacancy.get('address') else vacancy['address'].get('lng', 0))
"""
    def get_data_from_db(self):
        pass

    #
    #
    # Метод связанный с созданием и заполнением таблиц по умолчанию
    def fill_out_default_tables(self, dict_with_default_data):
        """Это комплексный метод для заполнения таблиц данными по умолчанию.
        Принимает в себя словарь с данными для заполнения"""
        self.fill_out_tables_area(dict_with_default_data['data_area'])

    def fill_out_tables_area(self, *args):
        areas_country = []
        areas_region = []
        areas_city = []
        for dict_country in args:
            areas_country.append({'country_id': dict_country['id'], 'country_name': dict_country['country_name']})
            for dict_region in dict_country['areas']:
                areas_region.append({'country_id': dict_region['parent_id'], 'region_id': dict_region['id'],
                                     'region_name': dict_region['name']})

                for dict_city in dict_region['areas']:
                    areas_city.append({'region_id': dict_city['parent_id'], 'city_id': dict_city['id'],
                                       'city_name': dict_city['name']})

        session = Session()
        session.add_all([areas_country, areas_region, areas_city])
        session.commit()

    #
    #
    # Метод связанный с созданием таблиц
    @staticmethod
    def get_basic_tables(metadata: object) -> dict[str, object]:

        areas_country = Table('areas_country', metadata,
                              Column('num_country', Integer(), autoincrement=True),
                              Column('country_id', Integer()),
                              Column('country_name', String(20), nullable=False),
                              PrimaryKeyConstraint('country_id', name='country_id_pk'),
                              extend_existing=True)

        areas_region = Table('areas_region', metadata,
                             Column('num_region', Integer(), autoincrement=True),
                             Column('country_id', Integer()),
                             Column('region_id', Integer()),
                             Column('region_name', String(20), nullable=False),
                             PrimaryKeyConstraint('region_id', name='region_id_pk'),
                             ForeignKeyConstraint(['country_id'], ['areas_country.country_id']),
                             extend_existing=True
                             )

        areas_city = Table('areas_city', metadata,
                           Column('num_city', Integer(), autoincrement=True),
                           Column('region_id', Integer()),
                           Column('city_id', Integer()),
                           Column('city_name', String(30), nullable=False),
                           PrimaryKeyConstraint('city_id', name='city_id_pk'),
                           ForeignKeyConstraint(['region_id'], ['areas_region.region_id']),
                           extend_existing=True
                           )

        vacancies = Table('vacancies', metadata,
                          Column('num_vacancy', Integer(), autoincrement=True),
                          Column('id', Integer(), primary_key=True),
                          Column('premium', Boolean()),
                          Column('name', Text(), ),
                          Column('department', Text()),
                          Column('has_test', Boolean()),
                          Column('response_letter_required', Boolean()),
                          Column('area_id', Integer()),
                          Column('area_name', Text()),
                          Column('area_url', Text()),
                          Column('salary_from', Integer()),
                          Column('salary_to', Integer()),
                          Column('salary_currency', Text()),
                          Column('salary_gross', Boolean()),
                          Column('type_id', Text()),
                          Column('type_name', Text()),
                          Column('address_city', Text()),
                          Column('address_street', Text()),
                          Column('address_building', Text()),
                          Column('address_lat', Text()),
                          Column('address_lng', Text()),
                          Column('address_description', Text()),
                          Column('address_raw', Text()),
                          Column('address_metro', Text()),
                          Column('address_metro_stations', Text()),
                          Column('address_id', Text()),
                          Column('response_url', Text()),
                          Column('sort_point_distance', Text()),
                          Column('published_at', Text()),
                          Column('created_at', Text()),
                          Column('archived', Text()),
                          Column('apply_alternate_url', Text()),
                          Column('show_logo_in_search', Text()),
                          Column('insider_interview', Text()),
                          Column('url', Text()),
                          Column('alternate_url', Text()),
                          Column('relations', Text()),
                          Column('employer_id', Text()),
                          Column('employer_name', Text()),
                          Column('employer_url', Text()),
                          Column('employer_alternate_url', Text()),
                          Column('employer_logo_urls', Text()),
                          Column('employer_logo_90', Text()),
                          Column('employer_logo_240', Text()),
                          Column('employer_logo_original', Text()),
                          Column('employer_vacancies_url', Text()),
                          Column('employer_accredited_it_employer', Text()),
                          Column('employer_trusted', Text()),
                          Column('snippet_requirement', Text()),
                          Column('snippet_responsibility', Text()),
                          Column('contacts', Text()),
                          Column('schedule', Text()),
                          Column('schedule_id', Text()),
                          Column('schedule_name', Text()),
                          Column('working_days', Text()),
                          Column('working_time_intervals', Text()),
                          Column('working_time_modes', Text()),
                          Column('accept_temporary', Text()),
                          Column('professional_roles_id', Text()),
                          Column('professional_roles_name', Text()),
                          Column('accept_incomplete_resumes', Text()),
                          Column('experience_id', Text()),
                          Column('experience_name', Text()),
                          Column('employment_id', Text()),
                          Column('employment_name', Text()),
                          Column('adv_response_url', Text()),
                          Column('is_adv_vacancy', Text()),
                          Column('adv_context', Text()),
                          extend_existing=True
                          )

        dict_basic_tables = {'areas_country': areas_country, 'areas_region': areas_region, 'areas_city': areas_city,
                             'vacancies': vacancies}

        return dict_basic_tables
