import json
import time
from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
#Módulos propios
from ToneDetector import *



app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def index():
    return 'Server Works!'
  
@app.route('/set_audio_file')
@cross_origin()
def setAudioFile():
    audio_file = request.args.get('audio_file')
    data = analyzeAudioFile(audio_file)
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response
