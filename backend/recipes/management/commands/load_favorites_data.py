from csv import DictReader

from django.core.management import BaseCommand

from recipes.models import Favorites, Recipe
from users.models import User
from ._utils import DATA_PATH, info


class Command(BaseCommand):
    CLS = Favorites
    FILE_NAME = CLS.__name__.lower()
    help = f'Loads data from {FILE_NAME}.csv'

    @info
    def handle(self, *args, **options):
        for row in DictReader(
            open(f'{DATA_PATH}{self.FILE_NAME}.csv', encoding='utf-8')
        ):
            instance = self.CLS(
                user=User.objects.get(pk=row['user_id']),
                recipe=Recipe.objects.get(pk=row['recipe_id']),
                added=row['added'])
            instance.save()
