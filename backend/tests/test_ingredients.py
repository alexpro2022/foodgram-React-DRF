from rest_framework import status

from recipes.models import Ingredient
from .fixtures import (
    AbstractAPITest,
    confirm_405,
)
from .standard_LCRUD import GET_query


RESPONSE_SAMPLE = {
    "id": 1,
    "name": "Капуста",
    "measurement_unit": "г"
}


def get_ingredient(name='Капуста'):
    ingredient, _ = Ingredient.objects.get_or_create(
        name=name,
        measurement_unit='г',
    )
    return ingredient


class IngredientsAPITest(AbstractAPITest):
    """Тестируем API ингредиентов."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.BASE_URL = '/api/ingredients/'
        cls.test_instance = get_ingredient()

    def test_not_allowed_actions(self):
        confirm_405(self, self.get_url(), ['GET'])
        confirm_405(self, self.get_url(True), ['GET'])

    def test_list_action(self):
        URL = self.get_url()
        SEARCH_URL = f'{URL}?name=Кап'
        INVALID_SEARCH_URL = f'{URL}?name=Кар'
        CASES = (
            (URL, [RESPONSE_SAMPLE]),
            (SEARCH_URL, [RESPONSE_SAMPLE]),
            (INVALID_SEARCH_URL, []),
        )
        for url, sample in CASES:
            with self.subTest(url=url):
                GET_query(self, self.client, url, response_sample=sample)

    def test_retrieve_action(self):
        CASES = (
            (self.get_url(True), status.HTTP_200_OK, RESPONSE_SAMPLE),
            (self.get_url(not_found=True), status.HTTP_404_NOT_FOUND, None),
        )
        for url, status_code, sample in CASES:
            with self.subTest(url=url):
                GET_query(self, self.client, url, status_code, sample)
