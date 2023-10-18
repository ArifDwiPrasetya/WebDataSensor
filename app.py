import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]

app= Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def show_diary():
    dataList = list(db.sensor.find({},{'_id':False}))
    return jsonify({'dataList' : dataList})

@app.route('/data', methods=['POST'])
def save_data():
    data_receive = request.form.get('SensorData')

    today = datetime.now()
    time = today.strftime('%Y-%m-%d-%H-%M-%S')
    doc = {
        'nilai_sensor' : data_receive,
        'time' : time
    }
    db.sensor.insert_one(doc)
    return jsonify({'message' : 'data was saved!!!'})

if __name__== '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

