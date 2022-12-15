import requests
from n_token import*
from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import json
import re
#class VKClient:
# def __init__(self, token= None, user_id=None):
# self.token = my_token
# self.user_id = user_id

PROTOCOL_VERSION: str = "5.131"

session = vk_api.VkApi(token=token_group)
longpoll = VkLongPoll(session)


def bot():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.text.lower()
            user_id = event.user_id

def write_msg(user_id, message):
    session.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})

def user_info():
    url = "https://api.vk.com/method/users.get"
    params = {
             "access_token": my_token,
             "v": PROTOCOL_VERSION,
             "fields": "sex,bdate,city,relation"
    }

    response = requests.get(url, params=params)
    result = response.json()
    for i in result["response"]:
        return i



def user_search(city_s,sex_s,birth_year_s,relation_s):
    url = "https://api.vk.com/method/users.search"
    params = {
             "access_token": my_token,
             "v": PROTOCOL_VERSION,
             "sort": 0,
             "city":city_s,
             "sex":sex_s,
             "fields": "domain",
             "birth_year": birth_year_s,
             "status": relation_s,
             "has_photo": 1
    }

    response = requests.get(url, params=params)
    result = response.json()
    result2 = result["response"]
    return result2

def get_foto(id_user_search):
    url = "https://api.vk.com/method/photos.get"
    params = {
             "access_token": my_token,
             "v": PROTOCOL_VERSION,
             "owner_id": - "id_user_search",
             "extended": "1",
             "need_like":"1"
    }

    response = requests.get(url, params=params)
    result = response.json()
    return result

def data_year(n):
    for element in n["response"]:
        line = element["bdate"]
        search = re.search('(\d{4})', line)
        return search.group()
def sex_change(n):
    for element in n["response"]:
        sex1 = element["sex"]
        if sex1 == 2:
            result=1
        else:
            result=2
        return result



