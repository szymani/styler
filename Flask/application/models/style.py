from application import db, ma
from datetime import datetime as dt
from . import user
from . import single_post


class Style(db.Model):
    __tablename__ = 'style'
    id = db.Column(db.Integer, primary_key=True)
    style_author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  #  style_author = db.relationship("User", backref="author_of_styles")
    description = db.Column(db.String(250), nullable=True)
    style_image = db.Column(db.LargeBinary)
    upvotes = db.Column(db.Integer, nullable=True)
    downvotes = db.Column(db.Integer, nullable=True)
    creation_date = db.Column(db.DateTime)
    ifprivate = db.Column(db.Boolean)
    # used_in = db.relationship("Single_post", backref="style")
   # fav_for = db.relationship("User", secondary=user_style_association, backref="fav_styles")

    def __init__(self, author_id, style_image, description='Default description', localization="", ifprivate=True):
    #    self.style_author = user.User.query.get(author_id)
        self.style_author_id = author_id
        self.description = description
        self.style_image = style_image
        self.result_image = None
        self.upvotes = 0
        self.downvotes = 0
        self.creation_date = dt.now()
        self.localization = localization
        self.ifprivate = ifprivate
        self.status = 0

