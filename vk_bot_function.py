import requests
from n_token import token_group, token_my
from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from datetime import datetime

PROTOCOL_VERSION: str = "5.131"

session = vk_api.VkApi(token=token_group)
longpoll = VkLongPoll(session)


def write_msg(user_id, message, attachment=None):
    session.method('messages.send', {'user_id': user_id,
                                     'message': message,
                                     'random_id': randrange(10 ** 7),
                                     'attachment': attachment})


def gender_convert(gender):
    return 1 if gender == 2 else 2


def age_range(bdate, params='from'):
    year = int(bdate.split('.')[2])
    current_datetime = datetime.now()
    data_now = current_datetime.year
    return data_now - year - 5 if params == 'from' else data_now - year + 5


def city_id(city):
     url = "https://api.vk.com/method/database.getCities"
     params = {
     "access_token": token_my,
     "v": PROTOCOL_VERSION,
     "country_id": 1,
     "q": city,
     "need_all": 0,
     "count": 1
        }
     response = requests.get(url, params=params)
     result = response.json()
     for i in result["response"]["items"]:
        city = i["id"]
        return city


def relation_check(relation):
    if 0 <= relation <= 8:
        return relation
    else:
        if relation == "не женат" or relation == "не замужем":
            relation = 1
        elif relation == "есть друг" or relation == "есть подруга":
            relation = 2
        elif relation == "помолвлен" or relation == "помолвлена":
            relation = 3
        elif relation == "женат" or relation == "замужем":
            relation = 4
        elif relation == "все сложно":
            relation = 5
        elif relation == "в активном поиске":
            relation = 6
        elif relation == "влюблён" or relation == "влюблена":
            relation = 7
        elif relation == "в гражданском браке":
            relation = 8
        return relation


def user_info(user_id):
    url = "https://api.vk.com/method/users.get"
    params = {
        "access_token": token_my,
        "v": PROTOCOL_VERSION,
        "fields": "sex,bdate,city,relation",
        "user_ids": user_id
    }
    response = requests.get(url, params=params)
    result = response.json()
    for i in result["response"]:
        return i


def user_search(city_s, sex_s, age_from, age_to, relation_s):
    url = "https://api.vk.com/method/users.search"
    params = {
        "access_token": token_my,
        "v": PROTOCOL_VERSION,
        "sort": 0,
        "city": city_s,
        "sex": sex_s,
        'age_from': age_from,
        'age_to': age_to,
        "status": relation_s,
        "has_photo": 1,
        "count": 100
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        result = response.json()
        return result['response']['items']
    else:
        return None


def user_aggregation(city_s, sex_s, age_from, age_to, relation_s):
    profiles = user_search(city_s, sex_s, age_from, age_to, relation_s)
    profile_list = []
    for profile in profiles:
        if profile['is_closed'] == False:
            profile_list.append(profile)
    return profile_list


def get_foto(id_user_search):
    url = "https://api.vk.com/method/photos.get"
    params = {
        "access_token": token_my,
        "v": PROTOCOL_VERSION,
        "owner_id": id_user_search,
        "album_id": "profile",
        "extended": "1",
        "need_like": "1"

    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        result = response.json()
        return result['response']['items']
    else:
        return None


def photo_process(user_id, profile_id):
    photos = get_foto(profile_id)
    photos.sort(reverse=True, key=lambda item: (item["likes"]["count"], item["comments"]["count"]))
    cnt = 0
    write_msg(user_id, f"Хочешь познакомиться - лови ссылку  https://vk.com/id{profile_id}")
    for photo in photos:
        cnt += 1
        link = f'photo{profile_id}_{photo["id"]}'
        write_msg(user_id, f"фото {cnt}", attachment=link)
        if cnt == 3:
            break
