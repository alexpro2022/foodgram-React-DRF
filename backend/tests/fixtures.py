import shutil
import tempfile

from django.conf import settings
from django.test import override_settings
from rest_framework.test import APIClient, APITestCase

from users.models import User

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
ANOTHER = {
    'email': 'another@another.com',
    'username': 'test_another',
    'first_name': 'first_name_Another',
    'last_name': 'last_name_Another',
    'password': 'X123C234V345@_Another',
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

        cls.another = create_user(ANOTHER)

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
