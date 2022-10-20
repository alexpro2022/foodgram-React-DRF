from django.urls import reverse
from rest_framework.test import APITestCase

from .fixtures import ROUTES, ROUTES_AMOUNT


class RoutesTest(APITestCase):
    def test_url_corresponds_with_namespace_name(self):
        """Проверка соответствия урл его namespace:name."""
        counter = 0
        for url, name, args in ROUTES:
            counter += 1
            with self.subTest(url=url, name=name):
                self.assertEqual(
                    f'/api/{url}', reverse(f'api:{name}', args=args))
        self.assertEqual(counter, ROUTES_AMOUNT)
