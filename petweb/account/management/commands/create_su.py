from django.conf import settings
from django.contrib.auth import get_user_model

from django.core.management import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(email=settings.SUPERUSER_EMAIL).exists():
            super_user = User.objects.create_superuser(
                email=settings.SUPERUSER_EMAIL,
                password=settings.SUPERUSER_PASSWORD,
                nickname='husky',
            )
            print(f'create superuser : {super_user.email}')
        else:
            print('superuser is already exist.')
