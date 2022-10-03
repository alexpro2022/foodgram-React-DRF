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
        for user in self.CLS.objects.all():
            user.set_password('111')
            user.save()
