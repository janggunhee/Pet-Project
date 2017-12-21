from datetime import timedelta

from django.db import models

from account.models import Pet, PetSpecies

__all__ = (
    'PetMedical',
    'BodySize',
    'Operation',
    'Vaccine',
    'Inoculation',
)


# 펫의 의료정보 모델
class PetMedical(models.Model):
    # account.model_pet의 Pet 모델에서 상속
    pet = models.OneToOneField(
        Pet,
        related_name='pet_set',
        on_delete=models.CASCADE,
        primary_key=True,
    )

    USERNAME_FIELD = 'pet'

    def __str__(self):
        return self.pet.name


# 동물의 신체 정보 모델
class BodySize(models.Model):
    # 동물의 신체 사이즈 (몸무게, 몸길이, 가슴둘레, 목둘레)
    medical = models.ForeignKey(
        PetMedical,
        related_name='pet_size_set',
        on_delete=models.CASCADE,
    )
    # 목표 체중
    goal_weight = models.FloatField(
        null=True, blank=True,
    )

    # 동물의 몸무게
    current_weight = models.FloatField(
        null=True, blank=True
    )
    # 동물의 가슴둘레
    chest = models.PositiveSmallIntegerField(
        null=True, blank=True
    )
    # 동물의 목둘레
    neck = models.PositiveSmallIntegerField(
        null=True, blank=True
    )
    # 동물의 사이즈 생성일
    created_date = models.DateField(
        auto_now_add=True,
    )

    USERNAME_FIELD = 'medical'

    def __str__(self):
        return self.medical.pet.name


# 이미지 업로드 시 폴더 경로 구성 함수
# 참고 (장고 공식 문서):
# https://docs.djangoproject.com/en/1.11/ref/models/fields/#django.db.models.FileField.upload_to
def user_directory_path(instance, filename):
    return f'operation/pet_{instance.medical.pet.id}/{filename}'


# 동물의 수술 정보 모델
class Operation(models.Model):
    medical = models.ForeignKey(
        PetMedical,
        related_name='operation_set',
        on_delete=models.CASCADE,
    )
    # 수술 상태 사진
    image = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
    )
    # 수술 날짜
    date = models.DateField(
        blank=True,
        null=True,
    )
    # 수술 명
    description = models.CharField(
        max_length=70,
    )
    # 수술 내용
    comment = models.TextField(
        max_length=500,
        blank=True,
    )

    USERNAME_FIELD = 'description'

    def __str__(self):
        return f'{self.medical.pet.name}: {self.description}'


# 예방접종 기본 정보 모델
class Vaccine(models.Model):
    # 동물 종류 (dog/cat)
    species = models.ForeignKey(
        PetSpecies,
        related_name='species_set',
        on_delete=models.CASCADE,
    )
    # 의학 정보와 many-to-many relationship
    inoculations = models.ManyToManyField(
        PetMedical,
        # intermediate model 위치
        through='Inoculation',
    )
    # 백신 이름
    name = models.CharField(
        max_length=20,
    )
    # 백신 접종 회차
    turn = models.PositiveSmallIntegerField(
        default=1,
    )
    # 백신 접종 주기
    period = models.DurationField(
        default=timedelta(weeks=4),
    )

    USERNAME_FIELD = 'name'

    def __str__(self):
        return f'{self.species.pet_type}: {self.name}'


# 펫의 예방접종 정보 모델
class Inoculation(models.Model):
    # 어떤 동물의 의학 정보인가
    medical = models.ForeignKey(
        PetMedical,
        on_delete=models.CASCADE,
        related_name='inoculation_set',
    )
    # 어떤 백신을 맞았는가
    vaccine = models.ForeignKey(
        Vaccine,
        related_name='vaccine_set',
        on_delete=models.CASCADE,
    )
    # 백신 접종 횟수
    num_of_times = models.PositiveSmallIntegerField(
        default=1,
    )
    # 백신 맞은 날짜
    inoculated_date = models.DateTimeField(
        blank=True,
        null=True,
    )
    # 백신 맞은 병원
    hospital = models.CharField(
        max_length=100,
        blank=True,
    )
    # 알람 체크 여부
    is_alarm = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'vaccine'

    def __str__(self):
        return f'{self.medical.pet.name}: {self.vaccine.name}'
