from application import db
from sqlalchemy.dialects.mysql import INTEGER, TINYINT

class Pictures(db.Model):
    """Represents an entry for the Pictures table
    """
    __tablename__ = 'Pictures'

    pic_id = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    site = db.Column(TINYINT(display_width=2, unsigned=True), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    url = db.Column(db.String(200), nullable=False)
    tags = db.relationship('Tags', backref='picture', lazy=True)

    def __init__(self, site, date, url):
        self.site = site
        self.date = date
        self.url = url

    def __repr__(self):
        return '<Picture(%r, %r, %r)>' % self.site, self.date, self.url

class Tags(db.Model):
    """Represents an entry for the Tags table
    """
    __tablename__ = 'Tags'

    pic_id = db.Column(INTEGER(unsigned=True), db.ForeignKey('Pictures.pic_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    tag = db.Column(db.String(length=20), primary_key=True)

    def __init__(self, pic_id, tag):
        self.pic_id = pic_id
        self.tag = tag

    def __repr__(self):
        return '<Tag(%r, %r)>' % self.id, self.tag
