from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


__all__ = (
    'PetSpecies',
    'PetBreeds',
    'Pet',
)


class PetSpecies(models.Model):
    # 강아지, 고양이 품종을 고른다 (다른 동물 추가 가능)
    CHOICE_TYPE = (
        ('dog', '강아지'),
        ('cat', '고양이'),
    )
    # choice 옵션으로 pet_type 선택
    pet_type = models.CharField(max_length=20, choices=CHOICE_TYPE)

    # 매직 메소드: 품종이 출력되는 방식
    def __str__(self):
        return self.get_pet_type_display()


class PetBreeds(models.Model):
    species = models.ForeignKey(
        PetSpecies
    )
    breeds_name = models.CharField(max_length=50)

    def __str__(self):
        return self.breeds_name


class CommonInfo(models.Model):
    # 개별 pet에 대한 필드가 담긴 추상 클래스
    species = models.ForeignKey(
        PetSpecies,
        default=True
    )
    # 동물의 품종
    breeds = models.ForeignKey(
        PetBreeds,
        default=True
    )
    # 동물 이름
    name = models.CharField(max_length=100)
    # 생년월일
    birth_date = models.DateField()
    # 성별
    CHOICE_GENDER = (
        ('male', '수컷'),
        ('female', '암컷')
    )
    gender = models.CharField(max_length=10, choices=CHOICE_GENDER)
    # 동물등록번호
    identified_number = models.CharField(max_length=20, blank=True)
    # 중성화 여부
    is_neutering = models.BooleanField()
    # 개체별 색상
    CHOICE_COLOR = (
        ('black', '검정색'),
        ('white', '하얀색'),
        ('brown', '갈색'),
        ('gold', '황금색'),
    )
    body_color = models.CharField(max_length=10, choices=CHOICE_COLOR)

    class Meta:
        abstract = True


class Pet(CommonInfo):
    # 주인
    owner = models.ForeignKey(User, default=True)

    def __str__(self):
        return self.name




