# 6C/19090023/Muchammad Nachirul Ichsan
# 6C/19090063/Arwinda Laurisma
# 6C/19090089/Miftakhul mubarok 
# 6C/19090051/Utari Cahyaningsih

import os, random, string

from flask import Flask
from flask import request
from flask import jsonify
from flask_httpauth import HTTPTokenAuth
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "dbtouring.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)
auth = HTTPTokenAuth(scheme='Bearer')

class Users(db.Model):
    username = db.Column(db.String(20), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(20), unique=False, nullable=False, primary_key=False)
    token = db.Column(db.String(225), unique=True, nullable=True, primary_key=False)
    db.create_all()

class Events(db.Model):
    event_creator = db.Column(db.String(20), unique=True, nullable=False, primary_key=True)
    event_name = db.Column(db.String(20), unique=False, nullable=False, primary_key=False)
    event_start_time = db.Column(db.String, unique=False, nullable=False, primary_key=False)
    event_end_time = db.Column(db.String, unique=False, nullable=False, primary_key=False)
    event_start_lat = db.Column(db.String(20), unique=False, nullable=False, primary_key=False)
    event_start_lng = db.Column(db.String(20), unique=False, nullable=False, primary_key=False)
    event_finish_lat = db.Column(db.String(20), unique=False, nullable=False, primary_key=False)
    event_finish_lng = db.Column(db.String(20), unique=False, nullable=False, primary_key=False)
    created_at = db.Column(db.String, unique=False, nullable=False, primary_key=False)
    token = db.Column(db.String(225), unique=True, nullable=True, primary_key=False)
    db.create_all()

class Logs(db.Model):
    username = db.Column(db.String(20), unique=True, nullable=False, primary_key=True)
    event_name = db.Column(db.String(20), unique=False, nullable=False, primary_key=False)
    log_lat = db.Column(db.String(20), unique=False, nullable=False, primary_key=False)
    log_lng = db.Column(db.String(20), unique=False, nullable=False, primary_key=False)
    created_at = db.Column(db.String, unique=False, nullable=False, primary_key=False)
    token = db.Column(db.String(225), unique=True, nullable=True, primary_key=False)
    db.create_all()

#curl -i http://127.0.0.1:7123/api/v1/users/create -X POST -H 'Content-Type: application/json' -d '{"username":"19090023", "password":"19090023"}'
@app.route("/api/v1/users/create", methods=["POST"])
def create():
  username = request.json['username']
  password = request.json['password']
  addUsers = Users(username=username, password=password)
  db.session.add(addUsers)
  db.session.commit() 
  return jsonify({
    'msg': 'Registrasi Sukses',
    'username': username,
    'password' : password,
    })

#curl -i http://127.0.0.1:7123/api/v1/users/login -X POST -H 'Content-Type: application/json' -d '{"username":"19090023", "password": "19090023"}'
@app.route("/api/v1/users/login", methods=["POST"])
def login():
  username = request.json['username']
  password = request.json['password']
  user = Users.query.filter_by(username=username, password=password).first()
  if user:
    token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    Users.query.filter_by(username=username, password=password).update({'token': token})
    db.session.commit()
    return jsonify({
      'msg': 'Login Sukses',
      'username': username,
      'token': token,
      })
  else:
    return jsonify({'msg': 'Login Failed'})

#curl -i -X POST http://127.0.0.1:7123/api/v1/events/create -H 'Content-Type: application/json' -d '{"token": "WXHP5HM8TE", "event_name": "touring RR", "event_start_time":2022-12-07 12:00:00, "event_end_time":2022-12-07 12:00:00, "event_start_lat": 40, "event_finish_lat": 42, "event_start_lng": 40, "event_finish_lng": 34}'
@app.route("/api/v1/events/create", methods=["POST"])
def create_event():
    token = request.json['token']
    token = Users.query.filter_by(token=token).first()
    if token:
        event_creator = request.json['event_creator']
        event_name = request.json['event_name']
        event_start_time = request.json['event_start_time']
        event_end_time = request.json['event_end_time']
        event_start_lat = request.json['event_start_lat']
        event_finish_lat = request.json['event_finish_lat']
        event_start_lng = request.json['event_start_lng']
        event_finish_lng = request.json['event_finish_lng']
        newEvents = Events(event_start_times=event_start_time, event_end_times=event_end_time, event_creators=event_creator, event_names=event_name, event_start_lat=event_start_lat, event_finish_lat=event_finish_lat, event_start_lng=event_start_lng, event_finish_lng=event_finish_lng)
        db.session.add()
        db.session.commit() 
        return newEvents, jsonify({
            'msg': 'Berhasil Tambah Event'
            })

#curl -i http://127.0.0.1:7123/api/v1/events/log -X POST -H 'Content-Type: application/json' -d '{"username":"19090023", "event_name":"touring RR", "log_lat":"40,6", "log_lng":"44,5", "created_at":"2022-11-04 08:00"}'
@app.route("/api/v1/events/log", methods=["POST"])
def log_event():
  username = request.json['username']
  event_name = request.json['event_name']
  log_lat = request.json['log_lat']
  log_lng = request.json['log_lng']
  created_at = request.json['created_at']
  token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
  addlogs = Logs(username=username, event_name=event_name, log_lat=log_lat, log_lng=log_lng, created_at=created_at, token=token)
  db.session.add(addlogs)
  db.session.commit() 
  return jsonify({
    'msg': 'Sukses Mencatat Posisi Terbaru',
    'event_name': event_name,
    'log_lat' : log_lat,
    'log_lng' : log_lng,
    })

#curl -i -X GET http://127.0.0.1:7123/api/v1/events/logs -H 'Content-Type: application/json' -d '{"username": "19090023", "event_name":"touring RR"}'
@app.route("/api/v1/events/logs", methods=["GET"])
def event_logs():
    username = request.json['username']
    event_name = request.json['event_name']
    logs_event = Logs.query.filter_by(event_name=event_name).all()
    logs_status = {}
    for log in logs_event:
        dict_logs = []
        logs_status.append(dict_logs)
    return jsonify(logs_status)

if __name__ == '__main__':
   app.run(debug = True, port=7123)
