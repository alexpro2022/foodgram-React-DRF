import shutil
import tempfile

from django.conf import settings
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from recipes.models import Ingredient, Recipe, Tag
from users.models import User


DEBUG = False


def print_(msg):
    if DEBUG:
        print(msg)


USER = {
    'email': 'user@user.com',
    'username': 'test_user',
    'first_name': 'first_name_User',
    'last_name': 'last_name_User',
    'password': 'X123C234V345@_User',
}
AUTHOR = {
    'email': 'author@author.com',
    'username': 'test_author',
    'first_name': 'first_name_Author',
    'last_name': 'last_name_Author',
    'password': 'X123C234V345@_Author',
}


def create_user(user):
    return User.objects.create_user(
        email=user['email'],
        username=user['username'],
        first_name=user['first_name'],
        last_name=user['last_name'],
        password=user['password'],
    )


def get_user(user, is_subscribed=False):
    return {
        "email": user.email,
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_subscribed": is_subscribed
    }


def get_next_pk(model='user'):
    model = model.upper()
    if model == 'USER':
        model = User
    elif model == 'TAG':
        model = Tag
    elif model == 'RECIPE':
        model = Recipe
    elif model == 'INGREDIENT':
        model = Ingredient
    return model.objects.last().pk + 1


TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class AbstractAPITest(APITestCase):
    """Абстрактный класс для тестирования API."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # clients for testing access rights to object(s)
        cls.user = create_user(USER)
        cls.authenticated = APIClient()
        cls.authenticated.force_authenticate(cls.user)

        cls.author = create_user(AUTHOR)
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
def print_model_(model):
    print_(f'==={model.__name__}=== ')
    for field in model._meta.get_fields(parent=False):
        print_(f'{field.__name__}: {model._meta.get_field(field).value_from_object(
                    self.test_instance)}')
def compare(self, data):
    print_(f'===compare=== {self}')
    for field in self.test_fields:
        with self.subTest(field=field):
            self.assertEqual(
                self.model._meta.get_field(field).value_from_object(
                    self.test_instance),
                data.get(field),
            )
            print_(f'{self.model.__name__}: {field}: {data.get(field)}')


def get_url(self, detail=True, not_found=False):
    if not_found:
        return f'{self.BASE_URL}not_found/'
    if not detail:
        return self.BASE_URL
    if self.DETAIL_URL is not None:  # for non-standard cases
        return self.DETAIL_URL  # when URL is not a BASE_URL/id/
    return f'{self.BASE_URL}{self.test_instance.id}/'  # standard case


def _response(self, client, action):
    action = action.upper()
    if action == 'LIST':
        return client.get(get_url(self, detail=False))
    if action == 'CREATE':
        return client.post(get_url(self, detail=False), self.create_payload)
    if action == 'RETRIEVE':
        return client.get(get_url(self))
    if action == 'UPDATE':
        return client.put(get_url(self), self.put_payload)
    if action == 'PARTIAL_UPDATE':
        return client.patch(get_url(self), self.patch_payload)
    if action == 'DESTROY':
        return client.delete(get_url(self))


def action_not_allowed(self, action, response):
    action = action.upper()
    if action not in self.allowed_actions:
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        print_('=action not allowed=')
        return True
    return False


def check_access(self, action):
    def confirm_401(client):
        self.assertEqual(
            _response(self, client, action).status_code,
            status.HTTP_401_UNAUTHORIZED)

    action = action.upper()
    permission = self.allowed_actions.get(action)
    if permission == 'authenticated':
        confirm_401(self.client)
    elif permission == 'auth_author':
        confirm_401(self.client)
        confirm_401(self.authenticated)


def get_response(self, client, action):
    response = _response(self, client, action)
    if action_not_allowed(self, action, response):
        return
    check_access(self, action)
    return response


'''
