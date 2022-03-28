from collections import namedtuple
import requests
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

Message = namedtuple('Message', 'protocol url domain')
messages = []
Info = namedtuple('Info', 'Code Status ResponseTime')
information = []


def get_status(url):
    try:
        print('Попытка подключения...')
        response = requests.head(url, timeout=5)
        status_code = response.status_code
        reason = response.reason
        response_time = response.elapsed.total_seconds()
    except requests.exceptions.ConnectionError:
        status_code = '000'
        reason = 'Сайт не доступен'
        response_time = '10 секунд'
    website_status = (status_code, reason, response_time)
    return website_status


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')


@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html', information=information)


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
    print(site)
    print('Код:', website_status[0], '| Статус:', website_status[1], '| Время ответа:', website_status[2])
    information.append(Info(Code, Status, ResponseTime))
    print(information)
    return redirect(url_for('main'))

@app.route('/clear', methods=['POST'])
def clear():
    for i in range(len(information)):
        information[i] = ""
    return redirect(url_for('main'))
