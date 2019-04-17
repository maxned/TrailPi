"""Contains db initialization and provides the models for the db
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:ECS193dev!@trailpi-db-instance.ckdc802eljqg.us-west-1.rds.amazonaws.com:3306/ReserveWebcamImages'
application.config['SQLALCHEMY_POOL_RECYCLE'] = 3600

db = SQLAlchemy(application)
