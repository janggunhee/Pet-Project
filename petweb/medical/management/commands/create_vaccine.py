from datetime import timedelta

from django.core.management import BaseCommand

from account.models import PetSpecies
from utils.functions.vaccine_info import get_dog_vaccine_info, get_cat_vaccine_info
from ...models import Vaccine


class Command(BaseCommand):
    def handle(self, *args, **options):
        dog = get_dog_vaccine_info()
        cat = get_cat_vaccine_info()
        if not Vaccine.objects.all():
            for d in dog:
                Vaccine.objects.create(
                    species=PetSpecies.objects.get(pet_type=d.species),
                    name=d.name,
                    turn=d.turn,
                    period=timedelta(weeks=d.period),
                )
            total_dog_vaccine = len(Vaccine.objects.filter(species__pet_type='dog'))

            for c in cat:
                Vaccine.objects.create(
                    species=PetSpecies.objects.get(pet_type=c.species),
                    name=c.name,
                    turn=c.turn,
                    period=timedelta(weeks=c.period),
                )
            total_cat_vaccine = len(Vaccine.objects.filter(species__pet_type='cat'))

            print(f'create dog vaccine info : {total_dog_vaccine}')
            print(f'create cat vaccine info : {total_cat_vaccine}')

        else:
            print('vaccine info already exists.')
