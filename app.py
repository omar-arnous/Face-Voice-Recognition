from flask import Flask, jsonify, request
from face_recognition_system import FaceRecognition
from SpeakerIdentification import VoiceRecognition


app = Flask(__name__)

@app.route('/face', methods=['POST'])
def facerecognition():
    request_data = request.get_json()
    name = request_data['name']
    picture_1 = request_data['picture_1']
    picture_2 = request_data['picture_2']
    result = FaceRecognition(picture_1, picture_2)
    if result:
        return jsonify({'message': f'{name} face recognized'})
    else:
        return jsonify({'message': f'{name} face  Not recognized'})

@app.route('/voice', methods=['POST'])
def voicerecognition():
    return jsonify({'message': 'omar voice verified'})    

if __name__ == '__main__':
    app.run()    