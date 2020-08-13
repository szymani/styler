from application import db, ma
from datetime import datetime as dt


class Style(db.Model):
    __tablename__ = 'style'
    id = db.Column(db.Integer, primary_key=True)
    style_author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String(250), nullable=True)
    style_image = db.Column(db.LargeBinary)
    upvotes = db.Column(db.Integer, nullable=True)
    downvotes = db.Column(db.Integer, nullable=True)
    creation_date = db.Column(db.DateTime)
    isprivate = db.Column(db.Boolean)

    def __init__(self, author_id, style_image, description='Default description', localization="", isprivate=True):
        self.style_author_id = author_id
        self.description = description
        if (content_image is not None):
            self.style_image = style_image.encode('ascii')
        else:
            self.style_image = style_image
        self.result_image = None
        self.upvotes = 0
        self.downvotes = 0
        self.creation_date = dt.now()
        self.isprivate = isprivate
