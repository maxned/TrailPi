import sys
sys.path.append('..')

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import INTEGER, TINYINT, DATETIME
from utils import get_local_date
import jwt
import datetime

SECRET_KEY = 't_pi!sctkey%20190203#'

db = SQLAlchemy() # will be initialized in application.py

class Pictures(db.Model):
  """Represents an entry for the Pictures table
  """
  __tablename__ = 'Pictures'

  pic_id = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
  site = db.Column(TINYINT(display_width=2, unsigned=True), nullable=False)
  date = db.Column(DATETIME, default=get_local_date(), nullable=False)
  url = db.Column(db.String(200), nullable=False)
  tags = db.relationship('Tags', backref='picture', lazy=True)

  def __init__(self, site, date, url):
    self.site = site
    self.date = date
    self.url = url

  def __repr__(self):
    return '<Picture(%r, %r, %r)>' % (self.site, self.date, self.url)

class Tags(db.Model):
  """Represents an entry for the Tags table
  """
  __tablename__ = 'Tags'

  tag_id = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
  pic_id = db.Column(INTEGER(unsigned=True), db.ForeignKey('Pictures.pic_id', ondelete='CASCADE', onupdate='CASCADE'))
  tag = db.Column(db.String(length=20), nullable=False)

  def __init__(self, pic_id, tag):
    self.pic_id = pic_id
    self.tag = tag

  def __repr__(self):
    return '<Tag(%r, %r)>' % (self.id, self.tag)

class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    permissions = db.Column(db.Integer, nullable=False, default=1)

    def __init__(self, username, password, bcrypt, permissions=1):
        self.username = username
        self.password = bcrypt.generate_password_hash(
            password, rounds=12
        ).decode()
        print(self.password)
        self.registered_on = datetime.datetime.now()
        self.permissions = permissions

    def encode_auth_token(self, user_id):
        """Generates the Auth Token"""

        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=25),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """Validates the auth token"""

        try:
            payload = jwt.decode(auth_token, SECRET_KEY)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class BlacklistToken(db.Model):
    """Token Model for storing JWT tokens"""
    __tablename__ = 'BlacklistTokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False