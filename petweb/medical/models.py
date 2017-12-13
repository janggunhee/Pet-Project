from django.db import models

from account.models import Pet


# Pet의 의료정보
class PetMedical(models.Model):

    pet = models.OneToOneField(
        Pet,
        related_name='medical',
        on_delete=models.CASCADE,
        primary_key=True
    )


# 펫의 신체 정보
class PetSize(models.Model):

    pet_size = models.ForeignKey(
        PetMedical,
        related_name='sizes',
        on_delete=models.CASCADE,
    )

    # 펫의 몸무게
    pet_weight = models.IntegerField(
        null=True, blank=True
    )
    # 펫의 몸길이
    pet_height = models.IntegerField(
        null=True, blank=True
    )
    # 펫의 가슴둘레
    pet_chest = models.IntegerField(
        null=True, blank=True
    )
    # 펫의 목둘레
    pet_neck = models.IntegerField(
        null=True, blank=True
    )

    create_date = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return str(self.pet_size)



class OperationInfo(models.Model):

    operations = models.ForeignKey(
        PetMedical,
        related_name='operations',
    )

    chart = models.ImageField(

    )
    date = models.DateField(

    )
    description = models.CharField()

    comment = models.TextField()


# 팻의 예방접종 정보

class PetVaccine(models.Model):

    pet_vaccine = models.ForeignKey(
        PetMedical,
        related_name='vaccines'
    )
    # 백신 이름
    name = models.CharField(
        null=True,
        blank=True,
    )
    # 백신 회차
    turn = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    # 백신 접종일
    date = models.DateField(
        auto_now=False,
    )
    # 백신 기간
    period = models.CharField(
        null=True,
        blank=True,
    )
    due_date = models.DateField(
        auto_now=False,
    )
    hospital = models.CharField(
        null=True,
        blank=True,
    )

