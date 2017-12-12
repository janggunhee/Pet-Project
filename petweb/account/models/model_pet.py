from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from versatileimagefield.fields import VersatileImageField

from account.models.thumbnail_base import ThumbnailBaseModel

User = get_user_model()


__all__ = (
    'PetSpecies',
    'PetBreed',
    'Pet',
)


# 펫 종류 (고양이/강아지) 모델
class PetSpecies(models.Model):
    # 강아지, 고양이 품종을 고른다 (다른 동물 추가 가능)
    CHOICE_TYPE = (
        ('dog', '강아지'),
        ('cat', '고양이'),
    )
    # choice 옵션으로 pet_type 선택
    pet_type = models.CharField(max_length=20, choices=CHOICE_TYPE)

    USERNAME_FIELD = 'pet_type'

    # 매직 메소드: 품종이 출력되는 방식
    def __str__(self):
        return self.get_pet_type_display()

    class Meta:
        verbose_name_plural = "Pet species"


# 펫 품종 중 강아지 쿼리셋 매니저
# https://docs.djangoproject.com/en/1.11/topics/db/managers/#modifying-a-manager-s-initial-queryset
class DogManager(models.Manager):
    # 쿼리셋 호출 함수
    def get_queryset(self):
        # 펫 품종 모델의 쿼리셋에서 pet_type이 'dog'인 객체들만 리턴
        return super(DogManager, self).get_queryset().filter(
            species=PetSpecies.objects.get(pet_type='dog')
        )


# 펫 품종 중 고양이 쿼리셋 매니저
class CatManager(models.Manager):
    # 쿼리셋 호출 함수
    def get_queryset(self):
        # 펫 품종 모델의 쿼리셋에서 pet_type이 'cat'인 객체들만 리턴
        return super(CatManager, self).get_queryset().filter(
            species=PetSpecies.objects.get(pet_type='cat')
        )


# 펫 품종 모델
class PetBreed(models.Model):
    # 펫 종류
    species = models.ForeignKey(
        PetSpecies
    )
    # 품종 이름
    breeds_name = models.CharField(max_length=50)

    # 커스텀 매니저가 생겼기 때문에 원래 모델 매니저가 상속됨을 명시해 준다
    objects = models.Manager()
    # DogManager는 'dogs' attribute로 정의
    dogs = DogManager()
    # CatManager는 'cats' attribute로 정의
    cats = CatManager()

    USERNAME_FIELD = 'breeds_name'

    def __str__(self):
        return self.breeds_name


class Pet(ThumbnailBaseModel, models.Model):
    # 썸네일 저장 위치를 User/Pet으로 나눔
    image = VersatileImageField(
        upload_to='Pets',
        width_field='width',
        height_field='height',
    )

    # 동물의 주인
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='pets',
        on_delete=models.CASCADE)

    # 동물의 종류
    # 예: 강아지, 고양이
    species = models.ForeignKey(
        PetSpecies,
    )
    # 동물의 품종
    # 에: 시츄, 코리안 숏헤어 등등
    breeds = models.ForeignKey(
        PetBreed,
    )
    # 동물 이름
    name = models.CharField(max_length=100)
    # 생년월일
    birth_date = models.DateField()
    # 성별
    CHOICE_GENDER = (
        ('male', '수컷'),
        ('female', '암컷'),
    )
    gender = models.CharField(max_length=10, choices=CHOICE_GENDER)
    # 동물등록번호
    identified_number = models.CharField(max_length=20, blank=True)
    # 중성화 여부
    is_neutering = models.BooleanField(
        default=False
    )
    # 개체별 색상
    CHOICE_COLOR = (
        ('black', '검정색'),
        ('white', '하얀색'),
        ('brown', '갈색'),
        ('gold', '황금색'),
    )
    body_color = models.CharField(max_length=10, choices=CHOICE_COLOR)

    # 동물 비활성화 여부
    is_active = models.BooleanField(
        default=True
    )

    USERNAME_FIELD = 'name'

    class Meta:
        ordering = ('-pk', )

    def __str__(self):
        return self.name
