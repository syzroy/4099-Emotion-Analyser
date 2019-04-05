"""
Created on Dec 13, 2018

@author: Yizhe Sun
"""

import os
import eventlet

from emotion import create_app, socketio, VIDEO_FOLDER, CAMERA_FOLDER, STATIC_FOLDER
from emotion.main.tasks import predict_frame
from emotion.main.utils import q

if not os.path.isdir(VIDEO_FOLDER):
    os.mkdir(VIDEO_FOLDER)

if not os.path.isdir(CAMERA_FOLDER):
    os.mkdir(CAMERA_FOLDER)

if not os.path.isdir(STATIC_FOLDER):
    os.mkdir(STATIC_FOLDER)

app = create_app()
eventlet.monkey_patch()

if __name__ == '__main__':
    socketio.run(app)
