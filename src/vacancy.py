#
#     def authorization_user(self):
#         """Этот метод осуществляет процесс авторизации пользователя на сайте HeadHunters в полном объёме,
#         начиная с получения кода авторизации и, заканчиавая, получением необходимых токенов."""
#         # Тут должен быть код для авторизации пользователя
#         print(f'Авторизация прошла успешно. Необходимые коды и токены получены.\n'
#               f'Код авторизации получен. Код: {self.api_authorization_code}\n'
#               f'Assert-token получен. Токен: {self.api_assert_token}\n'
#               f'Refresher-token получен. Токен: {self.api_refresh_token}\n'
#               f'Вы авторизовались.\n')
#
#     def get_list_favorited_vacanсies(self):
#         params = {
#             'page': 0,
#             'per_page': 20
#         }
#
#         headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                                  'Chrome/121.0.0.0 Safari/537.36',
#                    'Authorization': f'Bearer {self.api_assert_token}'
# }
#
#         response = requests.get(self.api_basic_url + '/vacancies/favorited', params=params, headers=headers)
#         content = response.json()
#         print(content)