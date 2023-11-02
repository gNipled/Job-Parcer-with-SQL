import psycopg2
import src.config
import src.constants
import src.query


class DBManager:
    def __init__(self, db_name: str):
        self.db_name = db_name

    def get_companies_and_vacancies_count(self):
        """
        Method to print to console list of employers and number of vacancies for every of them
        """
        with psycopg2.connect(
                host='localhost',
                database=self.db_name,
                user=src.config.PG_USER_NAME,
                password=src.config.PG_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(src.query.select_em_and_vac_counts)
                results = cursor.fetchall()
        conn.close()
        for employer in results:
            print(
                f'{employer[0]} has {employer[1]} vacancies'
            )

    def get_all_vacancies(self):
        """
        Method to get list of all vacancies in database
        """
        with psycopg2.connect(
                host='localhost',
                database=self.db_name,
                user=src.config.PG_USER_NAME,
                password=src.config.PG_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(src.query.select_all_vacancies)
                results = cursor.fetchall()
        conn.close()
        return results

    def get_avg_salary(self):
        """
        Method to print in console average salary
        """
        with psycopg2.connect(
                host='localhost',
                database=self.db_name,
                user=src.config.PG_USER_NAME,
                password=src.config.PG_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(src.query.select_avg_salary)
                results = cursor.fetchone()
        conn.close()
        print(f'Average salary is {int(results[0])}')

    def get_vacancies_with_higher_salary(self):
        """
        Method to get list of vacancies in database with salary higher than average for all vacancies
        """
        with psycopg2.connect(
                host='localhost',
                database=self.db_name,
                user=src.config.PG_USER_NAME,
                password=src.config.PG_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(src.query.select_salary_bigger_then_avg)
                results = cursor.fetchall()
        conn.close()
        return results

    def get_vacancies_with_keyword(self, keyword: str):
        """
        Method to get list of vacancies in database with keyword in vacancy name
        """
        search = f'%{keyword}%'
        with psycopg2.connect(
                host='localhost',
                database=self.db_name,
                user=src.config.PG_USER_NAME,
                password=src.config.PG_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(src.query.select_with_keyword, (search,))
                results = cursor.fetchall()
        conn.close()
        return results
