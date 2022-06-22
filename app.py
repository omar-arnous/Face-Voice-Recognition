from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/face')
def facerecognition():
    return jsonify({'message': 'omar face verified'})

@app.route('/voice')
def voicerecognition():
    return jsonify({'message': 'omar voice verified'})    

app.run()    