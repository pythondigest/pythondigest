# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import json
import os
import time
from urllib.error import HTTPError
from urllib.request import urlretrieve

import requests
import tweepy
import twx
import vk
from django.conf import settings
from twx.botapi import TelegramBot


def init_auth(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


def download_image(url):
    try:
        file_path = os.path.abspath(os.path.split(url)[-1])
        urlretrieve(url, file_path)
    except IndexError as e:
        print(e)
        file_path = None
    except HTTPError as e:
        print(e)
        file_path = None
    return file_path


def send_tweet_with_media(api, text, image):
    if 'http://' not in image and 'https://' not in image:
        assert os.path.isfile(image)
        file_path = image

    else:
        # качаем файл из сети
        file_path = download_image(image)

    assert file_path is not None, "Not found image (for twitter)"
    api.update_with_media(file_path, text)


class Gitter:
    """
    Gitter API wrapper
    URL: https://developer.gitter.im/docs/welcome
    """

    def __init__(self, token):
        """token: access_token
        """
        self.token = token
        self.room_id_dict = self.get_room_id_dict()

    def get_rooms(self):
        """get all room information
        """
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token),
        }
        r = requests.get('https://api.gitter.im/v1/rooms', headers=headers)

        return r.json()

    def get_room_id_dict(self):
        """
        """
        room_id_dict = {}
        for room in self.get_rooms():
            if room['githubType'] != 'ONETOONE':
                room_id_dict[room['uri']] = room['id']

        return room_id_dict

    def send_message(self, room, text):
        """send message to room
        """
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token),
        }
        room_id = self.room_id_dict.get(room)
        url = 'https://api.gitter.im/v1/rooms/{room_id}/chatMessages'.format(room_id=room_id)
        payload = {'text': text}
        r = requests.post(url, data=json.dumps(payload), headers=headers)

        return r


def post_to_wall(api, owner_id, message, **kwargs):
    data_dict = {
        'from_group': 1,
        'owner_id': owner_id,
        'message': message,
    }
    data_dict.update(**kwargs)
    return api.wall.post(**data_dict)


def send_message(api, user_id, message, **kwargs):
    data_dict = {
        'user_id': user_id,
        'message': message,
    }
    data_dict.update(**kwargs)
    return api.messages.send(**data_dict)


def get_pydigest_users():
    return [
        197644,  # Кирилл Шерстюк https://vk.com/id197644
        156281315,  # Дмитрий Мусин https://vk.com/id156281315
    ]


def get_gitter_chats():
    return [
        'pythondigest/pythondigest',
        'dev-ua/python',
    ]


def get_pydigest_groups():
    return [
        (-96469126, 1),  # https://vk.com/pynsk
        (-1540917, 0),  # https://vk.com/python_developers
        (-54001977, 0),  # https://vk.com/pythonic_way
        (-52104930, 0),  # https://vk.com/club52104930
        (-24847633, 1),  # https://vk.com/club24847633     #
        (-69108280, 0),  # https://vk.com/pirsipy
        (-37392018, 1),  # python_for_fun
        (-75836319, 0),  # https://vk.com/flask_community
        (-76525381, 0),  # https://vk.com/iteapro
    ]
    # return [
    #     (-105509411, 1),  # тестовая группа
    # ]


def pub_to_gitter(text, token):
    # gitter
    gitter = Gitter(token)

    for chat in get_gitter_chats():
        gitter.send_message(chat, text)
        time.sleep(1)


def pub_to_twitter(text, image_path, api):
    send_tweet_with_media(api, text, image_path)


def pub_to_vk_users(text, api):
    user_text = "Привет. Вышел новый дайджест. Пример текста\n"
    user_text += text
    for user_id in get_pydigest_users():
        print("User ", user_id)
        res = send_message(api, user_id=user_id, message=user_text)
        time.sleep(1)
        print(res)


def pub_to_vk_groups(text, attachments, api):
    for groupd_id, from_group in get_pydigest_groups():
        print(groupd_id, from_group)
        res = post_to_wall(api, groupd_id, text, **{'attachments': attachments, 'from_group': from_group})
        print(res)
        time.sleep(1)


def pub_to_telegram(text, bot_token, tg_channel):
    tgm_bot = TelegramBot(bot_token)
    answer = tgm_bot.send_message(tg_channel, text).wait()
    if isinstance(answer, twx.botapi.Error):
        print("error code: %s\nerror description: %s\n",
              answer.error_code,
              answer.description)
    else:
        print('OK')


def pub_to_slack(text, digest_url, digest_image_url, ifttt_key):
    url = 'https://maker.ifttt.com/trigger/pub_digest/with/key/{}'.format(ifttt_key)

    data = {
        'value1': text,
        "value2": digest_url,
        "value3": digest_image_url
    }

    requests.post(
        url,
        json=data
    )


def pub_to_all(text, digest_url, digest_image_url):
    """
    digest_url ='http://pythondigest.ru/issue/101/'
    :param digest_url:
    :return:
    """
    session = vk.AuthSession(app_id=settings.VK_APP_ID,
                             user_login=settings.VK_LOGIN,
                             user_password=settings.VK_PASSWORD,
                             scope='wall,messages')
    api = vk.API(session)

    twitter_text = 'Вот и свежий выпуск дайджеста новостей о #python. Приятного чтения: {}'.format(digest_url)
    twitter_api = init_auth(settings.TWITTER_CONSUMER_KEY,
                            settings.TWITTER_CONSUMER_SECRET,
                            settings.TWITTER_TOKEN,
                            settings.TWITTER_TOKEN_SECRET)

    pub_to_slack(text, digest_url, digest_image_url, settings.IFTTT_MAKER_KEY)
    pub_to_vk_groups(text, digest_url, api)
    pub_to_telegram(text, settings.TGM_BOT_ACCESS_TOKEN, settings.TGM_CHANNEL)
    pub_to_vk_users(text, api)
    pub_to_gitter('\n'.join(text.split('\n')[1::]), settings.GITTER_TOKEN)
    pub_to_twitter(twitter_text, digest_image_url, twitter_api)
