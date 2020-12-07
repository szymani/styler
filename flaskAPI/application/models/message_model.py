from application import db, ma
from datetime import datetime as dt


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
    message_text = db.Column(db.String(250), nullable=True)
    creation_date = db.Column(db.DateTime)
    content_image = db.Column(db.LargeBinary)

    def __init__(self, author_id, message_text, content_image):
        self.author_id = author_id
        self.message_text = message_text
        self.creation_date = dt.now()
        if (content_image is not None):
            self.content_image = content_image.encode('ascii')
        else:
            self.content_image = content_image

    def as_dict(self):
        return {
            c.name: str(getattr(self, c.name))
            for c in self.__table__.columns
        }
