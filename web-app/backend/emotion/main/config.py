"""
Created on Sep 22, 2018

@author: Yizhe Sun
"""

# Where to put the uploaded and generated files
VIDEO_FOLDER = 'video-uploads/'
# Where to load the trained LSTM model
MODEL_PATH = '/mnt/c/Users/Yizhe Sun/Desktop/4099-Emotion-Analyser/web-app/backend/LSTM.h5'
# Where to put the analysis results for web camera
CAMERA_FOLDER = 'camera-analysis/'
# The URI for the database
DATABASE_URI = 'mysql+pymysql://fNBHVuOcxM:Bm880AOIL3@remotemysql.com/fNBHVuOcxM'
# Where to put the static files
STATIC_FOLDER = 'static/'

# Video formats accepted
ALLOWED_EXTENSIONS = {'mp4', 'mov'}

# HTTP response status codes
OK = 200
ERROR_NO_UPLOADED_FILE = 4001
VIDEO_TYPE_NOT_SUPPORTED = 4002
NO_VIDEO_ID = 4003
INVALID_VIDEO_ID = 4004

regression_units = [
    'Inner brow raiser', 'Outer brow raiser', 'Brow lower', 'Upper lid raiser',
    'Cheek raiser', 'Lid tightener', 'Nose wrinkler', 'Upper lip raiser',
    'Lip corner puller', 'Dimpler', 'Lip corner depressor', 'Chin raiser',
    'Lip stretcher', 'Lip tightener', 'Lips part', 'Jaw drop', 'Blink'
]

classification_units = [
    'Inner brow raiser', 'Outer brow raiser', 'Brow lower', 'Upper lid raiser',
    'Cheek raiser', 'Lid tightener', 'Nose wrinkler', 'Upper lip raiser',
    'Lip corner puller', 'Dimpler', 'Lip corner depressor', 'Chin raiser',
    'Lip stretcher', 'Lip tightener', 'Lips part', 'Jaw drop', 'Lip suck',
    'Blink'
]
