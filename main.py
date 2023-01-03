from n_token import *
from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_bot_function import*
from datetime import datetime
import requests
from database import *



translator = {'relation': 'семейное положение: не женат/ не замужем, есть друг/есть подруга,' 
                          'помолвлен/помолвлена, женат/замужем, все сложно, '
                          'в активном поиске, влюблён/влюблена, в гражданском браке',
              'city': 'город'
              }

bot = "start"
requaries = []
params = {}
profile_list = []


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        msg = event.text.lower()
        user_id = event.user_id

        if bot == "relation":
            if msg:
                write_msg(event.user_id, f"Семейное положение - {msg} записано")
                params["relation"] = msg
            if requaries:
                bot = "cheking_params"
                write_msg(user_id, f"В вашем профиле недостаточно параметров для поиска,")
                write_msg(user_id, f"Введите {translator[requaries[0]]} ,")
            else:
                bot = "params_ok"
        if bot == "city":
            if msg:
                write_msg(event.user_id, f"Город {msg} записан")
                params["city"] = msg
            if requaries:
                bot = "cheking_params"
                write_msg(user_id, f"В вашем профиле недостаточно параметров для поиска,")
                write_msg(user_id, f"Введите {translator[requaries[0]]} ,")
            else:
                bot = "params_ok"

        if bot == "photo_process":
            if msg == "далее":
                profile_id = profile_list.pop()['id']
                while check_form(conn, user_id, profile_id):
                    profile_id = profile_list.pop()['id']
                else:
                    add = add_form(conn, user_id, profile_id)
                if profile_id:
                    photo_process(user_id, profile_id)
                    write_msg(user_id, f"Чтобы посмотреть следующую анкету напишите - 'далее'")
                    bot = "photo_process"
                else:
                    bot = "start"
                    write_msg(user_id, f"Найденные анкеты подошли к концу, что бы искать ещё пиши 'да'")

        if bot == "start":
            if msg == "привет":
                write_msg(user_id,
                          "Чат-бот VKinder приветствует тебя. Давай найдем тебе пару! Чтобы начать, напиши - да")
                continue
            if msg == "да":
                write_msg(user_id, "Отлично! Начнем поиск!")
                informathion = user_info(user_id)
                if "city" not in informathion.keys():
                    requaries.append("city")
                else:
                    bot = "cheking_params"
                if informathion['relation'] == 0:
                    requaries.append("relation")
                else:
                    bot = "cheking_params"
                if requaries:
                    write_msg(user_id, f"В вашем профиле недостаточно параметров для поиска")
                    write_msg(user_id, f"Введите {translator[requaries[0]]}")
                else:
                    profile_list = user_aggregation(informathion['city']['id'],
                                                    gender_convert(informathion['sex']),
                                                    age_range(informathion['bdate']),
                                                    age_range(informathion['bdate'], params='to'),
                                                    informathion["relation"])

                    if len(profile_list) > 0:
                        profile_id = profile_list.pop()['id']
                        while check_form(conn, user_id,  profile_id):
                            profile_id = profile_list.pop()['id']
                        else:
                            add = add_form(conn, user_id, profile_id)
                        photo_process(user_id, profile_id)
                        write_msg(user_id, f"Чтобы посмотреть следующую анкету напишите 'далее'")
                        bot = "photo_process"

        if bot == "cheking_params":
            if requaries:
                param = requaries.pop()
                bot = param
                continue
            else:
                bot = "params_ok"
                continue

        if bot == "params_ok":
            if "city" in informathion:
                city_element = informathion['city']['id']
            else:
                city_element = city_id(params['city'])
            if informathion['relation'] != 0:
                relation_element = informathion['relation']
            else:
                relation_element = relation_check(user_id, params['relation'])

            profile_list = user_aggregation(city_element,
                                            gender_convert(informathion['sex']),
                                            age_range(informathion['bdate']),
                                            age_range(informathion['bdate'], params='to'),
                                            relation_element)
            if len(profile_list) > 0:
                profile_id = profile_list.pop()['id']
                while check_form(conn, user_id, profile_id):
                    profile_id = profile_list.pop()['id']
                else:
                    add = add_form(conn, user_id, profile_id)
                photo_process(user_id, profile_id)
                write_msg(user_id, f"Чтобы посмотреть следующую анкету напишите 'далее'")
                bot = "photo_process"