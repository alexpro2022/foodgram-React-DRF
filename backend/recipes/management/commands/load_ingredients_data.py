from django.core.management import BaseCommand

from recipes.models import Ingredient
from ._utils import info, load


class Command(BaseCommand):
    CLS = Ingredient
    FILE_NAME = f'{CLS.__name__.lower()}s.csv'
    help = f'Loads data from {FILE_NAME}'

    @info
    def handle(self, *args, **options):
        load(self.CLS, self.FILE_NAME)
