from os import name
from flask import request

from application import db
from ..models import Chat, Message
from flask_login import current_user
from ..services import helper_func


def get_chat(id):
    return Chat.query.get(id)


def is_user_in_chat(id, chat):
    for user in chat.participants:
        if user.id is id:
            return True
    return False


def send_pm(chat, data):
    new_message = Message(
        author_id=current_user.id, message_text=data["message_text"], content_image=data["content_image"])
    chat.messages.append(new_message)
    db.session.commit()
    return new_message


def create_chat(data):
    chat = Chat(name=data["chat_name"], participants=data["participants"])
    db.session.commit()
    return chat


def update_chat(id, data):
    chat = get_chat(id)
    Chat.query.filter(Chat.id == id).update(
        {'name': data["name"] or chat.name})
    db.session.commit()
    return chat
