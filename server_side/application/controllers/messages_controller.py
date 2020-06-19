from flask import request, send_file, Blueprint, jsonify, make_response, abort
from flask import current_app as app
from flask_login import login_required, logout_user, current_user

from application import db, ma
from ..models import User, Chat, Message
from ..services import helper_func
from ..schemas import schemas

message = Blueprint('message', __name__)
message_schema = schemas.MessageSchema()
messages_schema = schemas.MessageSchema(many=True)

chat_schema = schemas.ChatSchema()
chats_schema = schemas.ChatSchema(many=True)
# TODO Make service for messages


@login_required
@message.route('/chats/', methods=['GET'])
def get_chats_list():
    limit, page_num = helper_func.set_limit_and_page(request)
    if current_user.is_authenticated:
        chats = current_user.chats
        return jsonify(chats_schema.dump(chats)), 200
    abort(401)


@login_required
@message.route('/chats/<int:id>', methods=['GET'])
def get_chat(id):
    limit, page_num = helper_func.set_limit_and_page(request)
    if current_user.is_authenticated:
        chat = Chat.query.get(id)
        if (id is not None) and (chat is not None):
            for user in chat.participants:
                if user.id is current_user.id:
                    return jsonify(chat_schema.dump(chat)), 200
            abort(401)
        abort(400)
    abort(401)


@login_required
@message.route('/chats/<int:id>/send', methods=['POST'])
def send_pm(id):
    if current_user.is_authenticated:
        data = request.get_json()
        if id is not None and data is not None:
            conv = Chat.query.get(id)
            if conv is not None:
                for user in conv.participants:
                    if user.id is current_user.id:
                        if conv is not None:
                            new_message = Message(
                                author_id=current_user.id, message_text=data["message_text"], content_image=data["content_image"])
                            conv.messages.append(new_message)
                            db.session.commit()
                            return jsonify(message_schema.dump(new_message)), 200
                abort(401)
            abort(404, "Wrong id")
        abort(400)
    abort(401)


@login_required
@message.route('/chats/new', methods=['POST'])
def new_chat():
    if current_user.is_authenticated:
        data = request.get_json()
        if data is not None:
            print(data)
            try:
                conv = Chat(name=data["chat_name"],
                            participants=data["participants"])
            except Exception as e:
                abort(404, "Some users could not be added to chat")
            db.session.commit()
            return jsonify(chat_schema.dump(conv)), 200
        abort(400)
    abort(401)
