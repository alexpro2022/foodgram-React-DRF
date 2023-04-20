from csv import DictReader

from django.core.management import BaseCommand

from recipes.models import Ingredient, Recipe, RecipeIngredient
from ._utils import DATA_PATH, info


class Command(BaseCommand):
    CLS = RecipeIngredient
    FILE_NAME = 'recipe_ingredient'
    help = f'Loads data from {FILE_NAME}s.csv'

    @info
    def handle(self, *args, **options):
        for row in DictReader(
            open(f'{DATA_PATH}{self.FILE_NAME}s.csv', encoding='utf-8')
        ):
            instance = self.CLS(
                recipe=Recipe.objects.get(pk=row['recipe_id']),
                ingredient=Ingredient.objects.get(pk=row['ingredient_id']),
                amount=row['amount'])
            instance.save()
