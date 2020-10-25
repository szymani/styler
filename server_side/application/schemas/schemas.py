
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from application import ma
from ..models import User, SinglePost, Comment, Message, Chat, Style


class PostSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SinglePost
        include_relationships = True
        load_instance = True
    comments = ma.Nested("CommentSchema", many=True)
    style = ma.Nested("StyleSchema", only=['id', 'style_image'], many=False)
    author = ma.Nested("UserSchema", only=[
                       "login", "profile_photo", "id"], many=False)
    who_liked = ma.Nested("UserSchema", only=[
                          "login", "profile_photo", "id"], many=True)
    tags = ma.Nested("TagSchema", only=["id", "name"], many=True)


class StyleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Style
        include_relationships = True
        load_instance = True
    style_author = ma.Nested(
        "UserSchema", only=["login", "profile_photo", "id"], many=False)
    fav_for = ma.Nested("UserSchema", only=[
                        "login", "profile_photo", "id"], many=True)
    who_liked = ma.Nested("UserSchema", only=[
                          "login", "profile_photo", "id"], many=True)
    tags = ma.Nested("TagSchema", only=["id", "name"], many=True)


class CommentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        include_relationships = True
        load_instance = True
    comment_author = ma.Nested(
        "UserSchema", only=["login", "profile_photo", "id"], many=False)


class MessageSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Message
        include_relationships = True
        load_instance = True
    author = ma.Nested("UserSchema", only=[
                       "login", "profile_photo", "id"], many=False)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True


class ChatSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Chat
        include_relationships = True
        load_instance = True
    messages = ma.Nested("MessageSchema", many=True)
    participants = ma.Nested(
        UserSchema, only=["login", "profile_photo", "id"], many=True)


class TagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Chat
        include_relationships = True
        load_instance = True
