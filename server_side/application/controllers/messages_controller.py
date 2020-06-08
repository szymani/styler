from flask import request, send_file, Blueprint, jsonify, make_response
from flask import current_app as app
from flask_login import login_required, logout_user, current_user

from application import db, ma
from ..models import user_model, chat_model, message_model
from ..services import helper_func

message = Blueprint('message', __name__)


@login_required
@message.route('/chats/', methods=['GET'])
def get_chats_list():
    limit, page_num = helper_func.set_limit_and_page(request)
    if current_user.is_authenticated:
        try:
            chats = current_user.chats
        except:
            return str([]), 200
        if len(chats.all()) is not 0:
            result = []
            for chat in chats.all():
                part = []
                for participant in chat.participants:
                    part.append(participant.id)
                    print(participant.id)
                result.append({
                    'chat_id': chat.id,
                    'chat_name': chat.name,
                    'participants': part
                })
            return jsonify(result), 200
        else:
            abort(404)
    abort(401)


@login_required
@message.route('/chats/<int:id>', methods=['GET'])
def get_chat(id):
    limit, page_num = helper_func.set_limit_and_page(request)
    if current_user.is_authenticated:
        chat = chat_model.Chat.query.get(id)
        if (id is not None) and (chat is not None):
            for user in chat.participants:
                if user.id is current_user.id:
                    try:
                        messages = chat.messages
                    except:
                        return str([]), 200
                    if messages is not 0:
                        part = []
                        for participant in chat.participants:
                            part.append({
                                'author': participant.login,
                                'author_id': participant.id,
                                'author_photo': str(participant.profile_photo),
                            })
                        result = []
                        for message in messages:
                            result.append(message.as_dict())
                        response_object = ({
                            'chat_id': chat.id,
                            'chat_name': chat.name,
                            'participants': part,
                            'messages': result
                        })
                        return jsonify(response_object), 200
                    else:
                        return str([]), 200
            abort(401)
        abort(400)
    abort(401)


@login_required
@message.route('/chats/<int:id>/send', methods=['POST'])
def send_pm(id):
    print(current_user)
    if current_user.is_authenticated:
        data = request.get_json()
        if id is not None and data is not None:
            conv = chat_model.Chat.query.get(id)
            if conv is not None:
                for user in conv.participants:
                    if user.id is current_user.id:
                        if conv is not None:
                            new_message = message_model.Message(
                                author_id=current_user.id, message_text=data["message_text"], content_image=data["content_image"])
                            conv.messages.append(new_message)
                            db.session.commit()
                            return new_message.as_dict(), 200
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
            conv = chat_model.Chat(
                name=data["chat_name"], participants=data["participants"])
            if (conv.participants is None) or (conv.participants.count() < len(data["participants"])):
                return "Some users could not be added to chat", 400
            db.session.commit()
            participants_id = []
            for participant in data["participants"]:
                participants_id.append(participant)
            return jsonify({
                'chat_id': conv.id,
                'chat_name': conv.name,
                'participants': participants_id
            }), 200
        abort(400)
    abort(401)
