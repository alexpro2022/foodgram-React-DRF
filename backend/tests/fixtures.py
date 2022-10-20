import shutil
import tempfile

from django.conf import settings
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from users.models import User


DEBUG = False


def print_(msg):
    if DEBUG:
        print(msg)


def get_user():
    try:
        return User.objects.create_user(
            email='user@user.ru',
            username='test-user',
            first_name='User',
            last_name='User',
            password='User',
        )
    except Exception:
        return User.objects.get(
            email='user@user.ru',
            username='test-user',
        )


USER = get_user()
USER_RESPONSE_SAMPLE = {
    "email": USER.email,
    "id": USER.id,
    "username": USER.username,
    "first_name": USER.first_name,
    "last_name": USER.last_name,
    "is_subscribed": False
}


def get_author():
    try:
        return User.objects.create_user(
            email='author@author.ru',
            username='test-author',
            first_name='Author',
            last_name='Author',
            password='Author',
        )
    except Exception:
        return User.objects.get(
            email='author@author.ru',
            username='test-author',
        )


AUTHOR = get_author()
AUTHOR_RESPONSE_SAMPLE = {
    "email": AUTHOR.email,
    "id": AUTHOR.id,
    "username": AUTHOR.username,
    "first_name": AUTHOR.first_name,
    "last_name": AUTHOR.last_name,
    "is_subscribed": False
}

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class AbstractAPITest(APITestCase):
    """Абстрактный класс для тестирования API."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # clients for testing access rights to object(s)
        cls.user = USER
        cls.authenticated = APIClient()
        cls.authenticated.force_authenticate(cls.user)

        cls.author = AUTHOR
        cls.auth_author = APIClient()
        cls.auth_author.force_authenticate(cls.author)

        # ===to be overriden===
        cls.BASE_URL = None
        cls.test_instance = None

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def get_url(self, detail=False, not_found=False):
        if not_found:
            return f'{self.BASE_URL}{self.test_instance.id+100}/'
        if detail:
            return f'{self.BASE_URL}{self.test_instance.id}/'
        return self.BASE_URL


def check_response(self, url, method):
    method = method.upper()
    client = self.authenticated
    if method == 'GET':
        return client.get(url)
    if method == 'POST':
        return client.post(url)
    if method == 'PUT':
        return client.put(url)
    if method == 'PATCH':
        return client.patch(url)
    if method == 'DELETE':
        return client.delete(url)


def confirm_405(self, url, allowed=None, not_allowed=None):
    methods = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')
    if not_allowed is None:
        not_allowed = set(methods) - set(allowed)
    for method in not_allowed:
        with self.subTest(method=method):
            self.assertEqual(
                check_response(self, url, method).status_code,
                status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        print_(f'{method} not allowed')
    print_(f'===confirm_405 for {url}: {allowed} - OK===')


'''
      env:
        DB: postgres
        DB_HOST: 127.0.0.1
        DB_PORT: 5432
        DB_PASSWORD: 12345
'''
