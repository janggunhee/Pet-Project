from datetime import date
from typing import NamedTuple

__all__ = (
    'Age',
    'age_conversion',
    'breed_classification',
    'calculate_age',
    'dog_life_type',
)

# dog_breed_type
Large_dog = ['German Shepherd', 'Golden Retriever', 'Rottweiler', 'German Shorthaired Pointer', 'Doberman Pinscher',
             'Bernese Mountain Dog', 'Collie', 'Cane Corso', 'Rhodesian Ridgeback', 'Chesapeake Bay Retriever', 'Akita',
             'Bullmastiff', 'Bloodhound', 'Alaskan Malamute', 'Dogue de Bordeaux', 'Dalmatian', 'Old English Sheepdog',
             'Irish Setter', 'Greater Swiss Mountain Dog', 'Bouvier des Flandres']
Middle_dog = ['Labrador Retriever', 'Bulldog', 'Poodle', 'Boxer', 'Siberian Husky', 'Australian Shepherd', 'Brittany',
              'English Springer Spaniel', 'American Cocker Spaniel', 'Vizsla', 'Weimaraner',
              'Miniature American Shepherd', 'Border Collie', 'Basset Hound', 'Shiba Inu', 'Belgian Malinois',
              'Soft Coated Wheaten Terrier', 'Portuguese Water Dog', 'Australian Cattle Dog', 'Airedale Terrier']
Small_dog = ['Beagle', 'French Bulldog', 'Yorkshire Terrier', 'Dachshund', 'Miniature Schnauzer',
             'Pembroke Welsh Corgi', 'Cavalier King Charles Spaniel', 'Shih Tzu', 'Boston Terrier', 'Pomeranian',
             'Havanese', 'Shetland Sheepdog', 'Chihuahua', 'Pug', 'Maltese', 'West Highland White Terrier',
             'Bichon Frise', 'Papillon', 'Scottish Terrier', 'Miniature Pinscher']

# Cat_breed_type
Small_cat = ['Oriental', 'LaPerm', 'Munchkin', 'Bambino']
Middle_cat = ['Exotic Shorthair', 'Persian', 'Abyssinian', 'Sphynx', 'Siamese', 'Scottish Fold', 'Cornish Rex',
              'Devon Rex', 'Birman', 'Burmese', 'Tonkinese', 'Russian Blue', 'Egyptian Mau', 'Manx', 'Japanese Bobtail',
              'Selkirk Rex', 'American Curl', 'Somali', 'Turkish Angora', 'Colorpoint Shorthair']
Large_cat = ['British Shorthair', 'American Shorthair', 'Norwegian Forest Cat', 'Ocicat', 'Selkirk Rex', 'Chartreux',
             'Ragamuffin', 'American Bobtail', 'Turkish Van', 'American Wirehair', 'Himalayan', 'Pixie-bob', 'Savannah',
             'York Chocolate', 'British Semi-longhair', 'Cheetoh', 'Cyprus']

num_dog = len(Small_dog) + len(Middle_dog) + len(Large_dog)
num_cat = len(Small_cat) + len(Middle_cat) + len(Large_cat)


# pet = Pet.objects.get(pk=pk)   ### import not yet
# birth_date = pet.birth_date   ## models.Model.DateField << datetime.date
# pet_type = Pet class 이름


class Age(NamedTuple):
    years: int
    months: int


def calculate_age(birth_date):
    # 리턴 값은  oo년 00개월을 tuple형식으로 표현 (years, months)
    # 12개월이 넘으면 1년 00개월로 표현
    days = (date.today() - birth_date).days
    years = days // 365
    months = (days % 365) // 30
    Age.years = years
    Age.months = months
    ret = {
        'years': years,
        'months': months,
    }
    return Age(**ret)


def breed_classification(breed):
    # 품종을 대/중/소로 나누기
    if breed in Large_dog or breed in Large_cat:
        breed_type = "L"
    elif breed in Middle_dog or breed in Middle_cat:
        breed_type = "M"
        # Small_dog에 속하거나  품종을 모를 때
    else:
        breed_type = "S"
    return breed_type


