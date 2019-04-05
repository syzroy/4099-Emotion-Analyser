from flask import request, jsonify, make_response, send_from_directory
from flask import json
from flask_socketio import SocketIO
import sqlalchemy as db
import pandas as pd

from . import blueprint
from .config import *
from .utils import save_file, allowed_file, q
from .utils import engine, metadata, frame_analysis
from .utils import video as v
from .responses import Success, Error
from .tasks import process_video

# initialise socketio for web socket communication
socketio = SocketIO(message_queue='redis://')


# The controller which handles the video upload
@blueprint.route('/upload', methods=['POST'])
def upload_video():
    # Does the checking for the uploaded file
    if 'file' not in request.files:
        return jsonify(
            Error(ERROR_NO_UPLOADED_FILE, 'No uploaded file').__dict__)
    video = request.files['file']
    if not video or video.filename == '':
        return jsonify(
            Error(ERROR_NO_UPLOADED_FILE, 'No uploaded file').__dict__)
    if not allowed_file(video.filename):
        return jsonify(
            Error(VIDEO_TYPE_NOT_SUPPORTED,
                  'File type not supported').__dict__)

    # Save the video and start the background task to process it
    video_path, video_id = save_file(video, VIDEO_FOLDER)
    job = q.enqueue(process_video, video_path, job_id=video_id)

    # insert the video id into database
    connection = engine.connect()
    query = db.insert(v).values(video_id=video_id)
    connection.execute(query)
    connection.close()

    # Return the job id to the user for future analysis
    response = make_response(jsonify(Success(video_id).__dict__))
    response.mimetype = 'application/json'
    return response


# get the list of uploaded videos, with their current status
@blueprint.route('/list', methods=['GET'])
def get_list():
    connection = engine.connect()
    query = db.select([v])
    result_proxy = connection.execute(query)
    results = result_proxy.fetchall()

    result_list = []
    for result in results:
        status_query = db.select([
            frame_analysis
        ]).where(frame_analysis.columns.video_id == result[0])
        proxy = connection.execute(status_query)
        r = proxy.fetchall()
        if len(r) == 0:
            result_list.append((result[0], 0))
        else:
            result_list.append((result[0], 1))
    connection.close()
    return jsonify([e for e in result_list])


# get the frame and analysis data
@blueprint.route('/data', methods=['GET'])
def get_data():
    video_id = request.args.get('id')
    if not video_id:
        return jsonify(Error(NO_VIDEO_ID, 'No given video id').__dict__)
    connection = engine.connect()
    query = db.select(
        [frame_analysis]).where(frame_analysis.columns.video_id == video_id)
    result_proxy = connection.execute(query)
    results = result_proxy.fetchall()
    connection.close()

    if len(results) == 0:
        return jsonify(
            Error(INVALID_VIDEO_ID,
                  'No records under given video id').__dict__)

    return jsonify([result[2] for result in results])


# read csv file content
@blueprint.route('/static/<name>', methods=['GET'])
def read_file(name):
    path = '/home/roy/Downloads/backend/static/' + name
    df = pd.read_csv(path, index_col=0)
    au = []
    for _, row in df.iterrows():
        au.append(row.to_json())
    return jsonify(au)


# serve images
@blueprint.route('/static/<file_id>/<name>', methods=['GET'])
def serve_static(file_id, name):
    return send_from_directory(
        '/home/roy/Downloads/backend/static/' + file_id + '/', name)


# receive camera screenshots from websocket
@socketio.on('message')
def handle_message(image_base64, file_id):
    q.enqueue(predict_frame, image_base64, file_id)
