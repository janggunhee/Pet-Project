from django.db import models

from account.models import Pet, PetSpecies

__all__ = (
    'PetMedical',
    'PetSize',
    'PetVaccine',
    'VaccineInfo',
    'PetOperation',
)


# 펫의 의료정보 모델
class PetMedical(models.Model):
    # account.model_pet의 Pet 모델에서 상속
    pet = models.OneToOneField(
        Pet,
        related_name='medical',
        on_delete=models.CASCADE,
        primary_key=True,
    )


# 동물의 신체 정보 모델
class PetSize(models.Model):
    # 동물의 신체 사이즈 (몸무게, 몸길이, 가슴둘레, 목둘레)
    size = models.ForeignKey(
        PetMedical,
        related_name='size',
        on_delete=models.CASCADE,
    )

    # 동물의 몸무게
    weight = models.IntegerField(
        null=True, blank=True
    )
    # 동물의 몸길이
    height = models.IntegerField(
        null=True, blank=True
    )
    # 동물의 가슴둘레
    chest = models.IntegerField(
        null=True, blank=True
    )
    # 동물의 목둘레
    neck = models.IntegerField(
        null=True, blank=True
    )
    # 동물의 사이즈 생성일
    create_date = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return str(self.size)


# 동물의 수술 정보 모델
class PetOperation(models.Model):
    pet_operation = models.ForeignKey(
        PetMedical,
        on_delete=models.CASCADE,
        related_name='pet_operations',
    )
    # 수술 상태 사진
    image = models.ImageField(
        upload_to=None,
        max_length=100,
        blank=True,
    )
    # 수술 날짜
    date = models.DateField(
        auto_now=False,
    )
    # 수술 명
    description = models.CharField(max_length=50, )
    # 수술 내용
    comment = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return str(self.description)


# 예방접종 정보 모델
class VaccineInfo(models.Model):
    vaccine_info = models.ForeignKey(
        PetSpecies,
        on_delete=models.CASCADE,
    )
    # 예방 접종 이름
    vaccine_name = models.CharField(
        max_length=20,
        blank=True,
    )
    # 예방 접종의 회차
    vaccine_turn = models.PositiveIntegerField(
        default=0,
    )

    # # 예방 접종 주기
    # vaccine_cycle = models.PositiveIntegerField()

    def __str__(self):
        return self.vaccine_info.pet_type + ': ' + self.vaccine_name


# 동물의 예방접종 모델
class PetVaccine(models.Model):
    vaccine = models.ForeignKey(
        PetMedical,
        related_name='vaccines'
    )
    # 백신 종류
    vaccine_type = models.ForeignKey(VaccineInfo)
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
        max_length=30,
        null=True,
        blank=True,
    )
    # 백신 예정일
    due_date = models.DateField(
        auto_now=False,
    )
    # 병원 이름
    hospital = models.CharField(
        max_length=30,
        blank=True,
    )

    def __str__(self):
        return str(self.vaccine)
