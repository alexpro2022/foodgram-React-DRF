from rest_framework import status

from recipes.models import Ingredient
from .fixtures import AbstractAPITest
from .utils import confirm_405, query


def create_ingredient(name='Капуста'):
    ingredient, _ = Ingredient.objects.get_or_create(
        name=name,
        measurement_unit='г',
    )
    return ingredient


def get_ingredient(amount=False):
    obj = Ingredient.objects.last()
    if not amount:
        return {
            "id": obj.pk,
            "name": obj.name,
            "measurement_unit": obj.measurement_unit
        }
    return {
        "id": obj.pk,
        "name": obj.name,
        "measurement_unit": obj.measurement_unit,
        "amount": amount
    }


class IngredientsAPITest(AbstractAPITest):
    """Тестируем API ингредиентов."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.BASE_URL = '/api/ingredients/'
        cls.test_instance = create_ingredient()

    def test_not_allowed_actions(self):
        confirm_405(self, self.get_url(), ['GET'])
        confirm_405(self, self.get_url(True), ['GET'])

    def test_list_action(self):
        URL = self.get_url()
        SEARCH_URL = f'{URL}?name=Кап'
        INVALID_SEARCH_URL = f'{URL}?name=Кар'
        CASES = (
            (URL, [get_ingredient()]),
            (SEARCH_URL, [get_ingredient()]),
            (INVALID_SEARCH_URL, []),
        )
        for url, sample in CASES:
            with self.subTest(url=url):
                query(self, 'GET', self.client, url, response_sample=sample)

    def test_retrieve_action(self):
        CASES = (
            (self.get_url(True), status.HTTP_200_OK, get_ingredient()),
            (self.get_url(not_found=True), status.HTTP_404_NOT_FOUND, None),
        )
        for url, status_code, sample in CASES:
            with self.subTest(url=url):
                query(self, 'GET', self.client, url, status_code, sample)
