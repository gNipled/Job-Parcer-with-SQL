import src.constants
import src.config
import psycopg2
import psycopg2.errors
from src.dbmanager import DBManager
from src.table_functions import clear_table, create_table, fill_table


def start_screen():
    """
    Starting screen for user interaction
    """
    print(
        f"Hi! If you haven't created tables yet, please select create table"
        f"To quit program type one of these commands: {src.constants.EXIT_WORDS}"
    )
    while True:
        print(
            f"{src.constants.USER_RESPONSE_CREATE_TABLE}: create table in your database and fill it\n"
            f"{src.constants.USER_RESPONSE_FILL_TABLE}: clear and fill table with new vacancies\n"
            f"{src.constants.USER_RESPONSE_VAC_COUNT}: show number of vacancies for companies\n"
            f"{src.constants.USER_RESPONSE_ALL_VAC}: show all vacancies\n"
            f"{src.constants.USER_RESPONSE_AVG_SALARY}: show average salary for all vacancies\n"
            f"{src.constants.USER_RESPONSE_HIGHER_THAN_AVG_SALARY}: show all vacancies with higher than average salary\n"
            f"{src.constants.USER_RESPONSE_KEYWORD}: search for vacancies by keyword\n"
        )
        user_input = input('Your choice: ').lower()
        check_for_quit(user_input)
        if user_input in src.constants.VIABLE_RESPONSES:
            return user_input
        elif user_input == src.constants.USER_RESPONSE_CREATE_TABLE:
            try:
                create_table(src.config.PG_DB_NAME)
                fill_table(src.config.PG_DB_NAME)
            except psycopg2.OperationalError:
                print(f'Seems like there is no database with name {src.config.PG_DB_NAME}, please create it')
                quit('Thanks for using')
        elif user_input == src.constants.USER_RESPONSE_FILL_TABLE:
            try:
                clear_table(src.config.PG_DB_NAME)
                fill_table(src.config.PG_DB_NAME)
            except psycopg2.errors.UndefinedTable:
                print('Please create table first')
                continue
            except psycopg2.OperationalError:
                print(f'Seems like there is no database with name {src.config.PG_DB_NAME}, please create it')
                quit('Thanks for using')
        else:
            print('Please input viable command!\n')
            continue


def check_for_quit(user_input):
    """
    Function to check user input for exit commands, to close program
    """
    if user_input.lower() in src.constants.EXIT_WORDS:
        quit('Thanks for using')
    else:
        return user_input


def vacancy_print(vacancies_list: list):
    """
     Function to print to console found vacancies
    """
    for vacancy in vacancies_list:
        if vacancy[4] == 1:
            salary_str = 'not specified'
        elif vacancy[5] is None:
            salary_str = f'{vacancy[6]} {vacancy[7]}'
        elif vacancy[6] is None:
            salary_str = f'{vacancy[5]} {vacancy[7]}'
        else:
            salary_str = f'{vacancy[5]} - {vacancy[6]} {vacancy[7]}'
        print(
            f'Name: {vacancy[1]}\n'
            f'Salary: {salary_str}\n'
            f'Schedule: {vacancy[8]}\n'
            f'Employment: {vacancy[9]}\n'
            f'Link: {vacancy[2]}'
        )


def user_interaction():
    """
    Main user interaction function
    """
    while True:
        user_input = start_screen()
        db_manager = DBManager(src.config.PG_DB_NAME)
        if user_input == src.constants.USER_RESPONSE_VAC_COUNT:
            try:
                db_manager.get_companies_and_vacancies_count()
                check_for_quit(input('Press Enter to start over'))
                continue
            except psycopg2.errors.UndefinedTable:
                print('Please create table first')
                continue
            except psycopg2.OperationalError:
                print(f'Seems like there is no database with name {src.config.PG_DB_NAME}, please create it')
                quit('Thanks for using')
        elif user_input == src.constants.USER_RESPONSE_ALL_VAC:
            try:
                vacancy_print(db_manager.get_all_vacancies())
                check_for_quit(input('Press Enter to start over'))
                continue
            except psycopg2.errors.UndefinedTable:
                print('Please create table first')
                continue
            except psycopg2.OperationalError:
                print(f'Seems like there is no database with name {src.config.PG_DB_NAME}, please create it')
                quit('Thanks for using')
        elif user_input == src.constants.USER_RESPONSE_AVG_SALARY:
            try:
                db_manager.get_avg_salary()
                check_for_quit(input('Press Enter to start over'))
                continue
            except psycopg2.errors.UndefinedTable:
                print('Please create table first')
                continue
            except psycopg2.OperationalError:
                print(f'Seems like there is no database with name {src.config.PG_DB_NAME}, please create it')
                quit('Thanks for using')
        elif user_input == src.constants.USER_RESPONSE_HIGHER_THAN_AVG_SALARY:
            try:
                vacancy_print(db_manager.get_vacancies_with_higher_salary())
                check_for_quit(input('Press Enter to start over'))
                continue
            except psycopg2.errors.UndefinedTable:
                print('Please create table first')
                continue
            except psycopg2.OperationalError:
                print(f'Seems like there is no database with name {src.config.PG_DB_NAME}, please create it')
                quit('Thanks for using')
        elif user_input == src.constants.USER_RESPONSE_KEYWORD:
            print(f'Input keyword for search in vacancies names')
            try:
                vacancy_print(db_manager.get_vacancies_with_keyword(check_for_quit(input('Keyword: '))))
                check_for_quit(input('Press Enter to start over'))
                continue
            except psycopg2.errors.UndefinedTable:
                print('Please create table first')
                continue
            except psycopg2.OperationalError:
                print(f'Seems like there is no database with name {src.config.PG_DB_NAME}, please create it')
                quit('Thanks for using')
