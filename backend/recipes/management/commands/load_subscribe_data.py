from csv import DictReader

from django.core.management import BaseCommand

from users.models import Subscribe, User

from ._utils import DATA_PATH, info


class Command(BaseCommand):
    CLS = Subscribe
    FILE_NAME = CLS.__name__.lower()
    help = f'Loads data from {FILE_NAME}s.csv'

    @info
    def handle(self, *args, **options):
        for row in DictReader(
            open(f'{DATA_PATH}{self.FILE_NAME}s.csv', encoding='utf-8')
        ):
            instance = self.CLS(
                subscribed_user=User.objects.get(pk=row['follower_id']),
                author_subscription=User.objects.get(pk=row['following_id']))
            instance.save()
