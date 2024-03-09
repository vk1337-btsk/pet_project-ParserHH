from src.mixin import Mixin


class ViewCommandString(Mixin):

    def __init__(self):
        pass

    @staticmethod
    def print_my_text(text: str):
        print(text)

    @staticmethod
    def input_commands(text: str):
        query = '\nВведите вашу команду: '
        answer = input(text + query)
        return answer