def dog_life_type(breed, birth_date):
    age = calculate_age(birth_date)
    if breed_classification(breed) == "L":
        if age.years >= 5:
            life_type = 'senior'  # 고령
        elif age.years >= 10:
            life_type = 'aged'  # 노인
        else:
            life_type = 'young'  # 젊음

    elif breed_classification(breed) == 'M':
        if age.years >= 7:
            life_type = 'senior'  # 고령
        elif age.years >= 12:
            life_type = 'aged'  # 노인
        else:
            life_type = 'young'  # 젊음

    elif breed_classification(breed) == "S":
        if age.years >= 7:
            life_type = 'senior'  # 고령
        elif age.years >= 14:
            life_type = 'aged'  # 노인
        else:
            life_type = 'young'  # 젊음
    return life_type


def age_conversion(pet_type, breed, birth_date):
    """
    개의 경우, 
    네이버 블로그 <개 나이 계산법, 사람 나이로 환산하기> 참조
    https://m.blog.naver.com/PostView.nhn?blogId=happycare719&logNo=30145816887&proxyReferer=https%3A%2F%2Fwww.google.co.kr%2F
    10kg 이하의 소형견은 1년령이 15살, 2년령이 24살이구요, 그 후 부터는 1년을 4살로 계산하면 됩니다.  ﻿
     * 예를 들어 10살 소형견은 (10년령-2살)*4살 + 24살 = 56세
    25kg 전후의 중형견은 (진도개 크키) 1년령이 15살, 2년령이 24살이구요
     그 후 부터는 1년을 5살로 계산하면 됩니다.
     * 예를 들어 10살 중대형견은 (10년령-2살)*5살 + 24살 = 64세
    40kg 이상의 대형견은 (세인트버나드 등)  1년령이 10살, 2년령이 22살이구요
     그 후 부터는 1년을 7살로 계산하면 됩니다.
     * 예를 들어 10살 대형견은 (10년령-2살)*7살 + 22살 = 78세

     고양이의 경우
     네이버 블로그: 고양이 나이 계산법 (사람 나이로 환산하기)
     https://m.blog.naver.com/happycare719/30145835952
     1년령 = 15세, 2년령 = 24세, 2년령 이상 부터는 1년마다 4살씩 추가~!!
       예를 들어서 9년령 고양이는 (9살-2년)* 4세 + 24세 = 사람 나이 52세 입니다.
    """
    age = calculate_age(birth_date)
    if pet_type == "dog":
        # 대형견
        if breed_classification(breed) == 'L':
            if age.years == 0:
                conversion_human_age = (age.months * 10) // 12
            elif age.years == 1:
                conversion_human_age = 10 + age.months
            else:
                conversion_human_age = 7 * (age.years - 2) + 22 \
                                       + (age.months * 4) // 12
        # 중형견
        elif breed_classification(breed) == 'M':
            if age.years == 0:
                conversion_human_age = (age.months * 15) // 12
            elif age.years == 1:
                conversion_human_age = age.years * 15 \
                                       + (age.months * 9) // 12
            else:
                conversion_human_age = 5 * (age.years - 2) + 24 \
                                       + (age.months * 4) // 12
        # 소형견 또는 모르는 품종
        else:
            if age.years == 0:
                conversion_human_age = (age.months * 15) // 12
            elif age.years == 1:
                conversion_human_age = age.years * 15 \
                                       + (age.months * 9) // 12
            else:
                conversion_human_age = 4 * (age.years - 2) + 24 \
                                       + (age.months * 4) // 12
    elif pet_type == "cat":
        if age.years == 0:
            conversion_human_age = (age.months * 15) // 12
        elif age.years == 1:
            conversion_human_age = age.months * 10 // 12 + 15
        else:
            conversion_human_age = (25 + (age.years - 2) * 4) \
                                   + (age.months * 4) // 12
    # 모르는 동물이 입력되면 None
    else:
        conversion_human_age = None
    return conversion_human_age
