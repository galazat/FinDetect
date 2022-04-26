from flask import Flask, redirect
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request
import requests
from mechanize import Browser
from mechanize import urlopen
import re
import mechanize
import json
import os
from apscheduler.schedulers.background import BackgroundScheduler
from subprocess import PIPE
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
import dnstwist
import json
import threading
import nmap

import asyncio
import configparser
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)

from threading import Timer
import queue
import random

import telebot
from telebot import types


from scapy.all import *
import threading


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///FinDetect.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.Text, default=False)
    url = db.Column(db.String(20), nullable=False)

    site_available = db.Column(db.Boolean, default=False)
    available_desc = db.Column(db.Text, default=False)
    auth_available = db.Column(db.Boolean, default=False)
    mobile_available = db.Column(db.Boolean, default=False)
    available_count = db.Column(db.Integer, default=False)

    nmap_decr_1 = db.Column(db.Text, default=False)
    nmap_decr_2 = db.Column(db.Text, default=False)
    nmap_decr_3 = db.Column(db.Text, default=False)
    nmap_decr_4 = db.Column(db.Text, default=False)

    nslookup_decr_1 = db.Column(db.Text, default=False)
    nslookup_decr_2 = db.Column(db.Text, default=False)

    whois_decr_1 = db.Column(db.Text, default=False)
    whois_decr_2 = db.Column(db.Text, default=False)
    whois_decr_3 = db.Column(db.Text, default=False)
    whois_decr_4 = db.Column(db.Text, default=False)

    social_decr_1 = db.Column(db.Text, default=False)
    social_decr_2 = db.Column(db.Text, default=False)
    social_decr_3 = db.Column(db.Text, default=False)
    tech_decr = db.Column(db.Text, default=False)

    def __repr__(self):
        return f"<id={self.id}, title={self.title} , url={self.url}>"



def get_status(id=0):
    if (id==0):
        services = Service.query.order_by(Service.id).all()
        for i in services:
            try:
                print('Try to connect ...')
                response = requests.head(i.url, timeout=5)
                status_code = response.status_code
                reason = response.reason
                response_time = response.elapsed.total_seconds()
            except requests.exceptions.ConnectionError:
                status_code = '000'
                reason = 'Site not available'
                response_time = '10 sec'
            website_status = (status_code, reason, response_time)

            Code = website_status[0]
            Status = website_status[1]
            ResponseTime = website_status[2]
            print(i.url)
            print('Code:', website_status[0], '| Status:', website_status[1], '| Responce time:', website_status[2])
            i.available_desc = (str(Code) + " " + str(Status) + " " + str(ResponseTime))
            if (reason == "Site not available"):
                i.site_available = 0
                i.available_count += 1
                print(i.site_available)
                print("i.available_count: ", i.available_count)
                db.session.commit()
            else:
                i.site_available = 1
                i.available_count = 0
                print(i.site_available)
                db.session.commit()
                print("i.available_count: ", i.available_count)
                # if (i.available_count == 2):
                #     get_report()

            #test = Service.query.filter_by(id=1).all()
            # Service.query.filter_by(id=3).delete()
            # db.session.commit()
    else:
        print("start")
        service = Service.query.filter_by(id=id).all()
        for i in services:
            try:
                print('Try to connect ...')
                response = requests.head(i.url, timeout=5)
                status_code = response.status_code
                reason = response.reason
                response_time = response.elapsed.total_seconds()
            except requests.exceptions.ConnectionError:
                status_code = '000'
                reason = 'Site not available'
                response_time = '10 sec'
            website_status = (status_code, reason, response_time)

            Code = website_status[0]
            Status = website_status[1]
            ResponseTime = website_status[2]
            print(i.url)
            print('Code:', website_status[0], '| Status:', website_status[1], '| Responce time:', website_status[2])
            i.available_desc = (str(Code) + " " + str(Status) + " " + str(ResponseTime))
            if (reason == "Site not available"):
                i.site_available = 0
                i.available_count += 1
                print(i.site_available)
                print("i.available_count: ", i.available_count)
                db.session.commit()
            else:
                i.site_available = 1
                i.available_count = 0
                print(i.site_available)
                db.session.commit()
                print("i.available_count: ", i.available_count)


