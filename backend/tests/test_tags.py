from rest_framework import status

from recipes.models import Tag
from .fixtures import AbstractAPITest
from .utils import confirm_405, query


def create_tag(unique_slug='breakfast'):
    tag, _ = Tag.objects.get_or_create(
        name='Завтрак',
        color='#E26C2D',
        slug=unique_slug,
    )
    return tag


def get_tag():
    obj = Tag.objects.order_by('id').last()
    return {
        "id": obj.pk,
        "name": obj.name,
        "color": obj.color,
        "slug": obj.slug,
    }


class TagsAPITest(AbstractAPITest):
    """Тестируем API тегов."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.BASE_URL = '/api/tags/'
        cls.test_instance = create_tag()

    def test_not_allowed_actions(self):
        confirm_405(self, self.get_url(), ['GET'])
        confirm_405(self, self.get_url(True), ['GET'])

    def test_list_action(self):
        query(self, 'GET', self.client, self.get_url(), response_sample=[get_tag()])

    def test_retrieve_action(self):
        CASES = (
            (self.get_url(True), status.HTTP_200_OK, get_tag()),
            (self.get_url(not_found=True), status.HTTP_404_NOT_FOUND, None),
        )
        for url, status_code, sample in CASES:
            with self.subTest(url=url):
                query(self, 'GET', self.client, url, status_code, sample)
