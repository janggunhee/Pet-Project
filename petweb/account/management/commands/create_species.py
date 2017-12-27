from django.core.management import BaseCommand

from ...models import PetSpecies


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not PetSpecies.objects.all():
            make_dog = PetSpecies.objects.create(
                pet_type=PetSpecies.CHOICE_TYPE[0][0],
            )
            make_cat = PetSpecies.objects.create(
                pet_type=PetSpecies.CHOICE_TYPE[1][0],
            )
            print(f'create species : {make_dog.pet_type}')
            print(f'create species : {make_cat.pet_type}')
        else:
            print('species are already exists. please check the DB.')
