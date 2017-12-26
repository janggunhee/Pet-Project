from typing import NamedTuple


# ---------- 변수 선언 ---------- #

# 네임드 튜플
class VaccineInfo(NamedTuple):
    species: str
    name: str
    turn: int
    period: int


# ----- 강아지 변수 ----- #

# 강아지 종류 제너레이터 컴프리헨션
dog_species = ('dog' for d in range(1, 9))

# 강아지 백신 이름 튜플
dog_vaccine_name = (
    "종합백신(DHPPL)",
    "코로나(Corona)",
    "기관지염(Kennel Cough)",
    "광견병(Rabis)",
    "심장사상충(Herat worm)",
    "인플루엔자(Influenza)",
    "내부구충",
    "외부구충",
)

# 강아지 백신 접종 회차 튜플
dog_vaccine_turn = (5, 2, 3, 2, 1, 1, 3, 1,)

# 강아지 백신 접종 주기 튜플
dog_vaccine_period = (14, 14, 14, 168, 28, 0, 14, 28,)

# 네 가지 튜플을 모두 묶은 튜플
dog_tuple = tuple(zip(dog_species,
                      dog_vaccine_name,
                      dog_vaccine_turn,
                      dog_vaccine_period))

# ----- 고양이 변수 ----- #

# 고양이 종류 제너레이터 컴프리헨션
cat_species = ('cat' for c in range(1, 5))

# 고양이 백신 이름 튜플
cat_vaccine_name = (
    "혼합예방주사(CVRP)",
    "백혈병(Feline Leukemia)",
    "전염성 복막염(FIP)",
    "광견병(Rabis)",
)

# 고양이 백신 접종 회차 튜플
cat_vaccine_turn = (3, 2, 2, 1,)

# 고양이 백신 접종 주기 튜플
cat_vaccine_period = (21, 21, 21, 0,)

# 네 가지 튜플을 모두 묶은 튜플
cat_tuple = tuple(zip(cat_species,
                      cat_vaccine_name,
                      cat_vaccine_turn,
                      cat_vaccine_period))


# ---------- 함수 선언 ---------- #

# 강아지 백신 정보를 네임드 튜플로 저장: 리스트 컴프리헨션
def get_dog_vaccine_info():
    return [VaccineInfo(species=i[0],
                        name=i[1],
                        turn=i[2],
                        period=i[3],
                        )
            for i in dog_tuple]


# 고양이 백신 정보를 네임드 튜플로 저장: 리스트 컴프리헨션
def get_cat_vaccine_info():
    return [VaccineInfo(species=i[0],
                        name=i[1],
                        turn=i[2],
                        period=i[3],
                        )
            for i in cat_tuple]
