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
    url = db.Column(db.String(20), nullable=False)
    site_available = db.Column(db.Boolean, default=False)
    auth_available = db.Column(db.Integer, default=False)
    mobile_available = db.Column(db.Integer, default=False)

    def __repr__(self):
        return f"<id={self.id}, title={self.title}, , url={self.url}>"


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



@app.route('/')
def index():
    services = Service.query.order_by(Service.id).all()
    test = Service.query.filter_by(id=1).all()
    print(test,"-----------")
    for i in services:
        website_status = get_status(i.url)
        Code = website_status[0]
        Status = website_status[1]
        ResponseTime = website_status[2]
        print(i.url)
        print('Код:', website_status[0], '| Статус:', website_status[1], '| Время ответа:', website_status[2])
        i.description = (str(Code) + " "+ str(Status) +" " + str(ResponseTime))
        db.session.commit()

        #Service.query.filter_by(id=3).delete()
        #db.session.commit()

    print(services)
    return render_template('index.html', services=services)


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/adding', methods=['POST','GET'])
def adding():
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        url = request.form['url']

        service = Service(title=title, description=description, url=url)
        try:
            db.session.add(service)
            db.session.commit()
            return redirect('/')
        except:
            return "Opps.. где-то затаилась ошибка"
    else:
        return render_template('add_service.html')



@app.route('/view_service/<int:id>')
def view(id):
    service = Service.query.get(id)

    br = mechanize.Browser()
    br.open(service.url)


    return render_template('view_service.html', service=service)



if __name__ == '__main__':
    app.run(debug=True)
