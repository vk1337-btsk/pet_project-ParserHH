from abc import ABC


class GetDataFromUser(ABC):
    """This class collects information from the user about desired vacancies and form criteria for search"""

    def __init__(self) -> None:
        """
        Initialization attributes classes
        """
        self.name_vacancy = self.input_vacancy_name()
        self.experience = self.input_experience()

    #
    # Main method
    def get_criteria_from_user(self):
        params = {
                # Parameters for search
                'text': self.name_vacancy,  # Keyword for search (name vacancy or etc.)
                'experience': self.experience  # Experience work
        }
        return params

    # Static methods for getting search criteria
    @staticmethod
    def input_vacancy_name() -> str or None:
        """This method prompts the user for a job title to search for on the site.
        :return: name vacancy or None
        """
        vacancy_name = input('Введите название вакансии для поиска или нажмите Enter, чтобы не искать по: ')
        if vacancy_name == "":
            return None
        return vacancy_name

    @staticmethod
    def input_experience() -> str or None:
        """This method asks the user for their experience in searching the site and returns a dictionary with keys
        to filter the site
        :return dictionary with keys to filter the site or None"""
        dict_experience = \
            {
                range(0, 1): {"hh": "noExperience", 'sj': '1', "name": "Нет опыта"},
                range(1, 3): {"hh": "between1And3", 'sj': '2', "name": "От 1 года до 3 лет"},
                range(3, 6): {"hh": "between3And6", 'sj': '3', "name": "От 3 до 6 лет"},
                range(6, 100): {"hh": "moreThan6", 'sj': '4', "name": "Более 6 лет"}
            }

        count = 0
        while True:
            count += 1
            experience = input(str('Введите ваш опыт работы (в годах, целое число). '
                                   'Если желаете найти вакансии без фильтра "опыт работы" - нажмите Enter: '))

            if experience.strip() == '':
                return None
            elif experience.strip().isdigit():
                for key, value in dict_experience.items():
                    if int(experience) in key:
                        return value['hh']
            print("Вы ввели не корректный опыт")
            if count == 3:
                print(f'Вы {count} раза ввели ваш опыт работы неверно. '
                      'Поиск будет осуществлён без фильтра "Опыт работы".')
                return None
