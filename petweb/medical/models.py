from django.db import models

from account.models import Pet



class PetMedical(models.Model):
    # Petuser의 의료정보 (키 체중 질병)
    pet_user = models.OneToOneField(
        Pet,
        on_delete=models.CASCADE,
        primary_key=True
    )
    pet_profile = models.ImageField(upload_to='user', blank=True)
    pet_age = models.CharField()


class PetDisease(models.Model):
    # 동물의 질병
    pet_disease = models.CharField(max_length=100)
    pass

class PetHeight(models.Model):
    # 동물의 키
    pet_height = models.CharField(max_length=100)
    pass

class PetWeight(models.Model):
    # 동물의 체중
    pet_weight = models.CharField(max_length=100)
    pass

