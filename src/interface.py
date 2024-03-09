

class ControllerUserInterface:

    def __init__(self):
        self.current_command = None
        self.current_message = None
        self.list_command = self.commands()

    def commands(self):
        list_command = \
            {
                0: 'Выход из программы',
                1: 'Получить список вакансий с сайта HeadHunter',
                2: 'Авторизация пользователя',
                3: 'Просмотр резюме авторизованного пользователя',
                4: 'Просмотр избранных вакансий авторизованного пользователя'
            }
        return list_command

# Methods for communicating with the user

    # Properties for attributes for communicating with the user
    @property
    def current_command(self):
        return self._command

    @current_command.setter
    def current_command(self, value):
        self._command = value

    @property
    def current_message(self):
        return self._current_message

    @current_message.setter
    def current_message(self, value):
        self._current_message = value

    # Decorators for communicating with view
    def print_text(function):
        def wrapper(*args, **kwargs):
            text = function(*args, **kwargs)
            return text
        return wrapper

    def input_text(function):
        def wrapper(*args, **kwargs):
            text = function(*args, **kwargs)
            return text
        return wrapper

    @print_text
    def hello_message(self):
        text = (f'Привет! Это программа для работы с HeadHunter.ru.\n'
                f'В ней можно работать с вакансиями, а также после авторизации выполнять действия со своего аккаунта, '
                f'такие как просмотр резюме, избранных вакансий, осуществление откликов и т.д.\n')
        return text

    @input_text
    def main_menu(self):
        text_list_command = '\n'.join([f"{str(key)} - {value}" for key, value in self.list_command.items()])
        text = ('\nВведите номер команды для её осуществления:\n'
                f'{text_list_command}'
                'Введите номер команды, чтобы её выполнить.')
        return text
