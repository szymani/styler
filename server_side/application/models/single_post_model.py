from application import db, ma
from datetime import datetime as dt
from ..models import user_model, comment_model

who_liked_table = db.Table('who_liked', db.Model.metadata,
                           db.Column('post_id', db.Integer,
                                     db.ForeignKey('post.id')),
                           db.Column('user_id', db.Integer,
                                     db.ForeignKey('user.id'))
                           )


class SinglePost(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String(250), nullable=True)
    content_image = db.Column(db.LargeBinary)
    upvotes = db.Column(db.Integer, nullable=True)
    comments = db.relationship("Comment", backref="post")
    who_liked = db.relationship("User",
                                secondary=who_liked_table,
                                lazy='dynamic',
                                backref=db.backref('liked_posts', lazy='dynamic'))

    result_image = db.Column(db.LargeBinary)
    creation_date = db.Column(db.DateTime)
    localization = db.Column(db.String(100), nullable=True)
    ifprivate = db.Column(db.Boolean)
    style_id = db.Column(db.Integer, db.ForeignKey('style.id'))
    status = db.Column(db.Integer)

    def __init__(self,
                 content_image,
                 author_id,
                 style_id,
                 description='Default description'):
        # self.author = user_model.User.query.get(author_id)
        self.author_id = author_id
        self.description = description
        if (content_image is not None):
            self.content_image = content_image.encode('ascii')
        else:
            self.content_image = content_image
        # self.content_image = content_image
        self.upvotes = 0
        self.creation_date = dt.now()
        self.style_id = style_id
        # self.style = Style.query.get(style_id)
        self.result_image = None
        self.localization = localization
        self.ifprivate = ifprivate
        self.status = 0

    def as_dict(self):
        return {
            c.name: str(getattr(self, c.name))
            for c in self.__table__.columns
        }
