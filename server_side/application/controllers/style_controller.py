from flask import request, send_file, Blueprint
from flask import current_app as app
from flask_login import current_user
from io import BytesIO

from application import db, ma
from ..models import user_model, style_model
from ..services import style_service

style = Blueprint('style', __name__)


@style.route('/style', methods=['POST'])
def add_style():
    data = request.get_json()
    if data is not None:
        if current_user.is_authenticated:
            new_style = style_model.Style(
                author_id=current_user.id, isprivate=data["isprivate"], style_image=None, description=data["description"])
            db.session.add(new_style)
            db.session.commit()
            # TODO return whole style
            return str((new_style.id, new_style.isprivate)), 200
        abort(401)
    abort(400)


@style.route('/style/<int:id>', methods=['POST'])
def add_style_to_fav(id):
    if id is not None:
        wanted_style = style_model.Style.query.get(id)
        if wanted_style is not None:
            if current_user.is_authenticated:
                if wanted_style.isprivate and not (wanted_style.style_author.id == current_user.id or current_user.user_type == 1):
                    abort(401)
                # TODO return whole style
                current_user.fav_styles.append(wanted_style)
                db.session.commit()
                return current_user.fav_styles, 200
        abort(404, "No style with this id")
    abort(400)
    data = request.get_json()
    if data is not None:
        if current_user.is_authenticated:
            new_style = style_model.Style(
                author_id=current_user.id, isprivate=data["isprivate"], style_image=None, description=data["description"],)
            db.session.add(new_style)
            db.session.commit()
            # TODO return whole style
            return str(new_style.style_author_id), 200
        abort(401)
    abort(400)


@style.route('/style/<int:id>', methods=['GET'])
def get_style(id):
    if id is not None:
        wanted_style = style_model.Style.query.get(id)
        if wanted_style is not None:
            if current_user.is_authenticated:
                if wanted_style.isprivate and not (wanted_style.style_author.id == current_user.id or current_user.user_type == 1):
                    abort(401)
                # TODO return whole style
                return str((wanted_style.id, wanted_style.isprivate)), 200
        abort(404, "No style with this id")
    abort(400)


@style.route('/styles/all', methods=['GET'])
def get_all_styles():
    data = request.get_json()
    if data["limit"] != 0 and current_user.is_authenticated:
        if id is not None:
            wanted_styles = style_model.Style.query.filter(style_model.Style.isprivate == False).paginate(
                page=data["page"] if data["page"] != None else 1, per_page=data["limit"])
            if wanted_styles is not None:
                # TODO serialization of whole styles
                return str([(stylee.id, stylee.isprivate) for stylee in wanted_styles.items]), 200
            else:
                abort(404)
    abort(400)


@style.route('/styles/', methods=['GET'])
def get_your_styles():
    data = request.get_json()
    if data["limit"] != 0 and current_user.is_authenticated:
        if id is not None:
            wanted_styles = current_user.author_of_styles.paginate(
                page=data["page"] if data["page"] != None else 1, per_page=data["limit"])
            if wanted_styles is not None:
                # TODO serialization of whole styles
                return wanted_styles.first().login, 200
            else:
                abort(404)
    abort(400)


@style.route('/styles/favourite', methods=['GET'])
def get_fav_styles():
    data = request.get_json()
    if data["limit"] != 0 and current_user.is_authenticated:
        if id is not None:
            wanted_styles = current_user.fav_styles.paginate(
                page=data["page"] if data["page"] != None else 1, per_page=data["limit"])
            if wanted_styles is not None:
                # TODO serialization of whole styles
                return wanted_styles.first().login
            else:
                abort(404)
    abort(400)


@style.route('/styles/followed', methods=['GET'])
def get_followed_styles():
    data = request.get_json()
    if data["limit"] != 0 and current_user.is_authenticated:
        if id is not None:
            wanted_styles = current_user.fav_styles.paginate(
                page=data["page"] if data["page"] != None else 1, per_page=data["limit"])
            if wanted_styles is not None:
                # TODO serialization of whole styles
                return wanted_styles.first().login
            else:
                abort(404)
    abort(400)


@style.route('/style/<int:id>', methods=['PUT'])
def update_style(id):
    data = request.get_json()
    if data is not None and id is not None:
        wanted_style = style_model.Style.query.get(id)
        if wanted_style is not None:
            if current_user.is_authenticated and (wanted_style.style_author.id == current_user.id or current_user.user_type == 1):
                wanted_style.update(data)
                db.session.commit()
                # TODO return whole style
                return str((wanted_style.id, wanted_style.isprivate)), 200
            abort(401)
        abort(404, "No style with this id")
    abort(400)


@style.route('/style/<int:id>', methods=['DELETE'])
def delete_style(id):
    if id is not None:
        wanted_style = style_model.Style.query.get(id)
        if wanted_style is not None:
            if current_user.is_authenticated and (wanted_style.style_author.id == current_user.id or current_user.user_type == 1):
                db.session.delete(wanted_style)
                db.session.commit()
                # TODO return whole style
                return str((wanted_style.id, wanted_style.isprivate)), 200
            abort(401)
        abort(404, "No style with this id")
    abort(400)
