from application import db, ma
from datetime import datetime as dt
from ..models import user_model, comment_model, message_model

chats_users = db.Table('chats_users', db.Model.metadata,
    db.Column('chat_id', db.Integer, db.ForeignKey('chat.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    messages = db.relationship("Message", backref="chat")
    participants = db.relationship("User",
                    secondary=chats_users,
                    lazy='dynamic',
                    backref=db.backref('chats', lazy='dynamic'))
    creation_date = db.Column(db.DateTime)

    def __init__(self,name="Default name", participants=None):
        self.creation_date = dt.now()
        self.name = name
        if (participants is not None):
            for participant in participants:
                user = user_model.User.query.get(participant)
                if user is not None:
                    self.participants.append(user)
        else:
            self.participants = None


    def as_dict(self):
        return {
            c.name: str(getattr(self, c.name))
            for c in self.__table__.columns
        }
