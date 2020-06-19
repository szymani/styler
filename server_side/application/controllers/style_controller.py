from flask import request, send_file, Blueprint, abort, jsonify
from flask import current_app as app
from flask_login import current_user
from io import BytesIO

from application import ma
from ..schemas import schemas
from ..services import style_service, helper_func

style = Blueprint('style', __name__)
style_schema = schemas.StyleSchema()
styles_schema = schemas.StyleSchema(many=True)


@style.route('/style/', methods=['POST'])
def add_style():
    data = request.get_json()
    if data is not None:
        if current_user.is_authenticated:
            new_style = style_service.add_style(data)
            return jsonify(style_schema.dump(new_style)), 200
        abort(401)
    abort(400)


@style.route('/style/<int:id>', methods=['PUT'])
def update_style(id):
    data = request.get_json()
    if data is not None and id is not None:
        wanted_style = style_service.get_as_list(id)
        if wanted_style is not None:
            if style_service.check_auth(wanted_style):
                wanted_style = style_service.update_style(wanted_style, data)
                return jsonify(style_schema.dump(wanted_style.first())), 200
            abort(401)
        abort(404, "No style with this id")
    abort(400)


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


@ style.route('/style/favourite/<int:id>', methods=['PUT'])
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


@ style.route('/style/<int:id>', methods=['GET'])
def get_style(id):
    if id is not None:
        wanted_style = style_service.get_style_by_id(id)
        if wanted_style is not None:
            if current_user.is_authenticated:
                if style_service.check_auth(wanted_style):
                    return jsonify(style_schema.dump(wanted_style)), 200
                abort(401)
        abort(404, "No style with this id")
    abort(400)


@ style.route('/styles/all/', methods=['GET'])
def get_all_styles():
    return get_styles_generic(request, "all")


@ style.route('/styles/', methods=['GET'])
def get_your_styles():
    return get_styles_generic(request, "your")


@ style.route('/styles/favourite/', methods=['GET'])
def get_fav_styles():
    return get_styles_generic(request, "fav")


@ style.route('/styles/followed/', methods=['GET'])
def get_followed_styles():
    return get_styles_generic(request, "followed")


def get_styles_generic(request, request_type):
    limit, page_num = helper_func.set_limit_and_page(request)
    if limit and current_user.is_authenticated:
        if id is not None:
            wanted_styles = None
            if request_type is "followed":
                wanted_styles = style_service.get_followed_styles(
                    limit, page_num)
            elif request_type is "all":
                wanted_styles = style_service.get_all_styles(limit, page_num)
            elif request_type is "fav":
                wanted_styles = style_service.get_fav_styles(limit, page_num)
            elif request_type is "your":
                wanted_styles = style_service.get_your_styles(limit, page_num)
            return jsonify(styles_schema.dump(wanted_styles)), 200
    abort(400)
