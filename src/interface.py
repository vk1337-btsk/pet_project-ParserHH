from src.model_db.postgres import PostgresORM
from src.model_hh.main_hh import ModelHH
from src.view.com_str import ViewCommandString
from src.vacancy import Vacancy


class ControllerInterface:

    def __init__(self) -> None:
        self.ModelHH = ModelHH()
        self.ModelDB = None
        self.View = ViewCommandString()

        self.list_command = self.menu_command()
        self.params_controller = {}

    #
    #
    # Метод, который реализует метод команд для работы
    def menu_command(self):
        list_command = \
            {
                0: ['Выход из программы'],

                1: ['Получить и сохранить список вакансий с сайта HeadHunter по ключевому слову и/или другим критериям'],
                2: ['Получить и сохранить список вакансий с сайта HeadHunter по определённым компаниям'],

                3: ['Вывести список сохранённых вакансий (вывод N вакансий)'],

                4: ['Получить среднюю зарплату по сохранённым вакансиям'],
                5: ['Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям']
            }
        return list_command

    def start(self):
        self.hello_message()
        self.initialization_db()

        while True:
            command = self.message_main_menu()
            self.run_command(number_command=command)

    def run_command(self, number_command):
        if number_command == 0:
            # Выход из программы
            exit()

        elif number_command == 1:
            # Получить и сохранить список вакансий с сайта HeadHunter по ключевому слову и/или другим критериям
            answer = self.ModelHH.parse_vacancies_from_the_site()
            self.ModelDB.fill_vacancies(answer)

        elif number_command == 2:
            # Получить и сохранить список вакансий по выбранным компаниям
            answer = self.input_company_for_parse_vacancies()
            list_vacancies = self.ModelHH.parse_vacancies_employer(answer)
            self.ModelDB.fill_vacancies(list_vacancies)

        elif number_command == 3:
            # Вывести то N вакансий из БД
            answer = self.input_top_vacancies_to_print()
            list_vacancies = self.ModelDB.get_top_vacancies(answer)
            for index, vacancy in enumerate(list_vacancies, 1):
                self.View.print_my_text(f'{index} {str(Vacancy(vacancy))}')

        elif number_command == 4:
            # Получить среднюю зарплату по сохранённым вакансиям
            list_avg_salary = self.ModelDB.get_average_salary_from_db()
            self.params_controller.update({'list_avg_salary': list_avg_salary})
            self.print_info_avg_salary(list_avg_salary)

        elif number_command == 5:
            # Вывести компании, у которых средняя зарплата больше средней по БД
            if not self.params_controller.get('list_avg_salary', None):
                list_avg_salary = self.ModelDB.get_average_salary_from_db()
                self.params_controller.update({'list_avg_salary': list_avg_salary})
                self.print_info_avg_salary(list_avg_salary)

            list_vacancies = self.ModelDB.get_vacancies_where_salary_more_avg_salary(
                self.params_controller['list_avg_salary'])
            self.print_top_vacancies_where_salary_more_avg_salary(list_vacancies)


    #
    #
    # Метод инициализации БД при первичном подключении или запуске команды
    def initialization_db(self):
        # При первичном запуске атрибут ModelDB будет is None. Инициализация БД
        if self.ModelDB is None:
            self.ModelDB = PostgresORM()

            # Проверяем, существует БД или нет.
            if not self.ModelDB.check_exist_db():
                # Если не существует, то создаём БД
                self.ModelDB.create_db()

                # Заполняем таблицы данными по умолчанию
                default_data_hh: dict[str, list[dict or list]] = self.ModelHH.get_default_data()
                self.ModelDB.create_tables()
                self.ModelDB.fill_tables(default_data_hh)

            # Спрашиваем, пересоздать БД или нет (1 - да)
            if int(self.message_reboot_db()) == 2:
                default_data_hh: dict[str, list[dict or list]] = self.ModelHH.get_default_data()
                self.ModelDB.create_tables()
                self.ModelDB.fill_tables(default_data_hh)

    #
    #
    # Methods for communicating with the user
    def hello_message(self):
        """Метод, реализующий приветственное сообщение"""
        text = (f'Привет! Это программа для работы с HeadHunter.ru.\n'
                f'В ней можно работать с вакансиями, а также после авторизации выполнять действия со своего аккаунта, '
                f'такие как просмотр резюме, избранных вакансий, осуществление откликов и т.д.')
        self.View.print_my_text(text)

    def message_main_menu(self):
        """Метод, реализующий главное меню"""
        text_list_command = '\n'.join([f"{str(key)} - {value[0]}" for key, value in self.list_command.items()])
        text1 = ('\nВведите номер команды для её осуществления:\n'
                f'{text_list_command}\n'
                 'Введите номер команды, чтобы её выполнить.')
        text2 = 'Вы ввели неизвестную команду, повторите ввод: '
        answer = self.View.input_commands(text1)
        while not answer.isdigit() or (answer.isdigit() and int(answer) not in list(self.list_command.keys())):
            answer = self.View.input_commands(text2)
        return int(answer)

    def message_reboot_db(self):
        """Метод, реализующий вопрос у пользователя о сбросе БД"""
        text1 = ('\nЖелаете работать с текущей базой данных вакансий? (Нет означает пересоздание БД):\n'
                 '1 - Да\n'
                 '2 - Нет\n')
        text2 = 'Вы ввели неизвестную команду, повторите ввод: '
        answer = self.View.input_commands(text1)

        while not answer.isdigit() or (answer.isdigit() and int(answer) not in [1, 2]):
            answer = self.View.input_commands(text2)
        return int(answer)

    def input_top_vacancies_to_print(self):
        """Метод, реализующий вопрос у пользователя о выводе количества вакансий"""
        text1 = '\nСколько вакансий нужно вывести? Нужно ввести количество вакансий для вывода.'
        text2 = 'Вы ввели неизвестную команду, повторите ввод: '
        answer = self.View.input_commands(text1)
        while not answer.isdigit():
            answer = self.View.input_commands(text2)
        return int(answer)

    def input_favorites_company_for_search(self):
        """Метод, реализующий главное меню"""
        text1 = ('\nВведите компанию, чьи вакансии вы хотите получить. Можно ввести:\n'
                 '1 - id компании на сайте HeadHunter\n'
                 '2 - url компании на сайте HeadHunter\n'
                 # '3 - Название компании на сайте HeadHunter\n'
                 'Просто введите id или url:\n')
        text2 = 'Вы ввели неизвестную команду, повторите ввод: '

        answer = self.View.input_commands(text1)
        while True:
            if answer.isdigit():
                return int(answer)
            elif '/' in answer and answer[answer.rfind('/')+1:].isdigit():
                return int(answer[answer.rfind('/')+1:])
            answer = self.View.input_commands(text2)

    def input_company_for_parse_vacancies(self):
        """Метод, реализующий главное меню"""
        text1 = ('\nВведите компанию или компании, чьи вакансии вы хотите получить. Можно ввести:\n'
                 '1 - id компании на сайте HeadHunter\n'
                 '2 - url компании на сайте HeadHunter\n'
                 # '3 - Название компании на сайте HeadHunter\n'
                 'Если, хотите выйти - нажмите 0. Просто введите id или url компании:\n')
        text2 = 'Введите данные следующей компании или "0" для выхода: '
        text3 = 'Введены не корректная информация. Повторите ввод.'
        list_id_employers = []

        answer = self.View.input_commands(text1)
        while True:
            if answer.isdigit() and int(answer) == 0:
                break
            elif answer.isdigit():
                list_id_employers.append(answer)
            elif '/' in answer and answer[answer.rfind('/')+1:].isdigit():
                list_id_employers.append(answer[answer.rfind('/')+1:])
            else:
                self.View.print_my_text(text3)
            answer = self.View.input_commands(text2)

        return list_id_employers

    def print_info_avg_salary(self, dict_avg_salary):
        text = (f'\nИтого средняя зарплата по вакансиям из БД:\n'
                f'- {dict_avg_salary["avg_min_salary"]} - по вакансиям, у которых указано только ОТ\n'
                f'- {dict_avg_salary["avg_max_salary"]} - по вакансиям, у которых указано только ДО\n'
                f'- {dict_avg_salary["avg_salary"]} - по вакансиям, у которых указано и ОТ, и ДО\n'
                f'- по {dict_avg_salary["not_salary"]} не указана зарплата\n')
        self.View.print_my_text(text)

    def print_top_vacancies_where_salary_more_avg_salary(self, dict_list_vacancies: dict):
        for title, list_vacancies in dict_list_vacancies.items():
            text = ''
            if title == 'vacancies_avg_min_salary':
                text = 'Список вакансий, у которых указана только зарплата ОТ и она больше средней по БД'
            elif title == 'vacancies_avg_max_salary':
                text = 'Список вакансий, у которых указана только зарплата ДО и она больше средней по БД'
            elif title == 'vacancies_avg_salary':
                text = 'Список вакансий, у которых указана зарплата и ОТ, и ДО и она больше средней по БД'

            for index, vacancy in enumerate(list(list_vacancies), 1):
                self.View.print_my_text(text)
                self.View.print_my_text(f'{index} {str(Vacancy(vacancy))}')
            self.View.print_my_text('\n\n')
