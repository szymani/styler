from flask import request, send_file, Blueprint, jsonify, make_response, abort
from flask import current_app as app
from flask_login import login_required, logout_user, current_user

from application import db, ma
from ..models import User, Chat, Message
from ..services import helper_func, message_service, user_service
from ..schemas import schemas

message = Blueprint('message', __name__)
message_schema = schemas.MessageSchema()
messages_schema = schemas.MessageSchema(many=True)

chat_schema = schemas.ChatSchema()
chats_schema = schemas.ChatSchema(many=True)


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
        chat = message_service.get_chat(id)
        if chat is not None:
            if message_service.is_user_in_chat(current_user.id, chat):
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
            chat = message_service.get_chat(id)
            if chat is not None:
                if message_service.is_user_in_chat(current_user.id, chat):
                    return jsonify(message_schema.dump(message_service.send_pm(chat, data))), 200
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
            if user_service.if_users_exist(data["participants"]):
                abort(404, "Some users could not be added to chat")
            return jsonify(chat_schema.dump(message_service.create_chat(data))), 200
        abort(400)
    abort(401)
