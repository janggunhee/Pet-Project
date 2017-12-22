from datetime import datetime

from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from rest_framework.test import APILiveServerTestCase

from ..models import PetSpecies, PetBreed, Pet
from ..tests import DummyUser
from ..apis import PetListCreate

User = get_user_model()

__all__ = (
    'PetCreateListTest',
    'PetProfileTest',
)


# 자주 쓰는 메소드를 클래스로 정의
class DummyPet:
    @staticmethod
    def create_dummy_dog_species():
        return PetSpecies.objects.create(
            pet_type='dog',
        )

    @staticmethod
    def create_dummy_cat_species():
        return PetSpecies.objects.create(
            pet_type='cat',
        )

    @staticmethod
    def create_dummy_dog_breeds():
        return PetBreed.objects.create(
            species=DummyPet.create_dummy_dog_species(),
            breeds_name='시츄',
        )

    @staticmethod
    def create_dummy_cat_breeds():
        return PetBreed.objects.create(
            species=DummyPet.create_dummy_cat_species(),
            breeds_name='페르시안',
        )


# 펫 생성 / 리스트 보기 테스트
class PetCreateListTest(APILiveServerTestCase):
    def setUp(self):
        self.dummy_user_pk = '1'
        self.URL_API_PET_LIST_CREATE_NAME = 'profile:pets'
        self.URL_API_PET_LIST_CREATE = '/profile/{pk}/pets/'
        self.PET_LIST_CREATE_VIEW_CLASS = PetListCreate

    # 테스트 17. PetListCreate url이 reverse name과 매치되는가
    def test_signup_url_name_reverse(self):
        url = reverse(self.URL_API_PET_LIST_CREATE_NAME, args=self.dummy_user_pk)
        self.assertEqual(url, self.URL_API_PET_LIST_CREATE.format(pk=self.dummy_user_pk))

    # 테스트 18. account.apis. PetListCreateview에 대해
    # URL, reverse, resolve, view 함수가 같은지 확인
    def test_signup_url_resolve_view_class(self):
        resolver_match = resolve(self.URL_API_PET_LIST_CREATE.format(pk=self.dummy_user_pk))
        self.assertEqual(resolver_match.view_name,
                         self.URL_API_PET_LIST_CREATE_NAME)
        self.assertEqual(
            resolver_match.func.view_class,
            self.PET_LIST_CREATE_VIEW_CLASS
        )

    # 테스트 19. pet이 생성되는가
    def test_pet_create(self):
        # 더미 펫 품종 생성
        dummy_dog_breed = DummyPet.create_dummy_dog_breeds()
        # 더미 유저 생성
        dummy_user = DummyUser.create_user()
        # 더미 유저 인증
        token = dummy_user.token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # 입력할 펫의 정보
        input_data = {
            'name': 'dummy_pet',
            'birth_date': '2014-04-15',
            'gender': 'male',
            'body_color': 'gold',
            'species': 'dog',
            'breeds': '시츄',
            'identified_number': '1234',
            'is_neutering': 'true',
        }

        # URL로 create 요청
        response = self.client.post(self.URL_API_PET_LIST_CREATE.format(pk=dummy_user.pk), data=input_data)
        # 응답 코드 확인
        self.assertEqual(response.status_code, 201)
        # 생성된 더미 펫 인스턴스 호출
        dummy_dog = Pet.objects.get(owner_id=dummy_user.pk)

        # 더미 펫의 정보와 입력된 펫의 정보 비교
        self.assertEqual(dummy_dog.name, input_data['name'])  # 이름
        # 생년월일
        self.assertEqual(dummy_dog.birth_date, datetime.strptime(input_data['birth_date'], '%Y-%m-%d').date())
        self.assertEqual(dummy_dog.gender, input_data['gender'])  # 성별
        self.assertEqual(dummy_dog.body_color, input_data['body_color'])  # 색상
        self.assertEqual(dummy_dog.species.pet_type, 'dog')  # 종류
        self.assertEqual(dummy_dog.breeds.breeds_name, '시츄')  # 품종
        self.assertEqual(dummy_dog.identified_number, input_data['identified_number'])  # 동물등록번호
        self.assertTrue(dummy_dog.is_neutering)  # 중성화
        self.assertTrue(dummy_dog.is_active)  # 활성화

    # 테스트 20. pet list가 호출되는가
    def test_pet_list(self):
        # 더미 유저 생성
        dummy_user = DummyUser.create_user()
        # 더미 고양이 종류 생성
        dummy_cat_species = DummyPet.create_dummy_cat_species()
        # 더미 고양이 품종 생성
        dummy_cat_breed = DummyPet.create_dummy_cat_breeds()
        # 더미 고양이 인스턴스 생성
        dummy_cat = Pet.objects.create(
            owner=dummy_user,
            name='cat_1',
            birth_date=datetime.strptime('2017-01-01', '%Y-%m-%d').date(),
            gender='male',
            body_color='brown',
            species=dummy_cat_species,
            breeds=dummy_cat_breed,
            identified_number='4321',
            is_neutering=True,
        )

        # 더미 강아지 종류 생성
        dummy_dog_species = DummyPet.create_dummy_dog_species()
        # 더미 강아지 품종 생성
        dummy_dog_breed = DummyPet.create_dummy_dog_breeds()
        # 더미 강아지 인스턴스 생성
        dummy_dog = Pet.objects.create(
            owner=dummy_user,
            name='dog_1',
            birth_date=datetime.strptime('2017-05-01', '%Y-%m-%d').date(),
            gender='female',
            body_color='gold',
            species=dummy_dog_species,
            breeds=dummy_dog_breed,
            identified_number='2468',
            is_neutering=False,
        )

        # PetList 요청
        response = self.client.get(self.URL_API_PET_LIST_CREATE.format(pk=dummy_user.pk))
        # 응답 코드 확인
        self.assertEqual(response.status_code, 200)
        # 응답 데이터의 유저가 더미 유저와 같은가
        self.assertEqual(response.data['results'][0]['owner']['pk'], dummy_user.pk)
        # 응답 데이터의 0번째 펫이 'dog_1'인가
        # (ordering을 '-pk'로 해서 최근에 생성된 펫이 가장 앞 순서 인덱스를 갖는다)
        self.assertEqual(response.data['results'][0]['pet']['name'], 'dog_1')
        # 응답 데이터의 1번째 펫이 'cat_1'인가
        self.assertEqual(response.data['results'][1]['pet']['name'], 'cat_1')


# 펫 프로필 테스트 (디테일/정보 수정/삭제)
class PetProfileTest(APILiveServerTestCase):
    pass
