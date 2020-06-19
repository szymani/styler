
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from application import ma
from ..models import User, SinglePost, Comment, Message, Chat, Style


class PostSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SinglePost
        include_relationships = True
        load_instance = True


class StyleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Style
        include_relationships = True
        load_instance = True


class CommentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        include_relationships = True
        load_instance = True


class MessageSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Message
        include_relationships = True
        load_instance = True


class ChatSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Chat
        include_relationships = True
        load_instance = True
    messages = ma.Nested(MessageSchema, many=True)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
