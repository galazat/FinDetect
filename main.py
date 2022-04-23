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
    short_description = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(20), nullable=False)

    site_available = db.Column(db.Boolean, default=False)
    available_desc = db.Column(db.Text, default=False)

    auth_available = db.Column(db.Boolean, default=False)
    mobile_available = db.Column(db.Boolean, default=False)
    nmap_decr = db.Column(db.Text, default=False)
    zabbix_decr = db.Column(db.Text, default=False)

    social_decr = db.Column(db.Text, default=False)
    tech_decr = db.Column(db.Text, default=False)

    def __repr__(self):
        return f"<id={self.id}, title={self.title}, , url={self.url}>"


def get_status():
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
            print(i.site_available)
            db.session.commit()
        else:
            i.site_available = 1
            print(i.site_available)
            db.session.commit()

        #test = Service.query.filter_by(id=1).all()
        # Service.query.filter_by(id=3).delete()
        # db.session.commit()

def get_domain_info(url=''):
    if (url==''):
        services = Service.query.order_by(Service.id).all()
        for i in services:
            try:
                url = (re.search('[A-Za-z0-9]{2,20}\.[com|ru|org|us|en|fr|]{2,4}', i.url)).group(0)
                print('URL : ',url)
                nslookup = subprocess.run(["nslookup", url], stdout=PIPE, stderr=PIPE)
                i.nmap_decr = (re.search('[A-Za-z0-9]{2,20}\.[com|ru|org|us|en|fr|]{2,4}', (nslookup.stdout).decode("utf-8"))).group(0)
                print('nslookup domain : ',i.nmap_decr)
                tmp = (re.findall(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", (nslookup.stdout).decode("utf-8") ))
                i.zabbix_decr = tmp[2]
                print('nslookup address : ',i.zabbix_decr)
            except:
                i.nmap_decr = "Opps... There are problem on server ! We are work on it "
                print('oops...')
            try:
                whois = subprocess.run(["whois", url], stdout=PIPE, stderr=PIPE)
                print('whois : ',whois)
                i.tech_decr = (whois.stdout).decode('utf-8')
                print(i.tech_decr)
            except:
                i.tech_decr = "Opps... There are problem on server ! We are work on it "
            db.session.commit()
    else:
        url = (re.search('[A-Za-z0-9]{2,20}\.[com|ru|org|us|en|fr|]{2,4}', url)).group(0)
        try:
            print(url)
            nslookup = subprocess.run(["nslookup", url], stdout=PIPE, stderr=PIPE)
            i.nmap_decr = (re.search('[A-Za-z0-9]{2,20}\.[com|ru|org|us|en|fr|]{2,4}', (nslookup.stdout).decode("utf-8"))).group(0)
            tmp = (re.findall(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", (nslookup.stdout).decode("utf-8") ))
            i.zabbix_decr = tmp[2]
        except:
            i.nmap_decr = "Opps... There are problem on server ! We are work on it "
        try:
            whois = subprocess.run(["whois", url], stdout=PIPE, stderr=PIPE)
            i.tech_decr = (whois.stdout).decode('utf-8')
        except:
            i.tech_decr = "Opps... There are problem on server ! We are work on it "
        db.session.commit()



scheduler = BackgroundScheduler()
scheduler.add_job(func=get_status, trigger="interval", seconds=900)
scheduler.add_job(func=get_domain_info, trigger="interval", seconds=900)
scheduler.start()




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

        service = Service(title=title, short_description=short_description, description=description, url=url)
        try:
            db.session.add(service)
            db.session.commit()
            get_status()
            get_domain_info(url)
            return redirect('/')
        except:
            return "Opps.. где-то затаилась ошибка"
    else:
        return render_template('add_service.html')



@app.route('/view_service/<int:id>')
def view(id):
    service = Service.query.get(id)
    return render_template('view_service.html', service=service)


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

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    # app.run(debug=False)
