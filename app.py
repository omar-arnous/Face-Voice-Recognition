from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the AI System'})

@app.route('/face')
def facerecognition():
    return jsonify({'message': 'omar face verified'})

@app.route('/voice')
def voicerecognition():
    return jsonify({'message': 'omar voice verified'})    

app.run()    