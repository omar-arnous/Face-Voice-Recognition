from flask import Flask, jsonify, request
from face_recognition_system import FaceRecognition
from SpeakerIdentification import VoiceRecognition
from pydub import AudioSegment
import sys
sys.path.append('/path/to/ffmpeg')

app = Flask(__name__)

@app.route('/face', methods=['POST'])
def facerecognition():
    picture_1 = request.files['picture_1']
    picture_2 = request.files['picture_2']
    face_recognition = FaceRecognition(picture_1, picture_2)
    result = face_recognition.run() 
    if result:
        return jsonify({'result': 1})
    else:
        return jsonify({'result': 0})

@app.route('/register', methods=['POST'])
def trainmodel():
    audio = request.files['audio']
    name = request.form['name']
    # AudioSegment.from_file(audio).export(audio, format="wav")
    # voice_recognition = VoiceRecognition(audio, name)

@app.route('/voice', methods=['POST'])
def voicerecognition():
    return jsonify({'message': 'omar voice verified'})    

if __name__ == '__main__':
    app.run()    