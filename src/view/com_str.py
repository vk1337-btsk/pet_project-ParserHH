class ViewCommandString:

    def __init__(self):
        pass

    @staticmethod
    def print_my_text(text: str):
        print(text)

    @staticmethod
    def input_commands(text: str):
        query = '\nВведите вашу команду: '
        text_question = text + query
        answer = input(text_question).strip()
        return answer

