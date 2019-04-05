"""
Created on Oct 8, 2018

@author: Yizhe Sun
"""

import os
import base64
import shutil

import pandas as pd
import sqlalchemy as db
from flask_socketio import SocketIO

from .config import *
from .utils import remove_file, engine, metadata, frame_analysis


# analyse frame for action unit and facial expression
def predict_frame(image_base64, file_id):
    out_path = CAMERA_FOLDER + file_id + '/'
    os.mkdir(out_path)

    data = image_base64[23:]
    file_path = out_path + file_id + '.jpg'
    with open(file_path, 'wb') as f:
        f.write(base64.b64decode(data))

    openface = "/home/roy/Downloads/backend/OpenFace/FaceLandmarkImg"
    command = openface + ' -f ' + file_path + ' -aus -out_dir ' + out_path
    os.system(command)

    csv_path = out_path + file_id + '.csv'
    df = pd.read_csv(csv_path, index_col=0)
    df = df.loc[:, ' AU01_r':]

    labels = [l + ' Regression' for l in regression_units] + \
        [l + ' Classification' for l in classification_units]
    df.columns = labels

    au = [file_id]
    for _, row in df.iterrows():
        au.append(row.to_json())

    socketio = SocketIO(message_queue='redis://')
    socketio.emit('message', au)

    shutil.rmtree(out_path)


# Preprocess and analyse the video
# Then Store the results to the database
def process_video(path):
    # use OpenFace to extract frames and action unit results
    result_path = path + '-processed'
    os.mkdir(result_path)
    command = 'OpenFace/FeatureExtraction -f ' + path + ' -nomask -out_dir ' + result_path
    os.system(command)
    remove_file(path)

    path_list = str(path).split('/')
    filename = path_list[len(path_list) - 1]

    # remove unnecessary files
    avi_path = os.path.join(result_path, filename + '.avi')
    hog_path = os.path.join(result_path, filename + '.hog')
    txt_path = os.path.join(result_path, filename + '_of_details.txt')
    remove_file(avi_path)
    remove_file(hog_path)
    remove_file(txt_path)

    # prepare dataframe
    csv_path = os.path.join(result_path, filename + '.csv')
    df = pd.read_csv(csv_path, index_col=0)
    df = df[df[' success'] == 1].loc[:, ' AU01_c':]
    labels = [l + ' Classification' for l in classification_units]
    df.columns = labels

    # delete unsuccessful images
    success_images = df.index.values
    aligned_path = os.path.join(result_path, filename + '_aligned/')
    static_path = STATIC_FOLDER + filename + '/'
    os.mkdir(static_path)
    img_paths = []
    for img in os.listdir(aligned_path):
        names = img.replace('.bmp', '').split('_')
        img_no = int(names[len(names) - 1])
        if img_no in success_images:
            img_path = os.path.join(aligned_path, img)
            dest = shutil.move(img_path, static_path)
            img_paths.append(dest)

    new_csv_path = os.path.join(STATIC_FOLDER, filename + '.csv')
    df.to_csv(new_csv_path)

    # add all of the data into database
    data = [{
        'video_id': filename,
        'frame_path': frame_path,
        'csv_path': new_csv_path
    } for frame_path in img_paths]

    connection = engine.connect()
    query = db.insert(frame_analysis)
    connection.execute(query, data)
    connection.close()

    shutil.rmtree(result_path)
