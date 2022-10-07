from django.core.management import BaseCommand

from .load_favorites_data import Command as load_favorites
from .load_ingredients_data import Command as load_ingredients
from .load_recipe_ingredient_data import Command as load_recipe_ingredient
from .load_recipes_data import Command as load_recipes
from .load_shoppingcarts_data import Command as load_shoppingcards
from .load_subscribe_data import Command as load_subscribes
from .load_tags_data import Command as load_tags
from .load_users_data import Command as load_users


class Command(BaseCommand):
    def handle(self, *args, **options):
        load_users().handle()
        load_subscribes().handle()
        load_tags().handle()
        load_ingredients().handle()
        load_recipes().handle()
        load_recipe_ingredient().handle()
        load_favorites().handle()
        load_shoppingcards().handle()
