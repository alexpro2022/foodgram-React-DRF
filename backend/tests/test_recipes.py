from rest_framework import status

from recipes.models import Recipe, RecipeIngredient
from .fixtures import AbstractAPITest, get_user
from .test_ingredients import create_ingredient, get_ingredient
from .test_tags import create_tag, get_tag
from .utils import (
    confirm_405,
    get_next_pk,
    query,
)


AMOUNT = 500
IMAGE = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=="
IMAGE_FILE = 'temp.png'
IMAGE_FOLDER = Recipe._meta.get_field("image").upload_to
IMAGE_PATH = f'http://testserver/media/{IMAGE_FOLDER}{IMAGE_FILE}'


def create_recipe(author):
    recipe, created = Recipe.objects.get_or_create(
        author=author,
        name='Recipe',
        text='Description',
        image=f'{IMAGE_FOLDER}{IMAGE_FILE}',
        cooking_time=10,
    )
    if created:
        recipe.tags.set([create_tag()])
        RecipeIngredient.objects.get_or_create(
            recipe=recipe,
            ingredient=create_ingredient(),
            amount=AMOUNT,
        )
    return recipe


def get_recipe(reduced=False, ingredient_amount=AMOUNT):
    obj = Recipe.objects.last()
    if reduced:
        return {
            "id": obj.pk,
            "name": obj.name,
            "image": '/media/recipes/images/temp.png',
            "cooking_time": obj.cooking_time,
        }
    return {
        "id": obj.pk,
        "tags": [get_tag()],
        "author": get_user(obj.author),
        "ingredients": [get_ingredient(ingredient_amount)],
        "is_favorited": False,
        "is_in_shopping_cart": False,
        "name": obj.name,
        "image": IMAGE_PATH,
        "text": obj.text,
        "cooking_time": obj.cooking_time
    }


'''
def get_recipe_response_sample(author):
    return {
        "id": 1,
        "tags": [get_tag()],
        "author": get_user(author),
        "ingredients": [get_ingredient(AMOUNT)],
        "is_favorited": False,
        "is_in_shopping_cart": False,
        "name": "Recipe",
        "image": IMAGE_PATH,
        "text": "Description",
        "cooking_time": 10
    }
'''


