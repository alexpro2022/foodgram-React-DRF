from rest_framework import status

from recipes.models import (
    Favorites,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
)
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


def create_recipe(author, tag='breakfast'):
    recipe, created = Recipe.objects.get_or_create(
        author=author,
        name='Recipe',
        text='Description',
        image=f'{IMAGE_FOLDER}{IMAGE_FILE}',
        cooking_time=10,
    )
    if created:
        recipe.tags.set([create_tag(tag)])
        RecipeIngredient.objects.get_or_create(
            recipe=recipe,
            ingredient=create_ingredient(),
            amount=AMOUNT,
        )
    return recipe


def get_recipe(reduced=False, ingredient_amount=AMOUNT):
    obj = Recipe.objects.order_by('id').last()
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
        author_recipe = get_recipe()
        create_recipe(self.user, 'lunch')
        user_recipe = get_recipe()

        URL = self.get_url()
        response_sample = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [author_recipe, user_recipe]
        }

        # ---PAGINATION---
        URL_page1 = f'{URL}?page=1&limit=1'
        response_page1 = {
            "count": 2,
            "next": "http://testserver/api/recipes/?limit=1&page=2",
            "previous": None,
            "results": [author_recipe]
        }
        URL_page2 = f'{URL}?page=2&limit=1'
        response_page2 = {
            "count": 2,
            "next": None,
            "previous": "http://testserver/api/recipes/?limit=1",
            "results": [user_recipe]
        }
        URL_page3 = f'{URL}?page=3&limit=1'
        PAGINATION_CASES = (
            (URL_page1, status.HTTP_200_OK, response_page1),
            (URL_page2, status.HTTP_200_OK, response_page2),
            (URL_page3, status.HTTP_404_NOT_FOUND, None),
        )

        # ---FILTERING - author
        URL_author = f'{URL}?author={self.test_instance.author.id}'
        response_author = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [author_recipe]
        }
        URL_user = f'{URL}?author={self.user.id}'
        response_user = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [user_recipe]
        }
        URL_another = f'{URL}?author={self.another.id}'
        empty_response_sample = {
            "count": 0,
            "next": None,
            "previous": None,
            "results": []
        }
        URL_invalid_author = f'{URL}?author={self.test_instance.author.id+10}'
        AUTHOR_CASES = (
            (URL_author, status.HTTP_200_OK, response_author),
            (URL_user, status.HTTP_200_OK, response_user),
            (URL_another, status.HTTP_200_OK, empty_response_sample),
            (URL_invalid_author, status.HTTP_400_BAD_REQUEST, None),
        )

        # ---FILTERING - tags
        URL_tags = f'{URL}?tags=breakfast&tags=lunch'
        URL_breakfast = f'{URL}?tags=breakfast'
        response_breakfast = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [author_recipe]
        }
        URL_lunch = f'{URL}?tags=lunch'
        response_lunch = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [user_recipe]
        }
        URL_invalid_tag = f'{URL}?tags=asf123'
        TAGS_CASES = (
            (URL_tags, status.HTTP_200_OK, response_sample),
            (URL_breakfast, status.HTTP_200_OK, response_breakfast),
            (URL_lunch, status.HTTP_200_OK, response_lunch),
            (URL_invalid_tag, status.HTTP_400_BAD_REQUEST, None),
        )
        URL_is_favorited = f'{URL}?is_favorited=1'
        URL_is_in_shopping_cart = f'{URL}?is_in_shopping_cart=1'

        CASES_for_anonymous_user = (
            (URL, status.HTTP_200_OK, response_sample),
            *PAGINATION_CASES,
            *AUTHOR_CASES,
            *TAGS_CASES,
            (URL_is_favorited, status.HTTP_200_OK, response_sample),
            (URL_is_in_shopping_cart, status.HTTP_200_OK, response_sample),
        )
        for url, status_code, sample in CASES_for_anonymous_user:
            with self.subTest(url=url):
                query(self, 'GET', self.client, url, status_code, sample)

        # ---FILTERING - favorites
        Favorites.objects.create(
            user=self.user,
            recipe=self.test_instance,
        )
        author_recipe['is_favorited'] = True
        URL_is_not_favorited = f'{URL}?is_favorited=0'
        CASES_favorite = (
            (self.authenticated, URL_is_favorited, status.HTTP_200_OK, response_author),
            (self.authenticated, URL_is_not_favorited, status.HTTP_200_OK, response_sample),
            (self.auth_author, URL_is_favorited, status.HTTP_200_OK, empty_response_sample),
        )

        # ---FILTERING - shopping_cart
        ShoppingCart.objects.create(
            user=self.user,
            recipe=self.test_instance,
        )
        author_recipe['is_in_shopping_cart'] = True
        URL_is_not_in_shopping_cart = f'{URL}?is_in_shopping_cart=0'
        CASES_shopping_cart = (
            (self.authenticated, URL_is_in_shopping_cart, status.HTTP_200_OK, response_author),
            (self.authenticated, URL_is_not_in_shopping_cart, status.HTTP_200_OK, response_sample),
            (self.auth_author, URL_is_in_shopping_cart, status.HTTP_200_OK, empty_response_sample),
        )

        CASES_for_authenticated_users = (
            *CASES_favorite,
            *CASES_shopping_cart,
        )
        for client, url, status_code, sample in CASES_for_authenticated_users:
            with self.subTest(client=client, url=url):
                query(self, 'GET', client, url, status_code, sample)

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
