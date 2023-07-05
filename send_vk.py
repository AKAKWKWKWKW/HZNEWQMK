# -*- coding: utf-8 -*- 
import tempfile
import pydub
from pydub import AudioSegment
import urllib.request
import re
from pathlib import Path
import os, sys
import gtts
import glob
from urllib.request import urlopen
from urllib.parse import quote
import json
import vk_api
import requests
import random


def get_accounts():
	connection,q = connect_bomber()
	q.execute(f'SELECT token FROM ugc_vk_account WHERE status = "1" ORDER BY RAND() LIMIT 1')
	row = q.fetchone()[0]
	return row


def generate_url(text, ttype):
	cookies = {
        'PHPSESSID': '7g7tom1m0h0q3uagck8sjfdr8k',
        '_ym_uid': '1664207689207587883',
        '_ym_d': '1664207689',
        '_ym_isad': '1',
        '_ym_visorc': 'w',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ru,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'PHPSESSID=7g7tom1m0h0q3uagck8sjfdr8k; _ym_uid=1664207689207587883; _ym_d=1664207689; _ym_isad=1; _ym_visorc=w',
        'Origin': 'https://texttospeech.ru',
        'Referer': 'https://texttospeech.ru/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.114 YaBrowser/22.9.1.1095 Yowser/2.5 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Yandex";v="22"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    voice = 0
    if ttype == 'м':
    	voice = 5
    else:
    	voice = 6
    data = {
        'voice': voice,
        'text': text,
        'pitch': '1.0',
        'rate': '1.1',
        'format': 'mp3',
        'volume': '1.0',
        'hertz': '16000',
    }

    response = requests.post('https://texttospeech.ru/syn2.php', cookies=cookies, headers=headers, data=data).json()
    print(response)
    return f'https://texttospeech.ru/{response["file"]}'

def generate_ogg(url, codee):
	headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary1poS0cED8jULsAN2',
        'Origin': 'https://fconvert.ru',
        'Referer': 'https://fconvert.ru/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.114 YaBrowser/22.9.1.1095 Yowser/2.5 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Yandex";v="22"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = '------WebKitFormBoundary1poS0cED8jULsAN2\r\nContent-Disposition: form-data; name="file"\r\n\r\n{0}\r\n------WebKitFormBoundary1poS0cED8jULsAN2\r\nContent-Disposition: form-data; name="filelocation"\r\n\r\nonline\r\n------WebKitFormBoundary1poS0cED8jULsAN2\r\nContent-Disposition: form-data; name="target"\r\n\r\nOGG\r\n------WebKitFormBoundary1poS0cED8jULsAN2\r\nContent-Disposition: form-data; name="bitrate"\r\n\r\n128k\r\n------WebKitFormBoundary1poS0cED8jULsAN2\r\nContent-Disposition: form-data; name="frequency"\r\n\r\n16000\r\n------WebKitFormBoundary1poS0cED8jULsAN2\r\nContent-Disposition: form-data; name="channel"\r\n\r\n1\r\n------WebKitFormBoundary1poS0cED8jULsAN2\r\nContent-Disposition: form-data; name="type_converter"\r\n\r\naudio\r\n------WebKitFormBoundary1poS0cED8jULsAN2--\r\n'.format(url)

    response = requests.post('https://s1.fconvert.ru/fconvert.php', headers=headers, data=data).json()

    print(response)
    responce_two = requests.get(f'https://s1.fconvert.ru/upload/{response["id"]}/')
    with open(f'sound_vk/{codee}.ogg', 'wb') as f:
        f.write(responce_two.content)



def send_vk(url, ttype, text, codee):
	gen_url = generate_url()
	gen_file = generate_ogg(gen_url, codee)

    a = vk.method("docs.getMessagesUploadServer", {"type": "audio_message"})
    sdad = random.choice(glob.glob('*.ogg'))
    b = requests.post(a['upload_url'], files={'file': open(sdad, 'rb')}).json()
    c = vk.method("docs.save", {"file": b["file"]})
    d = 'doc{}_{}'.format(c['audio_message']['owner_id'], c['audio_message']['id'])
    vk.method('messages.send', {'peer_id': 1, 'attachment': d, "random_id": random.randint(1, 2147483647)})