from application import db, ma
from datetime import datetime as dt
from datetime import timedelta
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app
import jwt


FollowerRelationship = db.Table(
    'FollowerRelationship', db.Model.metadata,
    db.Column('FollowerID', db.Integer, db.ForeignKey('user.id')),
    db.Column('FollowedID', db.Integer, db.ForeignKey('user.id')))


user_style_table = db.Table('user_style', db.Model.metadata,
                            db.Column('user_id', db.Integer,
                                      db.ForeignKey('user.id')),
                            db.Column('style_id', db.Integer, db.ForeignKey('style.id')))


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    description = db.Column(db.String(250), nullable=True)
    profile_photo = db.Column(db.LargeBinary)
    creation_date = db.Column(db.DateTime)
    user_type = db.Column(db.Integer)
    posts = db.relationship("SinglePost", backref="author")
    comments = db.relationship("Comment", backref="comment_author")
    followers = db.relation(
        'User',
        secondary=FollowerRelationship,
        primaryjoin=FollowerRelationship.c.FollowedID == id,
        secondaryjoin=FollowerRelationship.c.FollowerID == id,
        lazy='dynamic',
        backref=db.backref('followed', lazy='dynamic'))
    messages = db.relationship("Message", backref="author")
    total_upvotes = db.Column(db.Integer, nullable=True)
    fav_styles = db.relationship("Style",
                                 secondary=user_style_table,
                                 lazy='dynamic',
                                 backref=db.backref('fav_for', lazy='dynamic'))
    author_of_styles = db.relationship(
        "Style", lazy='dynamic', backref="style_author")

    def __init__(self,
                 login,
                 password,
                 email,
                 description='Default description',
                 profile_photo=None,
                 user_type=0):
        self.login = login
        self.email = email
        self.description = description
        if (profile_photo is not None):
            self.profile_photo = profile_photo.encode('ascii')
        else:
            self.profile_photo = profile_photo
        self.creation_date = dt.now()
        self.user_type = user_type
        self.password = generate_password_hash(password, method='sha256')
        self.total_upvotes = 0

    def as_dict(self):
        return {
            c.name: str(getattr(self, c.name))
            for c in self.__table__.columns if c.name != "password"
        }

    def update(self,
               login,
               password,
               email,
               description='Default description',
               profile_photo=None,
               user_type=0):
        self.login = login
        self.email = email
        self.description = description
        self.profile_photo = profile_photo
        self.user_type = user_type
        self.password = generate_password_hash(password, method='sha256')

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def encode_token(self):
        try:
            payload = {
                #! dates commented only for development
                # 'exp': dt.now() + timedelta(minutes=30),
                # 'iat': dt.now(),
                'login': self.login,
            }
            return jwt.encode(payload,
                              app.config.get('SECRET_KEY'),
                              algorithm='HS256').decode('utf-8')
        except Exception as e:
            return e

    def __repr__(self):
        return '<User {}>'.format(self.login)
