from application import db, ma
from datetime import datetime as dt
from . import user_model
from . import single_post_model


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    comment_author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    description = db.Column(db.String(250), nullable=True)
    upvotes = db.Column(db.Integer, nullable=True)
    creation_date = db.Column(db.DateTime)

    def __init__(self, author_id, post_id, description='Default description'):
        self.comment_author_id = author_id
        self.post_id = post_id
        self.description = description
        self.upvotes = 0
        self.creation_date = dt.now()

    def as_dict(self):
        return {
            c.name: str(getattr(self, c.name))
            for c in self.__table__.columns
        }
