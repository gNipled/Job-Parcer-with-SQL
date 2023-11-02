import psycopg2
import src.config
import src.constants
import src.query
from src.api import HeadHunterAPI


def create_table(db_name: str):
    """
    Function to create tables "employers" and "vacancies" in database "db_name"
    """
    with psycopg2.connect(
            host='localhost',
            database=db_name,
            user=src.config.PG_USER_NAME,
            password=src.config.PG_PASSWORD
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute(src.query.create_employers)
            cursor.execute(src.query.create_vacancies)
            cursor.execute(src.query.employers_add_constr_pk)
            cursor.execute(src.query.vacancies_add_constr_pk)
            cursor.execute(src.query.vacancies_add_constr_fk_employer_id)
            cursor.execute(src.query.vacancies_add_constr_chk_salary_not_specified)
    conn.close()


def fill_table(db_name: str):
    """
    Function to fill tables "employers" and "vacancies" in database "db_name"
    """
    print('Filling up a table, please wait for a bit')
    with psycopg2.connect(
            host='localhost',
            database=db_name,
            user=src.config.PG_USER_NAME,
            password=src.config.PG_PASSWORD
    ) as conn:
        with conn.cursor() as cursor:
            cursor.executemany(src.query.insert_employers,
                               HeadHunterAPI('').get_employers(src.constants.EMPLOYERS_IDS))
            for employer in src.constants.EMPLOYERS_IDS:
                cursor.executemany(src.query.insert_vacancies,
                                  (HeadHunterAPI(employer).get_vacancies()))
    conn.close()


def clear_table(db_name: str):
    """
    Function to clear tables "employers" and "vacancies" in database "db_name"
    """
    with psycopg2.connect(
            host='localhost',
            database=db_name,
            user=src.config.PG_USER_NAME,
            password=src.config.PG_PASSWORD
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute(src.query.truncate_employers)
            cursor.execute(src.query.truncate_vacancies)
    conn.close()
