from rest_framework import status

from recipes.models import Ingredient, Recipe, Tag
from users.models import User


DEBUG = False


def print_(msg):
    if DEBUG:
        print(msg)


def _perform(method, client, url, payload=None):
    if method == 'GET':
        return client.get(url)
    if method == 'POST':
        return client.post(url, payload)
    if method == 'PUT':
        return client.put(url, payload)
    if method == 'PATCH':
        return client.patch(url, payload)
    if method == 'DELETE':
        return client.delete(url)


def confirm_405(self, url, allowed=None, not_allowed=None):
    methods = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')
    if not_allowed is None and allowed is not None:
        for method in allowed:
            method = method.upper()
        not_allowed = set(methods) - set(allowed)
    for method in not_allowed:
        with self.subTest(url=url, method=method):
            self.assertEqual(
                _perform(method, self.authenticated, url).status_code,
                status.HTTP_405_METHOD_NOT_ALLOWED,
            )


def query(self, method, client, url, status_code=status.HTTP_200_OK, response_sample=None, payload=None):
    def response(self, response, status_code, response_sample=None):
        self.assertEqual(response.status_code, status_code)
        if response_sample is not None:
            print_(f'=response.data: {self}\n {response.data}')
            print_('-------------------')
            print_(f'=response_sample: \n {response_sample}')
            print_('===================')
            self.assertEqual(response.data, response_sample)
        return response
    method = method.upper()
    return response(self, _perform(method, client, url, payload), status_code, response_sample)


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
