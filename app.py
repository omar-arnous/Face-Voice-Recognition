from flask import Flask, jsonify, request
import werkzeug
from face_recognition_system import FaceRecognition
from SpeakerIdentification import VoiceRecognition
from PIL import Image
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/face', methods=['POST'])
def facerecognition():
    jsonify({"message": "face recognition started"})
    response = request.get_data()
    picture_1 = request.files['picture_1']
    picture_2 = request.files['picture_2']
    name = response['name']
    # print(picture_1)
    # print(picture_2)
    pic_1 = werkzeug.utils.secure_filename(picture_1.filename)
    pic_2 = werkzeug.utils.secure_filename(picture_2.filename)
    picture_1.save("static/img/" + pic_1)
    picture_1.save("static/img/" + pic_2)
    result = FaceRecognition(picture_1, picture_1) 
    name = 'omar'
    if result:
        return jsonify({'result': 1})
    else:
        return jsonify({'result': 0})

@app.route('/voice', methods=['POST'])
def voicerecognition():
    return jsonify({'message': 'omar voice verified'})    

if __name__ == '__main__':
    app.run()    