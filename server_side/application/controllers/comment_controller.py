from flask import request, send_file, Blueprint, make_response, jsonify
from flask import current_app as app
from flask_login import login_required, logout_user, current_user
from io import BytesIO

from application import db, ma
from ..models import user_model, comment_model
from ..services import helper_func

comment = Blueprint('comment', __name__)


@login_required
@comment.route('/post/<int:id>/comment/', methods=['POST'])
def add_comment(id):
    data = request.get_json()
    if data is not None and id is not None:
        if current_user.is_authenticated:
            new_comment = comment_model.Comment(
                author_id=current_user.id,
                post_id=id,
                description=data["description"])
            db.session.add(new_comment)
            db.session.commit()
            return new_comment.as_dict(), 200
        abort(401)
    abort(400)


@login_required
@comment.route('/post/<int:id>/comments/', methods=['GET'])
def get_comments(id):
    limit, page_num = helper_func.set_limit_and_page(request)
    if current_user.is_authenticated:
        if id is not None:
            try:
                wanted_comments = comment_model.Comment.query.filter(
                    comment_model.Comment.post_id == id).paginate(
                        page=page_num, per_page=limit)
            except:
                return str([]), 200
            if wanted_comments is not None:
                result = []
                for single_comment in wanted_comments.items:
                    result.append(single_comment.as_dict())
                return jsonify(result), 200
            else:
                abort(404)
    abort(400)


@login_required
@comment.route('/comment/<int:id>', methods=['PUT'])
def update_comment(id):
    data = request.get_json()
    if data is not None and id is not None:
        wanted_comment = comment_model.Comment.query.filter(
            comment_model.Comment.id == id)
        if wanted_comment is not None:
            try:
                if current_user.is_authenticated and (
                        wanted_comment.first().comment_author_id == current_user.id
                        or current_user.user_type == 1):
                    wanted_comment.update(data)
                    db.session.commit()
                    return wanted_comment.first().as_dict(), 200
            except:
                abort(400)
            abort(401)
        abort(404, "No comment with this id")
    abort(400)


@login_required
@comment.route('/comment/<int:id>', methods=['DELETE'])
def delete_comment(id):
    if id is not None:
        wanted_comment = comment_model.Comment.query.get(id)
        if wanted_comment is not None:
            if current_user.is_authenticated and (
                    wanted_comment.comment_author.id == current_user.id
                    or current_user.user_type == 1):
                db.session.delete(wanted_comment)
                db.session.commit()
                return wanted_comment.as_dict(), 200
            abort(401)
        abort(404, "No comment with this id")
    abort(400)
