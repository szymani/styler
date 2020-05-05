from application import db, ma
from datetime import datetime as dt
from application.models.user import User
from application.models.style import Style


class SinglePost(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  #  author = db.relationship("User", backref="history")
    description = db.Column(db.String(250), nullable=True)
    content_image = db.Column(db.LargeBinary)
    result_image = db.Column(db.LargeBinary)
    upvotes = db.Column(db.Integer, nullable=True)
    downvotes = db.Column(db.Integer, nullable=True)
    creation_date = db.Column(db.DateTime)
    localization = db.Column(db.String(100), nullable=True)
    ifprivate = db.Column(db.Boolean)
    style_id = db.Column(db.Integer, db.ForeignKey('style.id'))
    # style = db.relationship("Style", backref="used_in")
    status = db.Column(db.Integer)

    def __init__(self, content_image, style_id, author_id, description='Default description', style_image=None, localization="", ifprivate=True):
        self.author = User.query.get(author_id)
        self.author_id = author_id
        self.description = description
        self.content_image = content_image
        # self.style_id = style_id
        # self.style = Style.query.get(style_id)
        self.result_image = None
        self.upvotes = 0
        self.downvotes = 0
        self.creation_date = dt.now()
        self.localization = localization
        self.ifprivate = ifprivate
        self.status = 0

