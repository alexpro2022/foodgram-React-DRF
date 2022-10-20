from rest_framework import status

from .fixtures import (
    AUTHOR_RESPONSE_SAMPLE,
    USER_RESPONSE_SAMPLE,
    AbstractAPITest,
    confirm_405,
    print_,
)
from .standard_LCRUD import (
    GET_query,
    POST_query,
    DELETE_query,
)
from .test_recipes import get_recipe, RECIPE


class UsersAPITest(AbstractAPITest):
    """Тестируем API пользователей."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.BASE_URL = '/api/users/'
        cls.test_instance = cls.user

    def test_not_allowed_actions(self):
        confirm_405(self, self.get_url(), ['GET', 'POST'])
        confirm_405(self, self.get_url(True), ['GET', 'DELETE'])

    def test_list_action(self):
        URL = self.get_url()
        response_sample = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [USER_RESPONSE_SAMPLE, AUTHOR_RESPONSE_SAMPLE]
        }
        URL_page1 = f'{URL}?page=1&limit=1'
        response_sample1 = {
            "count": 2,
            "next": "http://testserver/api/users/?limit=1&page=2",
            "previous": None,
            "results": [USER_RESPONSE_SAMPLE]
        }
        URL_page2 = f'{URL}?page=2&limit=1'
        response_sample2 = {
            "count": 2,
            "next": None,
            "previous": "http://testserver/api/users/?limit=1",
            "results": [AUTHOR_RESPONSE_SAMPLE]
        }
        URL_page3 = f'{URL}?page=3&limit=1'
        CASES = (
            (URL, status.HTTP_200_OK, response_sample),
            (URL_page1, status.HTTP_200_OK, response_sample1),
            (URL_page2, status.HTTP_200_OK, response_sample2),
            (URL_page3, status.HTTP_404_NOT_FOUND, None),
        )
        for url, status_code, sample in CASES:
            with self.subTest(url=url):
                GET_query(self, self.client, url, status_code, sample)

    def test_retrieve_action(self):
        CASES = (
            (self.client, self.get_url(True), status.HTTP_401_UNAUTHORIZED, None),
            (self.authenticated, self.get_url(True), status.HTTP_200_OK, USER_RESPONSE_SAMPLE),
            (self.authenticated, self.get_url(not_found=True), status.HTTP_404_NOT_FOUND, None)
        )
        for client, url, status_code, sample in CASES:
            with self.subTest(client=client, url=url):
                GET_query(self, client, url, status_code, sample)

    def test_create_action(self):
        create_payload = {
            'email': 'create@create.com',
            'username': 'create_username',
            'first_name': 'first_name_CREATE',
            'last_name': 'last_name_CREATE',
            'password': 'X123C234V345@_',
        }
        response_sample = {
            "id": 3,
            "email": "create@create.com",
            "username": "create_username",
            "first_name": "first_name_CREATE",
            "last_name": "last_name_CREATE"
        }
        invalid_payload = {
            'email': 'create_create.com',
            'username': 'me',
            'first_name': '',
            'last_name': '',
            'password': '111',
        }
        CASES = (
            (create_payload, status.HTTP_201_CREATED, response_sample),
            (create_payload, status.HTTP_400_BAD_REQUEST, None),
            (invalid_payload, status.HTTP_400_BAD_REQUEST, None),
        )
        for payload, status_code, sample in CASES:
            with self.subTest(status_code=status_code):
                POST_query(
                    self, self.client, self.get_url(),
                    payload, status_code, sample)

    def test_ME_action(self):
        URL = f'{self.get_url()}me/'
        confirm_405(self, URL, ['GET', 'DELETE'])  # DELETE -400
        CASES = (
            (self.client, status.HTTP_401_UNAUTHORIZED, None),
            (self.authenticated, status.HTTP_200_OK, USER_RESPONSE_SAMPLE),
            (self.auth_author, status.HTTP_200_OK, AUTHOR_RESPONSE_SAMPLE),
        )
        for client, status_code, sample in CASES:
            with self.subTest(client=client):
                GET_query(self, client, URL, status_code, sample)
        print_('===ME - OK===')

    def test_SET_PASSWORD_action(self):
        URL = f'{self.get_url()}set_password/'
        new_password = 'X123C234V345@_'
        payload = {
            "current_password": "User",
            "new_password": new_password,
        }
        CASES = (
            (self.client, status.HTTP_401_UNAUTHORIZED),
            (self.authenticated, status.HTTP_204_NO_CONTENT),
            (self.authenticated, status.HTTP_400_BAD_REQUEST),
        )
        for client, status_code in CASES:
            with self.subTest(client=client, status_cose=status_code):
                POST_query(self, client, URL, payload, status_code)
        print_('===SET_PASSWORD - OK===')

    def test_LOGIN_action(self):
        URL = '/api/auth/token/login/'
        payload = {
            'email': self.user.email,
            'password': 'User',
        }
        response = self.client.post(URL, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data.get('auth_token'), str)
        print_('===LOGIN - OK===')

    def test_LOGOUT_actions(self):
        URL = '/api/auth/token/logout/'
        CASES = (
            (self.client, status.HTTP_401_UNAUTHORIZED),
            (self.authenticated, status.HTTP_204_NO_CONTENT),
        )
        for client, status_code in CASES:
            with self.subTest(client=client):
                response = client.post(URL)
                self.assertEqual(response.status_code, status_code)
        print_('===LOGOUT - OK===')

    def _get_subscribe_response_sample(self):
        response_sample = AUTHOR_RESPONSE_SAMPLE.copy()
        response_sample['is_subscribed'] = True
        response_sample.update({"recipes": [RECIPE], "recipes_count": 1})
        print_(f'===subscribe_response_sample {response_sample}')
        return response_sample

    def test_subscribe(self):
        self.test_instance = self.author
        get_recipe(self.test_instance)
        URL = f'{self.get_url(True)}subscribe/'
        NOT_FOUND = f'{self.get_url(not_found=True)}subscribe/'
        confirm_405(self, URL, ['POST', 'DELETE'])
        response_sample = self._get_subscribe_response_sample()
        SUBSCRIBE_CASES = (
            (self.client, URL, status.HTTP_401_UNAUTHORIZED, None),
            (self.auth_author, URL, status.HTTP_400_BAD_REQUEST, None),
            (self.authenticated, URL, status.HTTP_201_CREATED, response_sample),
            (self.authenticated, URL, status.HTTP_400_BAD_REQUEST, None),
            (self.authenticated, NOT_FOUND, status.HTTP_404_NOT_FOUND, None),
        )
        for client, url, status_code, sample in SUBSCRIBE_CASES:
            with self.subTest(method='subscribe', client=client):
                POST_query(self, client, url, None, status_code, sample)

        UNSUBSCRIBE_CASES = (
            (self.client, URL, status.HTTP_401_UNAUTHORIZED),
            (self.auth_author, URL, status.HTTP_400_BAD_REQUEST),
            (self.authenticated, URL, status.HTTP_204_NO_CONTENT),
            (self.authenticated, URL, status.HTTP_400_BAD_REQUEST),
            (self.authenticated, NOT_FOUND, status.HTTP_404_NOT_FOUND),
        )
        for client, url, status_code in UNSUBSCRIBE_CASES:
            with self.subTest(method='unsubscribe', client=client):
                DELETE_query(self, client, url, status_code)
        print_('===SUBSCRIBE - OK===')

    def test_subscriptions(self):
        self.test_instance = self.author
        get_recipe(self.test_instance)
        URL = f'{self.get_url()}subscriptions/'
        confirm_405(self, URL, ['GET'])
        POST_query(
            self, self.authenticated,
            f'{self.get_url()}{self.test_instance.id}/subscribe/')
        response_sample = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [self._get_subscribe_response_sample()]
        }
        CASES = (
            (self.client, status.HTTP_401_UNAUTHORIZED, None),
            (self.authenticated, status.HTTP_200_OK, response_sample),
        )
        for client, status_code, sample in CASES:
            with self.subTest(client=client):
                GET_query(self, client, URL, status_code, sample)
        print_('===SUBSCRIPTIONS - OK===')