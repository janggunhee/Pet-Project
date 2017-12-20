from django.core.management import BaseCommand

from ...models import PetBreed, PetSpecies
from utils.functions import pet_age


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not PetBreed.objects.all():
            for breed in pet_age.Large_dog:
                PetBreed.objects.create(
                    species=PetSpecies.objects.get(pet_type='dog'),
                    breeds_name=breed
                )
            for breed in pet_age.Middle_dog:
                PetBreed.objects.create(
                    species=PetSpecies.objects.get(pet_type='dog'),
                    breeds_name=breed
                )
            for breed in pet_age.Small_dog:
                PetBreed.objects.create(
                    species=PetSpecies.objects.get(pet_type='dog'),
                    breeds_name=breed
                )
            total_dog_length = len(PetBreed.objects.filter(species__pet_type='dog'))

            for breed in pet_age.Large_cat:
                PetBreed.objects.create(
                    species=PetSpecies.objects.get(pet_type='cat'),
                    breeds_name=breed
                )
            for breed in pet_age.Middle_cat:
                PetBreed.objects.create(
                    species=PetSpecies.objects.get(pet_type='cat'),
                    breeds_name=breed
                )
            for breed in pet_age.Small_cat:
                PetBreed.objects.create(
                    species=PetSpecies.objects.get(pet_type='cat'),
                    breeds_name=breed
                )
            total_cat_length = len(PetBreed.objects.filter(species__pet_type='cat'))

            print(f'total created dogs : {total_dog_length}')
            print(f'total created cats : {total_cat_length}')

        else:
            print('pet breeds are already exists.')
