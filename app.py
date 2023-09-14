import argparse
from flask import Flask, request, jsonify
import gunicorn
import subprocess
from pathlib import Path
import sys
from demucs.separate import main as separate

app = Flask(__name__)

"""stores file temporarily in /data/input to be processed by demucs"""
def store_temp_track(data, name):
    track = data.get('track')
    track.save('/data/input/{name}'.format(name=name))
    return '/data/input/{name}'.format(name=name)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to the demucs splittify api v-0.0.1'})

@app.route('/seperate', methods=['POST'])
def separate():
    model = 'htdemucs'
    processor = '-d cpu'
    data = request.get_json()
    track = data.get('track')
    name = data.get('trackname')
    output = "--out /data/output"
    input_path = store_temp_track(track, name)
    mp3 = "--mp3"
    #todo to expiriment with this to activate karaoke mode
    twostems = "--two-stems "
    
    try:
        separate(['python3', '-m', 'demucs', '-n', "mdx_extra",  model, mp3, processor, output, input_path])
        #todo to delete file in data/input after processing
    except Exception as e:
        return jsonify({'error': str(e)}), 400
