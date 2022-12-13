from random import randrange
from n_token import token_group
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from f import*

import requests



session = vk_api.VkApi(token=token_group)
longpoll = VkLongPoll(session)


def write_msg(user_id, message):
    session.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        msg = event.text.lower()
        user_id = event.user_id
        if msg == "привет":
            write_msg(user_id, "Чат-бот VKinder приветствует тебя. Давай найдем тебе пару! Чтобы начать, напиши - да")
        if msg == "да":
            informathion = user_info()
            data_y=data_year(informathion)
            sex_u= sex_change(informathion)
            city_user="2"
            status= "1"
            for i in informathion["response"]:
                if "city" not in i.keys():
                    write_msg(user_id, "Введите ваш город")
                    city_user = event.text.capitalize()
                    print(city_user)
                    continue
                elif i["relation"] == 0:
                    write_msg(user_id, "Введите свое семейное положение цифрой от 1 до 8, где: 1 — не женат/не замужем;"
                                       "2 — есть друг/есть подруга; 3 — помолвлен/помолвлена; 4 — женат/замужем;"
                                       "5 — всё сложно; 6 — в активном поиске; 7 — влюблён/влюблена;"
                                       "8 — в гражданском браке")
                    status= event.text
                    user_id = event.user_id
                    print(status)
                    continue
            searh_user= user_search(city_user, sex_u, data_y, status)
            print(searh_user)
            foto = get_foto(442362369)
            print (foto)
        if msg == "нет":
             write_msg(event.user_id, "Пока")



