from django.db import models

from account.models import Pet, PetSpecies


# Pet의 의료정보 모델
class PetMedical(models.Model):

    pet = models.OneToOneField(
        Pet,
        related_name='medical',
        on_delete=models.CASCADE,
        primary_key=True
    )


# 펫의 신체 정보 모델
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
    # 펫 사이즈 생성일 기록
    create_date = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return str(self.pet_size)


# 펫의 수술 정보 모델
class Operation(models.Model):

    operations = models.ForeignKey(
        PetMedical,
        related_name='operations',
    )
    # 수술 사진
    image = models.ImageField(
        upload_to=None,
        max_length=100,
    )
    # 수술 날짜
    date = models.DateField()
    # 수술명
    description = models.CharField(max_length=50)
    # 수술 내용
    comment = models.TextField(max_length=500, blank=True)



# 팻의 예방접종 모델
class PetVaccine(models.Model):

    pet_vaccine = models.ForeignKey(
        PetMedical,
        related_name='vaccines'
    )
    # 백신 종류
    vaccine_ = models.ForeignKey(
        VaccineInfo
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
    # 백신 예정일
    due_date = models.DateField()
    # 병원 이름
    hospital = models.CharField(
        null=True,
        blank=True,
    )


# 펫의 예방접종 정보 모델
class VaccineInfo(models.Model):
    vaccine_info = models.ForeignKey(
        PetSpecies,
    )
    # 예방 접종 이름
    vaccine_name = models.CharField(max_length=20)
    # 예방 접종의 회차
    vaccine_turn = models.PositiveIntegerField(max_length=10)
