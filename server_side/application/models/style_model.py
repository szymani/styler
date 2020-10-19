from application import db
from datetime import datetime as dt

who_liked_style = db.Table('who_liked_style', db.Model.metadata,
                           db.Column('style_id', db.Integer,
                                     db.ForeignKey('style.id')),
                           db.Column('user_id', db.Integer,
                                     db.ForeignKey('user.id'))
                           )


class Style(db.Model):
    __tablename__ = 'style'
    id = db.Column(db.Integer, primary_key=True)
    style_author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String(250), nullable=True)
    style_image = db.Column(db.LargeBinary)
    posts = db.relationship("SinglePost", backref="style")
    upvotes = db.Column(db.Integer, nullable=True)
    downvotes = db.Column(db.Integer, nullable=True)
    creation_date = db.Column(db.DateTime)
    isprivate = db.Column(db.Boolean)
    who_liked = db.relationship("User",
                                secondary=who_liked_style,
                                lazy='dynamic',
                                backref=db.backref('liked_styles', lazy='dynamic'))

    def __init__(self, author_id, style_image, description='Default description', localization="", isprivate=True):
        self.style_author_id = author_id
        self.description = description
        if (style_image is not None):
            self.style_image = style_image.encode('ascii')
        else:
            self.style_image = style_image
        self.result_image = None
        self.upvotes = 0
        self.downvotes = 0
        self.creation_date = dt.now()
        self.isprivate = isprivate

    def update(self, description, style_image, isprivate):
        self.description = description
        self.style_image = style_image
        self.isprivate = isprivate