def get_domain_info(id=0):
    print('DOMAIN id', id)
    if (id==0):
        services = Service.query.order_by(Service.id).all()
        for i in services:
            try:
                url = (re.search('[A-Za-z0-9]{2,20}\.[com|ru|org|us|en|fr|]{2,4}', i.url)).group(0)
                print('URL : ',url)
                nslookup = subprocess.run(["nslookup", url], stdout=PIPE, stderr=PIPE)
                i.nslookup_decr_1 = (re.search('[A-Za-z0-9]{2,20}\.[com|ru|org|us|en|fr|]{2,4}', (nslookup.stdout).decode("utf-8"))).group(0)
                print('nslookup domain : ',i.nslookup_decr_1)
                tmp = (re.findall(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", (nslookup.stdout).decode("utf-8") ))
                i.nslookup_decr_2 = tmp[2]
                print('nslookup address : ',i.nslookup_decr_2)
            except:
                i.nslookup_decr_1 = "Opps... There are problem on server ! We are work on it "
                print('oops...')            
            try:
                whois = subprocess.run(["whois", url], stdout=PIPE, stderr=PIPE)
                print('whois : ',whois) 
                tmp = (re.search('state:.{10,40}', (whois.stdout).decode("utf-8"))).group(0)
                print('1 :', (tmp.replace("state:", '')))
                i.whois_decr_1 = tmp.replace("state:", '')

                tmp = (re.search('registrar:.{10,30}', (whois.stdout).decode("utf-8"))).group(0)
                print('2 :', (tmp.replace("registrar:", '')))
                i.whois_decr_2 = tmp.replace("registrar:", '')

                tmp = (re.search('created:.{10,30}', (whois.stdout).decode("utf-8"))).group(0)
                print('3 :', (tmp.replace("created:", '')))
                i.whois_decr_3 = tmp.replace("created:", '')

                tmp = (re.search('free-date:.{5,20}', (whois.stdout).decode("utf-8"))).group(0)
                print('4 :', (tmp.replace("free-date:", '')))
                i.whois_decr_4 = tmp.replace("free-date:", '')
            except:
                i.tech_decr = "Opps... There are problem on server ! We are work on it "
            db.session.commit()
    else:
        print("start")
        service = Service.query.filter_by(id=id).all()
        for i in service:
            url = (re.search('[A-Za-z0-9]{2,20}\.[com|ru|org|us|en|fr|]{2,4}', i.url)).group(0)
            print("URL ", url)
            try:
                print(url)
                nslookup = subprocess.run(["nslookup", url], stdout=PIPE, stderr=PIPE)
                i.nslookup_decr_1 = (re.search('[A-Za-z0-9]{2,20}\.[com|ru|org|us|en|fr|]{2,4}', (nslookup.stdout).decode("utf-8"))).group(0)
                tmp = (re.findall(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", (nslookup.stdout).decode("utf-8") ))
                i.nslookup_decr_2 = tmp[2]
            except:
                i.nslookup_decr_1 = "Opps... There are problem on server ! We are work on it "
            try:
                whois = subprocess.run(["whois", url], stdout=PIPE, stderr=PIPE)
                print('whois : ',whois) 
                tmp = (re.search('state:.{10,40}', (whois.stdout).decode("utf-8"))).group(0)
                print('1 :', (tmp.replace("state:", '')))
                i.whois_decr_1 = tmp.replace("state:", '')

                tmp = (re.search('registrar:.{10,30}', (whois.stdout).decode("utf-8"))).group(0)
                print('2 :', (tmp.replace("registrar:", '')))
                i.whois_decr_2 = tmp.replace("registrar:", '')

                tmp = (re.search('created:.{10,30}', (whois.stdout).decode("utf-8"))).group(0)
                print('3 :', (tmp.replace("created:", '')))
                i.whois_decr_3 = tmp.replace("created:", '')

                tmp = (re.search('free-date:.{5,20}', (whois.stdout).decode("utf-8"))).group(0)
                print('4 :', (tmp.replace("free-date:", '')))
                i.whois_decr_4 = tmp.replace("free-date:", '')
            except:
                i.tech_decr = "Opps... There are problem on server ! We are work on it "
            db.session.commit()


def get_fishing(id=0):
    if (id==0):
        services = Service.query.order_by(Service.id).all()
        for i in services:
            url = (re.search('[A-Za-z0-9]{2,20}\.[com|ru|org|us|en|fr|]{2,4}', i.url)).group(0)
            print(url)
            dnstwist = subprocess.run(["dnstwist", '--registered', '--format', 'json', url], stdout=PIPE, stderr=PIPE)
            dns = json.loads((dnstwist.stdout).decode('utf-8'))
            print('get dnstwist')
            try:
                j=0
                while dns[j]:
                    try:
                        if(('172.' in str(dns[j]['dns_a'][0])) or ("!ServFail" in str(dns[j]['dns_a'][0]))):
                            dns.pop(j)
                            j -=1
                        else:
                            print(dns[j]['dns_a'][0], dns[j]['domain'])
                    except:
                        pass
                    j += 1
            except:
                pass

            fishing_ip = [0 for k in range(len(dns)-1)] #[[0] * 2] * len(dns)
            for m in range(0,len(dns)-1):
                fishing_ip[m] = dns[m+1]['dns_a'][0]

            fishing_domain = [0 for k in range(len(dns)-1)] #[[0] * 2] * len(dns)
            for m in range(0,len(dns)-1):
                fishing_domain[m] = dns[m+1]['domain']


                # fishing[j][1] = (dns[j]['domain'])
                # print(dns[j]['dns_a'][0], dns[j]['domain'], j)
                # if (j > 1):
                #     print(fishing[j-1], fishing[j])
            print(','.join(str(e) for e in fishing_ip))
            print(','.join(str(e) for e in fishing_domain))
            i.social_decr_1 = (','.join(str(e) for e in fishing_ip))
            i.social_decr_2 = (','.join(str(e) for e in fishing_domain))
            db.session.commit()
        print("DONE")
    else:
        print("start")
        service = Service.query.filter_by(id=id).all()
        print(id)
        for i in service:
            url = (re.search('[A-Za-z0-9]{2,20}\.[com|ru|org|us|en|fr|]{2,4}', i.url)).group(0)
            print(url)
            dnstwist = subprocess.run(["dnstwist", '--registered', '--format', 'json', url], stdout=PIPE, stderr=PIPE)
            dns = json.loads((dnstwist.stdout).decode('utf-8'))
            print('get dnstwist')
            try:
                j=0
                while dns[j]:
                    try:
                        if(('172.' in str(dns[j]['dns_a'][0])) or ("!ServFail" in str(dns[j]['dns_a'][0]))):
                            dns.pop(j)
                            j -=1
                        else:
                            print(dns[j]['dns_a'][0], dns[j]['domain'])
                    except:
                        pass
                    j += 1
            except:
                pass
            
            fishing_ip = [0 for k in range(len(dns)-1)] #[[0] * 2] * len(dns)
            for m in range(0,len(dns)-1):
                fishing_ip[m] = dns[m+1]['dns_a'][0]

            fishing_domain = [0 for k in range(len(dns)-1)] #[[0] * 2] * len(dns)
            for m in range(0,len(dns)-1):
                fishing_domain[m] = dns[m+1]['domain']


                # fishing[j][1] = (dns[j]['domain'])
                # print(dns[j]['dns_a'][0], dns[j]['domain'], j)
                # if (j > 1):
                #     print(fishing[j-1], fishing[j])
            print(','.join(str(e) for e in fishing_ip))
            print(','.join(str(e) for e in fishing_domain))
            i.social_decr_1 = (','.join(str(e) for e in fishing_ip))
            i.social_decr_2 = (','.join(str(e) for e in fishing_domain))
            db.session.commit()
            print("DONE")
    print('---------------------------------')
    print(fishing_ip)
    print(fishing_domain)


def get_report(id):
    service = Service.query.filter_by(id=id).all()
    for i in services:
        create_report(id)


checkTelegram = True
info = []

def change_checkTelegram():
    global checkTelegram
    checkTelegram = True
    print(change_checkTelegram)


scheduler = BackgroundScheduler()
scheduler.add_job(func=get_status, trigger="interval", seconds=(random.randint(120,240)))
scheduler.add_job(func=get_domain_info, trigger="interval", seconds=86400)
scheduler.add_job(func=get_fishing, trigger="interval", seconds=86400)
scheduler.add_job(func=change_checkTelegram, trigger="interval", seconds=900)
scheduler.start()


#my_thread = threading.Thread(target=get_fishing)
#my_thread.start()


@app.route('/', methods= ['GET'])
def index():
    services = Service.query.order_by(Service.id).all()    
    return render_template('index.html', services=services)


@app.route('/adding', methods=['POST','GET'])
def adding():
    if request.method == "POST":
        title = request.form['title']
        short_description = request.form['short_description']
        description = request.form['description']
        url = request.form['url']
        admin_token = request.form['admin_token']
        print('URL ', url)

        if (admin_token == "ShecyYTWcvdt3835btr52frRDsfcwr2f"):
            service = Service(title=title, short_description=short_description, description=description, url=url)
            try:
                db.session.add(service)
                print("add")
                db.session.commit()
            except:
                return "Opps.. где-то затаилась ошибка"
            print(2)
            get_status()
            print("ID ",service.id)
            get_domain_info(service.id)
            get_fishing(service.id)
            print(4)
            return redirect('/')
        else:
            return redirect('/error')
    else:
        return render_template('add_service.html')

@app.route('/view_service/<int:id>')
def view(id):
    service = Service.query.get(id)
    fishing_ip = (service.social_decr_1).split(",")
    fishing_domain = (service.social_decr_2).split(",")
    return render_template('view_service.html', service=service, fishing=zip(fishing_ip,fishing_domain) )

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/policy', methods=['GET'])
def policy():
    return render_template('policy.html')

@app.route('/team', methods=['GET'])
def team():
    return render_template('policy.html')

@app.route('/feedback', methods=['GET'])
def feedback():
    return render_template('fitback.html')

@app.route('/error', methods=['GET'])
def error():
    return render_template('error.html')



@app.route('/telegram/<int:id>')
def telegram_search(id):
    global checkTelegram, info

    #service = Service.query.get(id)
    titles = []
    services = Service.query.order_by(Service.id).all()
    for i in services:
        titles.append(i.title)

    def telegram_start(our_service):
        print(our_service)
        ALERT_INFORMATION = []
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

            # user_input_channel = input('enter entity(telegram URL or entity id):')
            file_url = open("tg_url.txt", "r")
            lines = file_url.readlines()
            for entity in lines:
                my_channel = await client.get_entity(entity)
                offset_id = 0
                limit = 25  # максималное число сообщений за 1 раз
                all_messages = []
                total_messages = 0
                total_count_limit = 50  # Сколько ввобще сообщений нужно

                while True:
                    print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
                    history = await client(GetHistoryRequest(
                        peer=my_channel,
                        offset_id=offset_id, offset_date=None,
                        add_offset=0,
                        limit=limit, max_id=0, min_id=0,
                        hash=0
                    ))
                    if not history.messages:
                        break
                    messages = history.messages
                    for message in messages:
                        all_messages.append(message.to_dict())
                    offset_id = messages[len(messages) - 1].id
                    total_messages = len(all_messages)
                    if total_count_limit != 0 and total_messages >= total_count_limit:
                        break

                def use_regex(input, bank, alert):
                    bank = str(bank)
                    alert = str(alert)
                    result = re.search(rf'{bank}.{{0,20}}{alert}', input)
                    if result is not None:
                        return True
                    else:
                        result = re.search(rf'{alert}.{{0,20}}{bank}', input)
                        if result is not None:
                            return True
                        else:
                            return False

                alert_words = ["сбой", "не работает", "упал", "оффлайн", "офлайн", "не онлайн", "не открывается", "не загружается", "не доступен", "лежит", "отвалилось", "проблемы", "лег", "не отвечает", "нет возможности"]
                for mes in all_messages:
                    user_message = str(mes[list(mes.keys())[4]]).lower()
                    time_message = str(mes[list(mes.keys())[3]]).lower()
                    for alert_word in alert_words:
                        for title in our_service:
                            if use_regex(user_message, title.lower(), alert_word):
                                ALERT_INFORMATION.append([entity[:-1], user_message, time_message, title])
                                print(ALERT_INFORMATION,  alert_word, title,'\n')
        with client:
            client.loop.run_until_complete(main(phone))
        return ALERT_INFORMATION

    if (checkTelegram):
        info.clear()
        print(titles)
        info = telegram_start(titles)
        checkTelegram = False
        print("info update:",info)
    else:
        print("info last:",info)
        pass
    
    alertMess = []
    target = Service.query.get(id)
    for k in info:
        print(k,'\n', target.title, k[3])
        if (target.title == k[3]):
            alertMess.append(k)
            print('mess: ',k)

    # return render_template('telegram.html', service=service, fishing=zip(), alert_message=0)
    return render_template('telegram.html', service=target, alert_count=alertMess)




@app.route('/nmap_search/<int:id>')
def nmap_search(id):
    service = Service.query.get(id)
    # nmap_path = [r"C:\Program Files (x86)\Nmap\nmap.exe", ]  # Необходимо скачать nmap для корректной работы
    # scanner = nmap.PortScanner(nmap_search_path=nmap_path)
    scanner = nmap.PortScanner()

    def nmap_ping_scan(ip_addr, mask):
        hosts = list()
        scanner.scan(hosts=ip_addr + "/" + mask, arguments=' - n - sP - PE - PA21, 23, 80, 3389')
        hosts_list = [(x, scanner[x]['status']['state']) for x in scanner.all_hosts()]
        print(hosts_list)
        for host, status in hosts_list:
            print('{0}:{1}'.format(host, status))
            if status == 'up':
                hosts.append(str(host))
        return hosts

    def nmap_scan_popular(network_prefix):
        nmap_information = ""
        print(network_prefix)
        nm = nmap.PortScanner()
        # Настроить параметры сканирования nmap
        scan_raw_result = nm.scan(hosts=network_prefix, arguments='-v -n -A')
        print(scan_raw_result)
        '''ports='1-8080','''  # 3 минуты
        # Анализировать результаты сканирования
        for host, result in scan_raw_result['scan'].items():
            if result['status']['state'] == 'up':
                nmap_information += '#' * 17 + 'Host:' + host + '#' * 17 + "<br>"
                for os in result['osmatch']:
                    nmap_information += "Операционная система:" + os['name'] + ' ' * 3 + "Точность:" + os[
                        'accuracy'] + "<br>"
                idno = 1
                try:
                    for port in result['tcp']:
                        try:
                            nmap_information += '-' * 17 + "Детали TCP - сервера" + '-' * 17 + "<br>"
                            nmap_information += 'Номер порта TCP:' + str(port) + "<br>"
                            idno += 1
                            try:
                                nmap_information += 'Статус:' + result['tcp'][port]['state'] + "<br>"
                            except:
                                pass
                            try:
                                nmap_information += 'Метод:' + result['tcp'][port]['reason'] + "<br>"
                            except:
                                pass
                            try:
                                nmap_information += 'Дополнительная информация:' + result['tcp'][port][
                                    'extrainfo'] + "<br>"
                            except:
                                pass
                            try:
                                nmap_information += 'Имя:' + result['tcp'][port]['name'] + "<br>"
                            except:
                                pass
                            try:
                                nmap_information += 'Версия:' + result['tcp'][port]['version'] + "<br>"
                            except:
                                pass
                            try:
                                nmap_information += 'Продукт:' + result['tcp'][port]['product'] + "<br>"
                            except:
                                pass
                            try:
                                nmap_information += 'CPE：' + result['tcp'][port]['cpe'] + "<br>"
                            except:
                                pass
                            try:
                                nmap_information += "Скрипт:" + result['tcp'][port]['script'] + "<br>"
                            except:
                                pass
                        except:
                            pass
                except:
                    pass

                idno = 1
                try:
                    for port in result['udp']:
                        try:
                            nmap_information += '-' * 17 + "Детали сервера UDP" + '-' * 17 + "<br>"
                            nmap_information += 'Номер порта UDP:' + str(port) + "<br>"
                            idno += 1
                            try:
                                nmap_information += 'Статус:' + result['udp'][port]['state'] + "<br>"
                            except:
                                pass
                            try:
                                nmap_information += 'Метод:' + result['udp'][port]['reason'] + "<br>"
                            except:
                                pass
                            try:
                                nmap_information += 'Дополнительная информация:' + result['udp'][port][
                                    'extrainfo'] + "<br>"
                            except:
                                pass
                            try:
                                nmap_information += 'Имя:' + result['udp'][port]['name'] + "<br>"
                            except:
                                pass
                            try:
                                nmap_information += 'Версия:' + result['udp'][port]['version'] + "<br>"
                            except:
                                pass
                            try:
                                nmap_information += 'Продукт:' + result['udp'][port]['product'] + "<br>"
                            except:
                                pass
                            try:
                                nmap_information += 'CPE：' + result['udp'][port]['cpe'] + "<br>"
                            except:
                                pass
                            try:
                                nmap_information += "Скрипт:" + result['udp'][port]['script'] + "<br>"
                            except:
                                pass
                        except:
                            pass
                except:
                    pass
        return nmap_information

    def cut_protocol(domain):
        url = re.compile(r"https?://(\.)?")
        url = url.sub('', domain).strip().strip('/')
        return str(url)
    print("Разрешение адреса: " + str(service.url))
    full_url = str(service.url)
    domain_name = cut_protocol(full_url)

    ip_list = []
    try:
        ais = socket.getaddrinfo(domain_name, 0, 0, 0, 0)
        for result in ais:
            ip_list.append(result[-1][0])
        ip_list = list(set(ip_list))
        print('Разрешение выполнилось удачно')
    except Exception:
        print('Неудалось рарешить адрес')

    print(ip_list)

    ip_addr = ip_list[0]
    mask = '24'
    nmap_information_hosts = ""
    nmap_information = ""
    # hosts = nmap_ping_scan(ip_addr, mask)
    # print(hosts)
    # for host in hosts:
        # nmap_information_hosts += "<br>" + str(host) + "<br>"

    print("Старт анализа...")
    nmap_information += nmap_scan_popular(ip_addr)
    if nmap_information == "":
        nmap_information = "Популярных открытых портов не найдено"
    print(nmap_information)

    return render_template('nmap.html', service=service, nmap_information_hosts=nmap_information_hosts, nmap_information=nmap_information)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    # app.run(debug=False)


