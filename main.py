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

import asyncio
import configparser
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)

from threading import Timer
import queue

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
                i.available_count = 0
                print(i.site_available)
                db.session.commit()
            else:
                i.site_available = 1
                i.available_count += 1
                print(i.site_available)
                db.session.commit()
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
                i.available_count = 0
                print(i.site_available)
                db.session.commit()
            else:
                i.site_available = 1
                i.available_count += 1
                print(i.site_available)
                db.session.commit()


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
                        if('172.' in str(dns[j]['dns_a'][0])):
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
                        if('172.' in str(dns[j]['dns_a'][0])):
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





scheduler = BackgroundScheduler()
scheduler.add_job(func=get_status, trigger="interval", seconds=1800)
scheduler.add_job(func=get_domain_info, trigger="interval", seconds=86400)
scheduler.add_job(func=get_fishing, trigger="interval", seconds=86400)
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





@app.route('/find_in_telegram', methods=['GET'])
def telegram_search():
    def telegram_start():
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
            ALERT_COUNT = 0 # количество алертов
            ALERT_INFO = [] # на какие банки пришлись алерты
            ALERT_MESSAGE = []
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

            #user_input_channel = input('enter entity(telegram URL or entity id):')
            file_url = open("tg_url.txt", "r")
            lines = file_url.readlines()
            for entity in lines:
                my_channel = await client.get_entity(entity)
                offset_id = 0
                limit = 5  # максималное число сообщений за 1 раз
                all_messages = []
                total_messages = 0
                total_count_limit = 10  # Сколько ввобще сообщений нужно

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

                for mes in all_messages:
                    user_message = str(mes[list(mes.keys())[4]]).lower()
                    file_banks = open("banks.txt", "r", encoding='utf-8')
                    lines_banks_file = file_banks.readlines()
                    file_alert_words = open("alert_words.txt", "r", encoding='utf-8')
                    lines_alert_words_file = file_alert_words.readlines()
                    for line_bank in lines_banks_file:
                        for line_alert in lines_alert_words_file:
                            if use_regex(user_message, str(line_bank[:-1]), str(line_alert[:-1])):
                                ALERT_COUNT += + 1
                                ALERT_INFO.append(str(line_bank[:-1]))
                                ALERT_MESSAGE.append(user_message)
                                print(ALERT_COUNT)
                                print(ALERT_INFO)
                                print(ALERT_MESSAGE)
        with client:
            client.loop.run_until_complete(main(phone))


    telegram_start()
    # scheduler.add_job(id='Scheduled Task', func=telegram_start, trigger="interval", seconds=30)
    # scheduler.start()
    return render_template('telegram.html')


@app.route('/telegram', methods=['GET'])
def telegram():
    return render_template('telegram.html')






# my_thread = threading.Thread(target=start_bot)
# my_thread.start()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    # app.run(debug=False)


