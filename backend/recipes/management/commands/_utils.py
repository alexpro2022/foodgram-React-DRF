import os
from csv import DictReader

from users.models import User

DATA_PATH = 'data/'


def info(func):
    def wrapper(self, *args, **options):
        if self.CLS.objects.exists():
            self.stdout.write(
                f'{self.FILE_NAME} data already loaded...exiting.')
            return
        self.stdout.write(f'=Loading {self.FILE_NAME} data')
        func(self, *args, **options)
        self.stdout.write(self.style.SUCCESS(
            f'===Successfully loaded: {self.CLS.objects.all()}'))
    return wrapper


def load(klass, file_name):
    fields = klass._meta.get_fields(include_parents=False)
    for row in DictReader(
        open(f'{DATA_PATH}{file_name}', encoding='utf-8')
    ):
        d = {}
        for field in fields:
            if field.name in row.keys():
                d[field.name] = row[field.name]
        if klass is User:
            d['password'] = os.getenv('TEST_USERS_PASSWORD')
            User.objects.create_user(**d)
        else:
            klass.objects.create(**d)