class RecipesAPITest(AbstractAPITest):
    """Тестируем API рецептов."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.BASE_URL = '/api/recipes/'
        cls.test_instance = create_recipe(cls.author)

    def test_not_allowed_actions(self):
        confirm_405(self, self.get_url(), ['GET', 'POST'])
        confirm_405(self, self.get_url(True), not_allowed=['PUT', 'POST'])

    def test_list_action(self):
        response_sample = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [get_recipe()]
        }
        query(self, 'GET', self.client, self.get_url(), response_sample=response_sample)

    def test_retrieve_action(self):
        CASES = (
            (self.get_url(True), status.HTTP_200_OK, get_recipe()),
            (self.get_url(not_found=True), status.HTTP_404_NOT_FOUND, None),
        )
        for url, status_code, sample in CASES:
            with self.subTest(url=url):
                query(self, 'GET', self.client, url, status_code, sample)

    def test_destroy_action(self):
        CASES = (
            (self.client, status.HTTP_401_UNAUTHORIZED),
            (self.authenticated, status.HTTP_403_FORBIDDEN),
            (self.auth_author, status.HTTP_204_NO_CONTENT),
            (self.auth_author, status.HTTP_404_NOT_FOUND)
        )
        for client, status_code in CASES:
            with self.subTest(client=client):
                query(self, 'DELETE', client, self.get_url(True), status_code)

    def favorite_shopping_cart(self, URL, NOT_FOUND):
        confirm_405(self, URL, ['POST', 'DELETE'])
        CASES = (
            (self.client, URL, status.HTTP_401_UNAUTHORIZED, None),
            (self.authenticated, URL, status.HTTP_201_CREATED, get_recipe(True)),
            (self.authenticated, URL, status.HTTP_400_BAD_REQUEST, None),
            (self.authenticated, NOT_FOUND, status.HTTP_404_NOT_FOUND, None),
        )
        for client, url, status_code, sample in CASES:
            query(self, 'POST', client, url, status_code, sample)

        CASES = (
            (self.client, URL, status.HTTP_401_UNAUTHORIZED),
            (self.authenticated, URL, status.HTTP_204_NO_CONTENT),
            (self.authenticated, URL, status.HTTP_400_BAD_REQUEST),
            (self.authenticated, NOT_FOUND, status.HTTP_404_NOT_FOUND),
        )
        for client, url, status_code in CASES:
            query(self, 'DELETE', client, url, status_code)

    def test_favorite(self):
        URL = f'{self.get_url(True)}favorite/'
        NOT_FOUND = f'{self.get_url(not_found=True)}favorite/'
        self.favorite_shopping_cart(URL, NOT_FOUND)

    def test_shopping_cart(self):
        URL = f'{self.get_url(True)}shopping_cart/'
        NOT_FOUND = f'{self.get_url(not_found=True)}shopping_cart/'
        self.favorite_shopping_cart(URL, NOT_FOUND)

    def test_download_shopping_cart(self):
        URL = f'{self.get_url(True)}shopping_cart/'
        query(self, 'POST', self.authenticated, URL, status.HTTP_201_CREATED, response_sample=get_recipe(True))
        URL = f'{self.get_url()}download_shopping_cart/'
        response_sample = b'\xd0\x9a\xd0\xb0\xd0\xbf\xd1\x83\xd1\x81\xd1\x82\xd0\xb0, \xd0\xb3: - 500\n'
        CASES = (
            (self.client, status.HTTP_401_UNAUTHORIZED),
            (self.authenticated, status.HTTP_200_OK),
        )
        for client, status_code in CASES:
            response = query(self, 'GET', client, URL, status_code=status_code)
        self.assertEqual(response.content, response_sample)

    def test_create_action(self):
        AMOUNT = 111
        TIME = 11
        create_payload = {
            'ingredients': [
                {
                    'id': get_ingredient()['id'],
                    'amount': AMOUNT
                }
            ],
            'tags': [get_tag()['id']],
            'image': IMAGE,
            'name': 'CREATE',
            'text': 'CREATE',
            'cooking_time': TIME
        }
        response_sample = {
            "id": get_next_pk('recipe'),
            "tags": [get_tag()],
            "author": get_user(self.user),
            "ingredients": [get_ingredient(AMOUNT)],
            "is_favorited": False,
            "is_in_shopping_cart": False,
            "image": IMAGE_PATH,
            "name": "CREATE",
            "text": "CREATE",
            "cooking_time": TIME
        }
        invalid_payload = {}
        CASES = (
            (self.client, create_payload, status.HTTP_401_UNAUTHORIZED, None),
            (self.authenticated, create_payload, status.HTTP_201_CREATED, response_sample),
            (self.authenticated, create_payload, status.HTTP_400_BAD_REQUEST, None),
            (self.authenticated, invalid_payload, status.HTTP_400_BAD_REQUEST, None),
        )
        for client, payload, status_code, sample in CASES:
            with self.subTest(status_code=status_code):
                query(self, 'POST', client, self.get_url(), status_code, sample, payload)

    def test_partial_update_action(self):
        AMOUNT = 1000
        TIME = 1
        TEXT = "PATCH"
        payload = {
            "ingredients": [
                {
                    "id": get_ingredient()['id'],
                    "amount": AMOUNT
                }
            ],
            "tags": [get_tag()['id']],
            "text": TEXT,
            "cooking_time": TIME
        }
        response_sample = {
            "id": get_recipe()['id'],
            "tags": [get_tag()],
            "author": get_user(self.author),
            "ingredients": [get_ingredient(amount=1000)],
            "is_favorited": False,
            "is_in_shopping_cart": False,
            "name": get_recipe()['name'],
            'image': IMAGE_PATH,
            "text": TEXT,
            "cooking_time": TIME
        }
        URL = self.get_url(True)
        NOT_FOUND = self.get_url(not_found=True)
        CASES = (
            (self.client, URL, payload, status.HTTP_401_UNAUTHORIZED, None),
            (self.authenticated, URL, payload, status.HTTP_403_FORBIDDEN, None),
            (self.auth_author, URL, payload, status.HTTP_200_OK, response_sample),
            (self.auth_author, NOT_FOUND, payload, status.HTTP_404_NOT_FOUND, None),
        )
        for client, url, load, status_code, sample in CASES:
            with self.subTest(client=client):
                query(self, 'PATCH', client, url, status_code, sample, load)
