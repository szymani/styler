from flask import request, send_file, Blueprint, make_response, jsonify, abort
from flask import current_app as app
from flask_login import login_required, logout_user, current_user
from io import BytesIO

from application import db, ma
from ..schemas import schemas
from ..services import helper_func, comment_service

comment = Blueprint('comment', __name__)
comment_schema = schemas.CommentSchema()
comments_schema = schemas.CommentSchema(many=True)


@login_required
@comment.route('/post/<int:id>/comment', methods=['POST'])
def add_comment(id):
    data = request.get_json()
    if data is not None and id is not None:
        if current_user.is_authenticated:
            new_comment = comment_service.add_comment(id, data)
            return jsonify(comment_schema.dump(new_comment)), 200
        abort(401)
    abort(400)


@login_required
@comment.route('/comments/<int:id>', methods=['GET'])
def get_comment(id):
    if id is not None:
        wanted_comment = comment_service.get_comment(id)
        if wanted_comment is not None:
            if comment_service.check_auth(wanted_comment):
                return jsonify(comment_schema.dump(wanted_comment)), 200
        abort(404, "No comment with this id")
    abort(400)


@login_required
@comment.route('/post/<int:id>/comments/', methods=['GET'])
def get_comments(id):
    limit, page_num = helper_func.set_limit_and_page(request)
    if current_user.is_authenticated:
        if id is not None:
            try:
                wanted_comments = comment_service.get_comments(
                    id, page_num, limit)
                return jsonify(comments_schema.dump(wanted_comments.items)), 200
            except:
                return jsonify([]), 200
    abort(400)


@login_required
@comment.route('/comments/<int:id>', methods=['PUT'])
def update_comment(id):
    data = request.get_json()
    if data is not None and id is not None:
        wanted_comment = comment_service.get_as_list(id)
        if wanted_comment is not None:
            try:
                if comment_service.check_auth(wanted_comment):
                    comment_service.update_comment(wanted_comment, data)
                    return jsonify(comment_schema.dump(comment_service.update_comment(wanted_comment, data).first())), 200
            except Exception as e:
                abort(400, f'Exception {e}')
            abort(401)
        abort(404, "No comment with this id")
    abort(400)


@ login_required
@ comment.route('/comments/<int:id>', methods=['DELETE'])
def delete_comment(id):
    if id is not None:
        wanted_comment = comment_service.get_comment(id)
        if wanted_comment is not None:
            if comment_service.check_auth(wanted_comment):
                return jsonify(comment_schema.dump(comment_service.delete_comment(wanted_comment))), 200
            abort(401)
        abort(404, "No comment with this id")
    abort(400)
