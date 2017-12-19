from django.core.management import BaseCommand

from ...models import Vaccine


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not Vaccine.objects.all():
            pass
