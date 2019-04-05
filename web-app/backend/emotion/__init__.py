"""
Created on Sep 22, 2018

@author: Yizhe Sun
"""

import os

from flask import Flask
from flask_cors import CORS
from flask_cdn import CDN

from .main.config import *
from .main.controllers import socketio


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['VIDEO_FOLDER'] = VIDEO_FOLDER
    app.config['MODEL_PATH'] = MODEL_PATH
    app.config['CDN_DOMAIN'] = 'cdn.yourdomain.com'
    # cnn_model, lstm_model = load_model(app.config['MODEL_PATH'])

    from .main.controllers import blueprint
    app.register_blueprint(blueprint)
    socketio.init_app(app)

    return app