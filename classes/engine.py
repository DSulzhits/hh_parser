import requests
import json
from abc import ABC, abstractmethod


class Engine(ABC):

    @abstractmethod
    def get_request(self):
        pass


class HH(Engine):
    vacancies_all = []
    vacancies_dicts = []

    def __init__(self, vacancy):
        self.vacancy = vacancy

    def get_request(self):
        for num in range(1):
            url = 'https://api.hh.ru/vacancies'
            vacancies_per_page = 20
            params = {
                'text': {self.vacancy},
                'areas': 113,
                'per_page': vacancies_per_page,
                'page': num,
                'only with salary': True
            }
            response = requests.get(url, params=params)
            info = response.json()
            if info is None:
                return "Данны не получены!"
            elif 'errors' in info:
                return info['errors'][0]['value']
            elif info['found'] == 0:
                return "Нет вакансий"
            else:
                for vacancy in range(vacancies_per_page):
                    self.vacancies_all.append(vacancy)
                    if info['items'][vacancy]['salary'] is not None \
                            and info['items'][vacancy]['salary']['currency'] == 'RUR':
                        vacancy_dict = {'employer': info['items'][vacancy]['employer']['name'],
                                        'name': info['items'][vacancy]['name'],
                                        'url': info['items'][vacancy]['alternate_url'],
                                        'requirement': info['items'][vacancy]['snippet']['requirement'],
                                        'salary_from': info['items'][vacancy]['salary']['from'],
                                        'salary_to': info['items'][vacancy]['salary']['to']}
                        if vacancy_dict['salary_from'] is None:
                            vacancy_dict['salary_from'] = "не указано"
                        elif vacancy_dict['salary_to'] is None:
                            vacancy_dict['salary_to'] = "не указано"
                        self.vacancies_dicts.append(vacancy_dict)
        return self.vacancies_dicts

    @staticmethod
    def make_json(vacancy, vacancies_dicts):
        with open(f"{vacancy}_hh_ru.json", 'w', encoding='utf-8') as file:
            json.dump(vacancies_dicts, file, indent=2, ensure_ascii=False)
        return f"Вакансии добавлены в файл: {vacancy}_hh_ru.json"

    @staticmethod
    def sorting(filename, type_of_sort, vacancies, num_of_vacancies=None):
        vacancies_list = []
        vacancies_sort = sorted(vacancies, key=lambda vacancy: vacancy['salary_from'], reverse=type_of_sort)
        for vacancy in vacancies_sort:
            vacancies_list.append(f"""
        Наниматель: {vacancy['employer']}
        Вакансия: {vacancy['name']}
        Описание/Требования: {vacancy['requirement']}
        Заработная плата от {vacancy['salary_from']} до {vacancy['salary_to']}
        Ссылка на вакансию: {vacancy['url']}""")
        with open(f'{filename}_sorted_vacancies.json', 'w', encoding='utf-8') as file:
            json.dump(vacancies_sort, file, indent=2, ensure_ascii=False)
        return vacancies_list


"""Пример работы"""
# vacancy_to_search = "маляр"
# hh = HH(vacancy_to_search)
# my_vacaincies = hh.get_request()
# print(hh.make_json(vacancy_to_search, my_vacaincies))
# sorted_vacancies = hh.sorting(vacancy_to_search, True, my_vacaincies)
# for vacancy in sorted_vacancies:
#     print(vacancy)
