create_employers = (
    'CREATE TABLE employers '
    '('
    'employer_id int NOT NULL, '
    'employer_name varchar(80) NOT NULL, '
    'employer_url varchar(30)'
    ')'
)
create_vacancies = (
    'CREATE TABLE vacancies '
    '('
    'vacancy_id int NOT NULL, '
    'vacancy_name varchar(100) NOT NULL,'
    'vacancy_url varchar(30) NOT NULL, '
    'employer_id int NOT NULL, '
    'salary_not_specified smallint NOT NULL, '
    'salary_from int, '
    'salary_to int, '
    'salary_currency varchar(5), '
    'schedule varchar(20), '
    'employment varchar(20)'
    ')'
)
insert_employers = 'INSERT INTO employers VALUES (%s, %s, %s)'
employers_add_constr_pk = 'ALTER TABLE employers ADD CONSTRAINT pk_employers_employer_id PRIMARY KEY (employer_id)'
vacancies_add_constr_pk = 'ALTER TABLE vacancies ADD CONSTRAINT pk_vacancies_vacancy_id PRIMARY KEY (vacancy_id)'
vacancies_add_constr_fk_employer_id = ('ALTER TABLE vacancies ADD CONSTRAINT fk_vacancies_employer_id '
                                       'FOREIGN KEY (employer_id) REFERENCES employers(employer_id)')
vacancies_add_constr_chk_salary_not_specified = (
    'ALTER TABLE vacancies ADD CONSTRAINT chk_vacancies_salary_not_specified '
    'CHECK (salary_not_specified IN (0, 1))')
insert_vacancies = 'INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
truncate_employers = 'TRUNCATE TABLE employers RESTART IDENTITY CASCADE'
truncate_vacancies = 'TRUNCATE TABLE vacancies RESTART IDENTITY'
select_em_and_vac_counts = ('SELECT DISTINCT employer_name, COUNT(*) '
                            'FROM vacancies '
                            'JOIN employers USING (employer_id) '
                            'GROUP BY employer_name '
                            'ORDER BY COUNT(*) DESC')
select_all_vacancies = 'SELECT * FROM vacancies'
select_avg_salary = 'SELECT AVG(salary_from) FROM vacancies'
select_salary_bigger_then_avg = ('SELECT * '
                                 'FROM vacancies '
                                 'WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies) '
                                 'OR salary_to > (SELECT AVG(salary_to) FROM vacancies)')
select_with_keyword = ('SELECT * '
                       'FROM vacancies '
                       'WHERE vacancy_name LIKE %s')
