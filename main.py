import random
from n_token import*
from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from f import*
import requests
from database import*


bot="start"
requaries = []
params = {}
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        msg = event.text.lower()
        user_id = event.user_id
        if bot == "relation":
            if msg.isdigit():
                write_msg(event.user_id, f"Семейное положение записано - {msg} ")
                params["relation"] = msg
                if requaries:
                    bot = "cheking_params"
                else:
                    bot = "params_ok"

        if bot == "bdate":
            if msg.isdigit():
                write_msg(event.user_id, f"Год рождения {msg} записан")
                params["bdate"] = msg
            else:
                write_msg(event.user_id, "Укажи год рождения цифрами")
            if requaries:
                bot = "cheking_params"
            else:
                bot = "params_ok"

        if bot == "city":
            if msg:
                write_msg(event.user_id, f"Город {msg} записан")
                params["city"] = msg
            if requaries:
                bot = "cheking_params"
            else:
                bot = "params_ok"

        if bot == "start":
            if msg == "привет":
                write_msg(user_id, "Чат-бот VKinder приветствует тебя. Давай найдем тебе пару! Чтобы начать, напиши - да")
                continue
            if msg == "да":
                write_msg(user_id,"Отлично! Начнем поиск!")
                informathion = user_info(user_id)
                if "relation" not in informathion.keys():
                    requaries.append("relation")
                else:
                    status = informathion["relation"]

                if "bdate" not in informathion.keys():
                    requaries.append("bdate")
                else:
                    data_y = data_year(informathion["bdate"])

                if "city" not in informathion.keys():
                    requaries.append("city")
                else:
                    city_user = city_id(informathion["city"])

                bot = "cheking_params"

                if bot == "cheking_params":
                    if requaries:
                        param = requaries.pop()
                        write_msg(user_id, f"Укажите {param}")
                        bot = param
                        continue
                    else:
                        bot = "params_ok"
                        continue

                if bot == "params_ok":
                    write_msg(user_id, f"Получены данные для поиска {params}")
                    bot = "start"
                    print(params)
                    print(requaries)
                    city_user=1
                    status=0
                    data_y=2000
                    #city_user=city_id("")
                    sex_u = sex_change(informathion["sex"])
                    # #status= relation_check("")
                    searh_user= user_search(city_user, sex_u, data_y, status)
                    select_search= select_random(searh_user)
                    while check_form(conn, user_id,select_search):
                        select_search= select_random(searh_user)
                    else:
                       add = add_form(conn, user_id, select_search)
                    foto = get_foto(select_search)
                    foto_popular= popular_foto(foto)
                    send_photo(user_id,select_search,foto_popular)
                    write_msg(user_id, f"Хочешь познакомиться - лови ссылку  https://vk.com/id{select_search}")
                    write_msg(user_id, f"Хочешь продолжить, напиши - да")
            if msg == "нет":
                write_msg(event.user_id, "Пока")

