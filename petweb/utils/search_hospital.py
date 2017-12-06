import requests
from config import settings
from typing import NamedTuple
import os
import json

# 실험값 :  모두 string으로 가정하지만  int, float에 대비하여


lat, lng = 37.50146079999999, 127.0532418
lat = str(lat)
lng = str(lng)

# 나중에 .config_secret에 들어갈 내용
google_apis_path = open(os.path.join(settings.ROOT_DIR, '.config_secret',
                    'settings_googlemaps.json')).read()
google_api_keys = json.loads(google_apis_path)

# key_place
key_place = google_api_keys['googlemaps']['places']
# key_distance
key_distance = google_api_keys['googlemaps']['distance']
# key_geocoding
key_geocoding = google_api_keys['googlemaps']['geocoding']

# URL 베이스
URL_base = 'https://maps.googleapis.com/maps/api/'


# 검색 시간 지연으로 검색량 제한 주의 : num_of_searches


class SearchInfo(NamedTuple):
    name: str
    address: str
    h_lat: str
    h_lng: str
    phone: str
    distance: str


def get_hospital_info(place_id):
    url = URL_base + "place/details/json"
    params = {
        'placeid': place_id,
        'key': key_place,
        'language': "ko"
    }
    res = requests.get(url, params)

    place_info = res.json().get('result')
    hospital_info = dict()
    # 주소
    hospital_info.update(address=place_info.get('formatted_address'))
    # 전화 번호
    hospital_info.update(phone=place_info.get('formatted_phone_number'))
    # 웹사이트 주소
    hospital_info.update(website=place_info.get('website'))
    # 페점 여부
    hospital_info.update(closed=place_info.get('permanently_closed'))
    return hospital_info


def get_distance(lat, lng, place_id):
    url = URL_base + 'distancematrix/json'
    params = {
        'key': key_distance,
        'origins': lat + ', ' + lng,
        'destinations': f'place_id:{place_id}',
        'language': 'ko',
        'mode': 'transit',
        'units': 'metric'
    }
    res = requests.get(url, params)
    distance = res.json()['rows'][0]['elements'][0]['distance'].get('value')
    return distance


# 찾으려는 장소
keyword = "24시 동물병원"


def nearbysearch(lat, lng, keyword, num_of_searches=20):
    """
    사용자의 위치에서 가장 가까운 동물병원들을  찾기
    20개 묶음으로 리스트 형성됨 (20개 미만이면 그 숫자)
      client의 POST요청 >> POST.data['lat'],  POST.data['lng']
      params: lat:: POST.data['lat']  사용자 위치 중 위도 string
              lng: POST.data['lng']  사용자 위치 중 경도 string
              num_of_searches  검색시간이 걸리므로 검색량 제한하는 인자
      return list of NamedTuple  [ NamedTuple0, NamedTuple1, ..., ]
   """
    lat = str(lat)
    lng = str(lng)

    url = URL_base + 'place/nearbysearch/json'

    params = {
        'location': lat + ',' + lng,
        'keyword': keyword,
        'rankby': "distance",
        'language': "ko",
        'key': key_place,
    }
    res = requests.get(url, params)

    # 결과:  이름, 위도, 경도, place_id
    result_list = []
    # 검색 시간 지연으로 검색량 제한 num_of_searches
    for nearby_hospital in res.json()['results'][0:num_of_searches]:
        name = nearby_hospital['name']
        h_lat = str(nearby_hospital['geometry']['location']['lat'])
        h_lng = str(nearby_hospital['geometry']['location']['lng'])
        place_id = nearby_hospital['place_id']
        # 병원정보  get_hospital_info
        hospital_info = get_hospital_info(place_id)
        address = hospital_info.get('address')
        phone = hospital_info.get('phone')
        # 거리 get_distance
        distance = get_distance(lat, lng, place_id)
        print(name, address, phone, distance)
        data = {
            'name': name,
            'address': address,
            'phone': phone,
            'distance': distance,
            'h_lat': h_lat,
            'h_lng': h_lng
        }
        result_list.append(SearchInfo(**data))
    print('검색 개수:  ', len(res.json()['results']))
    return result_list
