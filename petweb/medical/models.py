from django.db import models

from account.models import Pet


# Pet의 의료정보
class PetMedical(models.Model):

    pet_user = models.OneToOneField(
        Pet,
        on_delete=models.CASCADE,
        primary_key=True
    )

    create_date = models.DateTimeField(
        auto_now_add=True, blank=True
    )

# 펫의 신체 정보
class PetSize(models.Model):

    pet_size = models.ForeignKey(
        PetMedical
    )
    # 펫의 몸무게
    pet_weight = models.IntegerField(null=True, blank=True)
    # 펫의 몸길이
    pet_height = models.IntegerField(null=True, blank=True)
    # 펫의 가슴둘레
    pet_chest = models.IntegerField(null=True, blank=True)
    # 펫의 목둘레
    pet_neck = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.pet_size)



# 팻의 예방접종 정보

class PetVaccine(models.Model):

    # 백신 종류
    CHOICE_VACCINE = (
        ('')
    )
    pass
