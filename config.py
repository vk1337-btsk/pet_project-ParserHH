import os
from configparser import ConfigParser, NoSectionError


class Settings:
    DIR_PROJECT = os.path.dirname(__file__)         # Path to directory project
    name_section_params_db = 'database_vacancies'   # Name section params for database
    name_section_api_hh = 'params_api_hh'

    def __init__(self):
        self.params_api_hh = self.get_data_from_config(self.name_section_params_db)
        self.DB_NAME = self.params_api_hh['dbname']
        self.DB_HOST = self.params_api_hh['host']
        self.DB_USER = self.params_api_hh['user']
        self.DB_PASSWORD = self.params_api_hh['password']
        self.DB_PORT = self.params_api_hh['port']

        self.params_api_hh = self.get_data_from_config(self.name_section_api_hh)

    def get_data_from_config(self, name_section: str) -> dict[str, str]:
        """Этот метод получает словарь с данными из файла config.ini"""
        filename = os.path.join(self.DIR_PROJECT, "config.ini")
        parser = ConfigParser()
        try:
            parser.read(filename)
            return dict(parser.items(name_section))
        except NoSectionError as e:
            raise Exception(f"Section '{name_section}' not found in '{filename}'") from e

    @property
    def database_url_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def database_url_psycopg(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def api_hh(self):
        return self.params_api_hh

settings = Settings()