from flask import request, send_file, Blueprint, abort, jsonify
from flask import current_app as app
from flask_login import current_user, login_required
from io import BytesIO

from application import ma
from ..schemas import schemas
from ..services import style_service, helper_func

style = Blueprint('style', __name__)
style_schema = schemas.StyleSchema()
styles_schema = schemas.StyleSchema(many=True)
users_schema_basic = schemas.UserSchema(
    many=True, exclude=['password', 'email', 'messages', 'chats'])


@ login_required
@style.route('/style/', methods=['POST'])
def add_style():
    data = request.get_json()
    if data is not None:
        if current_user.is_authenticated:
            new_style = style_service.add_style(data)
            return jsonify(style_schema.dump(new_style)), 200
        abort(401)
    abort(400)


@ login_required
@style.route('/style/<int:id>', methods=['PUT'])
def update_style(id):
    data = request.get_json()
    if data is not None and id is not None:
        wanted_style = style_service.get_style_by_id(id)
        if wanted_style is not None:
            if style_service.check_auth(wanted_style):
                wanted_style = style_service.update_style(wanted_style, data)
                return jsonify(style_schema.dump(wanted_style)), 200
            abort(401)
        abort(404, "No style with this id")
    abort(400)


@ login_required
@style.route('/style/<int:id>', methods=['DELETE'])
def delete_style(id):
    if id is not None:
        wanted_style = style_service.get_style_by_id(id)
        if wanted_style is not None:
            if style_service.check_auth(wanted_style):
                wanted_style = style_service.delete_style(wanted_style)
                return jsonify(style_schema.dump(wanted_style)), 200
            abort(401)
        abort(404, "No style with this id")
    abort(400)


@ login_required
@ style.route('/style/favourite/<int:id>/add', methods=['PUT'])
def add_style_to_fav(id):
    if id is not None:
        wanted_style = style_service.get_style_by_id(id)
        if wanted_style is not None:
            if current_user.is_authenticated:
                if style_service.check_auth_view(wanted_style):
                    style_service.add_to_fav(wanted_style)
                    return jsonify(style_schema.dump(wanted_style)), 200
                abort(401)
        abort(404, "No style with this id")
    abort(400)


@ login_required
@ style.route('/style/favourite/<int:id>/remove', methods=['PUT'])
def remove_style_from_fav(id):
    if id is not None:
        wanted_style = style_service.get_style_by_id(id)
        if wanted_style is not None:
            if current_user.is_authenticated:
                if style_service.check_auth_view(wanted_style):
                    style_service.remove_from_fav(wanted_style)
                    return jsonify(style_schema.dump(wanted_style)), 200
                abort(401)
        abort(404, "No style with this id")
    abort(400)


@ login_required
@ style.route('/style/<int:id>/like', methods=['PUT'])
def like_style(id):
    wanted_style = style_service.get_style_by_id(id)
    if wanted_style is not None:
        if not style_service.is_liked(wanted_style):
            return jsonify(style_schema.dump(style_service.like_style(wanted_style))), 200
        else:
            abort(400, "Already liked")
    else:
        abort(404, "Wrong style id")


@ login_required
@ style.route('/style/<int:id>/unlike', methods=['PUT'])
def unlike_style(id):
    wanted_style = style_service.get_style_by_id(id)
    if wanted_style is not None:
        if style_service.is_liked(wanted_style):
            return jsonify(style_schema.dump(style_service.unlike_style(wanted_style))), 200
        else:
            abort(400, "Not liked yet")
    else:
        abort(404, "Wrong style id")


@ login_required
@ style.route('/style/<int:id>', methods=['GET'])
def get_style(id):
    if id is not None:
        wanted_style = style_service.get_style_by_id(id)
        if wanted_style is not None:
            if current_user.is_authenticated:
                if style_service.check_auth_view(wanted_style):
                    return jsonify(style_schema.dump(wanted_style)), 200
                abort(401)
        abort(404, "No style with this id")
    abort(400)


@ login_required
@ style.route('/styles/all/<int:id>', methods=['GET'])
def get_all_styles(id):
    if id is not None:
        return get_styles_generic(request, "all", id)
    else:
        return get_styles_generic(request, "all")


@ login_required
@ style.route('/styles/<int:id>', methods=['GET'])
def get_your_styles(id):
    if id is not None:
        return get_styles_generic(request, "your", id)
    else:
        return get_styles_generic(request, "your")


@ login_required
@ style.route('/styles/favourite/<int:id>', methods=['GET'])
def get_fav_styles(id):
    if id is not None:
        return get_styles_generic(request, "fav", id)
    else:
        return get_styles_generic(request, "fav")


@ login_required
@ style.route('/styles/followed/<int:id>', methods=['GET'])
def get_followed_styles(id):
    if id is not None:
        return get_styles_generic(request, "followed", id)
    else:
        return get_styles_generic(request, "followed")


def get_styles_generic(request, request_type, id):
    limit, page_num = helper_func.set_limit_and_page(request)
    if limit and current_user.is_authenticated:
        wanted_styles = None
        if id is None:
            if request_type == "followed":
                wanted_styles = style_service.get_followed_styles(
                    limit, page_num)
            elif request_type == "all":
                wanted_styles = style_service.get_all_styles(limit, page_num)
            elif request_type == "fav":
                wanted_styles = style_service.get_fav_styles(limit, page_num)
            elif request_type == "your":
                wanted_styles = style_service.get_your_styles(limit, page_num)
        else:
            if request_type == "followed":
                wanted_styles = style_service.get_followed_styles(
                    limit, page_num, id)
            elif request_type == "all":
                wanted_styles = style_service.get_all_styles(
                    limit, page_num, id)
            elif request_type == "fav":
                wanted_styles = style_service.get_fav_styles(
                    limit, page_num, id)
            elif request_type == "your":
                wanted_styles = style_service.get_your_styles(
                    limit, page_num, id)
        return jsonify(styles_schema.dump(wanted_styles)), 200

    abort(400)


@ login_required
@ style.route('/style/<int:id>/likes/', methods=['GET'])
def get_liked_style(id):
    limit, page_num = helper_func.set_limit_and_page(request)
    if current_user.is_authenticated:
        wanted_style = style_service.get_style_by_id(id)
        if wanted_style is not None:
            return jsonify(users_schema_basic.dump(style_service.get_who_liked(wanted_style))), 200
        else:
            abort(404, "Wrong post id")
    abort(400)
