import requests
from abc import ABC, abstractmethod


class AbstractAPI(ABC):
    """Abstract class for APIs"""

    @abstractmethod
    def get_vacancies(self):
        """Method for parsing vacancy sites"""
        pass


class HeadHunterAPI(AbstractAPI):
    """Class for hh.ru API"""

    def __init__(self, employer_id: str):
        self.employer_id = employer_id

    def __str__(self):
        return {self.employer_id}

    def __repr__(self):
        return f"{self.__class__.__name__}({self.employer_id})"

    def get_vacancies(self):
        """
        Method for parsing hh.ru for vacancy by 'employer_id'
        :return list
        """
        page = 0
        output = []
        response = requests.get(f'https://api.hh.ru/vacancies', headers={'User-Agent': 'job parser for study'},
                                params={'per_page': 100, 'employer_id': self.employer_id, 'area': '113'})
        if response.status_code != 200:
            return list(set(output))
        total_pages = int(response.json()['pages'])
        if total_pages > 15:
            total_pages = 15
        while page <= total_pages:
            response = requests.get(f'https://api.hh.ru/vacancies', headers={'User-Agent': 'job parser for study'},
                                    params={'per_page': 100, 'employer_id': self.employer_id, 'area': '113',
                                            'page': page})
            for vacancy in response.json()['items']:
                if response.status_code != 200:
                    return list(set(output))
                if vacancy['salary'] is None:
                    output.append((vacancy['id'], vacancy['name'], vacancy['alternate_url'], vacancy['employer']['id'],
                                   1, None, None, None, vacancy['schedule']['name'], vacancy['employment']['name']))
                else:
                    output.append((vacancy['id'], vacancy['name'], vacancy['alternate_url'], vacancy['employer']['id'],
                                   0, vacancy['salary']['from'], vacancy['salary']['to'], vacancy['salary']['currency'],
                                   vacancy['schedule']['name'], vacancy['employment']['name']))
            page += 1
        return list(set(output))

    @staticmethod
    def get_employers(employers_ids: tuple):
        """
        Statick method to get list of employers information to fill employers table in database
        """
        output = []
        for employer in employers_ids:
            response = requests.get(f'https://api.hh.ru/employers/{employer}')
            output.append((response.json()['id'], response.json()['name'], response.json()['alternate_url']))
        return output
