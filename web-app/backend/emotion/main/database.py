"""
Created on Nov 14, 2018

@author: Yizhe Sun
"""

import sqlalchemy as db

from config import *

# connect to database
engine = db.create_engine(DATABASE_URI)
metadata = db.MetaData()
connection = engine.connect()

# table descriptions
video = db.Table('video', metadata,
                 db.Column('video_id', db.String(255), primary_key=True))

frame_analysis = db.Table(
    'frame_analysis', metadata, db.Column(
        'id', db.Integer(), primary_key=True),
    db.Column(
        'video_id',
        db.String(255),
        db.ForeignKey('video.video_id'),
        nullable=False), db.Column('frame_path', db.Text(), nullable=False),
    db.Column('csv_path', db.Text(), nullable=False))

# create tables
# metadata.create_all(engine)

# delete tables
metadata.drop_all(engine)

connection.close()
engine.dispose()
