

class Vacancy:

    def __init__(self, db_vacancy):
        self.vacancy_id = db_vacancy.vacancy_id
        self.name = db_vacancy.name
        self.salary_from = db_vacancy.salary_from
        self.salary_to = db_vacancy.salary_to
        self.salary_currency = db_vacancy.salary_currency

    def __str__(self):
        return f'Вакансия: {self.name} (id № {self.vacancy_id}). Зарплата: {self.salary_from}-{self.salary_to}'
