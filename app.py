from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/face', methods=['POST'])
def facerecognition():
    return jsonify({'message': 'omar face verified'})

@app.route('/voice', methods=['POST'])
def voicerecognition():
    return jsonify({'message': 'omar voice verified'})    

if __name__ == '__main__':
    app.run()    