import sys
import os

import flask
import flask_sqlalchemy

# Allows importing the config.py file even if ran from other directories
_here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(_here))

app = flask.Flask(__name__)

app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = flask_sqlalchemy.SQLAlchemy(app)

from twitter_kafka_crawler import app_routes
