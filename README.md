Для работы с проектом нужно
создать файл config.ini со следующими параметрами:

[postgresql]
dbname=postgres
host=localhost
user=postgres
password=your_password
port=5432

; Configuration for database db_vacancies
[database_vacancies]
dbname=db_vacancies
host=localhost
user=postgres
password=your_password
port=5432

; Configuration for API HeadHunters
[params_api_hh]
redirect_uri = your_redirect_uri
client_id = your_client_id
client_secret = your_client_secret
api_authorization_code = your_api_authorization_code
api_assert_token = your_api_assert_token
api_refresh_token = your_api_refresh_token