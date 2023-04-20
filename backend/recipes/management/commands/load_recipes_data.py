from csv import DictReader

from django.core.management import BaseCommand

from recipes.models import Recipe
from users.models import User
from ._utils import DATA_PATH, info


class Command(BaseCommand):
    CLS = Recipe
    FILE_NAME = CLS.__name__.lower()
    help = f'Loads data from {FILE_NAME}s.csv'

    @info
    def handle(self, *args, **options):
        for row in DictReader(
            open(f'{DATA_PATH}{self.FILE_NAME}s.csv', encoding='utf-8')
        ):
            instance = self.CLS(
                author=User.objects.get(pk=row['author_id']),
                name=row['name'],
                text=row['text'],
                created=row['created'],
                cooking_time=row['cooking_time'])
            instance.save()
            instance.tags.set(row['tags'])
