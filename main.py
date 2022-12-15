from random import randrange
from n_token import token_group
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from f import*
import requests
from database import*






def write_msg(user_id, message):
    session.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})

bot="start"
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        msg = event.text.lower()
        user_id = event.user_id
        if bot == "status":
            if msg.isdigit():
                write_msg(event.user_id, f"Семейное положение записано{msg}")
            else:
                write_msg(event.user_id, "Укажи семейное положение цифрами, например: 1, если не женат/не замужем")
            bot == "start"
            continue
        if bot=="age":
            if msg.isdigit():
                write_msg(event.user_id, f"Год рождения {msg}записан")
            else:
                write_msg(event.user_id, "Укажи год рождения цифрами")

            bot="start"
            continue
        if bot=="city":
            if msg:
                write_msg(event.user_id, f"Город{msg}записан")
            bot="start"
            continue
        if bot=="start":
            if msg=="привет":
                write_msg(user_id, "Чат-бот VKinder приветствует тебя. Давай найдем тебе пару! Чтобы начать, напиши - да")
            if msg == "да":
                write_msg(user_id,"Отлично! Начнем поиск!")
                informathion = user_info()
                print(informathion)
                if informathion["relation"] == 0:
                    write_msg(user_id, "Введите свое семейное положение цифрой от 1 до 8, где: 1 — не женат/не замужем;"
                                    "2 — есть друг/есть подруга; 3 — помолвлен/помолвлена; 4 — женат/замужем;"
                                     "5 — всё сложно; 6 — в активном поиске; 7 — влюблён/влюблена;"
                                     "8 — в гражданском браке")
                    bot = "status"
                if "bdate" not in informathion.keys():
                    write_msg(user_id, "Укажите год рождения, например 2000")
                    bot = "age"
                if "city" not in informathion.keys():
                    write_msg(user_id, "Введите ваш город")
                    bot = "city"
                    #sex_u = sex_change(informathion)
            #searh_user= user_search(city_user, sex_u, data_y, status)
                    #print(searh_user)
                    #foto = get_foto(442362369)
                   #print (foto)
           # if msg == "нет":
                #write_msg(event.user_id, "Пока")

