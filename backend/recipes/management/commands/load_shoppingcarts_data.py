from csv import DictReader

from django.core.management import BaseCommand

from recipes.models import ShoppingCart, Recipe
from users.models import User
from ._utils import DATA_PATH, info


class Command(BaseCommand):
    CLS = ShoppingCart
    FILE_NAME = CLS.__name__.lower()
    help = f'Loads data from {FILE_NAME}s.csv'

    @info
    def handle(self, *args, **options):
        for row in DictReader(
            open(f'{DATA_PATH}{self.FILE_NAME}s.csv', encoding='utf-8')
        ):
            instance = self.CLS(
                user=User.objects.get(pk=row['user_id']),
                recipe=Recipe.objects.get(pk=row['recipe_id']),
                added=row['added'])
            instance.save()
