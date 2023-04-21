import os

from django.core.management import BaseCommand

from users.models import User

from ._utils import info, load


class Command(BaseCommand):
    CLS = User
    FILE_NAME = f'{CLS.__name__.lower()}s.csv'
    help = f'Loads data from {FILE_NAME}'

    @info
    def handle(self, *args, **options):
        load(self.CLS, self.FILE_NAME)
        admin_password = os.getenv('ADMIN_PASSWORD', 'a')
        if admin_password is not None:
            User.objects.create_superuser(
                os.getenv('ADMIN_USERNAME', 'a'),
                os.getenv('ADMIN_EMAIL', 'a@a.a'),
                admin_password,
            )
