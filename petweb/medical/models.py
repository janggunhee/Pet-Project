from django.db import models

from account.models import Pet


# Pet의 의료정보
class PetMedical(models.Model):

    pet_user = models.OneToOneField(
        Pet,
        on_delete=models.CASCADE,
        primary_key=True
    )

# 펫의 신체 정보
class PetSize(models.Model):

    pet_size = models.ForeignKey(PetMedical)

    weight = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    chest = models.IntegerField(null=True, blank=True)
    create_date = models.DateTimeField(
        auto_now_add=True
    )
    def __str__(self):
        return str(self.pet_size)




