from application import db, ma
from datetime import datetime as dt
from . import single_post
from . import style

user_style_association = db.Table('user_style',
                                  db.Column('user.id', db.Integer, db.ForeignKey('user.id')),
                                  db.Column('style.id', db.Integer, db.ForeignKey('style.id')))

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=True)
    profile_photo = db.Column(db.LargeBinary)
    #total_upvotes = db.Column(db.Integer, nullable=True)
    creation_date = db.Column(db.DateTime)
    user_type = db.Column(db.Integer)
    fav_styles = db.relationship("Style", secondary=user_style_association, backref="fav_for")
    author_of_styles = db.relationship("Style", backref="style_author")
    history = db.relationship("SinglePost", backref="author")

    def __init__(self, login, password, description='Default description', profile_photo=None, user_type=0):
        self.login = login
        self.password = password
        self.description = description
        self.profile_photo = profile_photo
        self.creation_date = dt.now()
        self.user_type = user_type

