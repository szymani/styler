from flask import request, Blueprint, jsonify, abort
from flask_login import login_required, current_user

from ..schemas import schemas
from ..services import helper_func, style_service, post_service


single_post = Blueprint('single_post', __name__)
post_schema = schemas.PostSchema()
posts_schema = schemas.PostSchema(many=True)
users_schema_basic = schemas.UserSchema(
    many=True, exclude=['password', 'email', 'messages', 'chats'])


@login_required
@single_post.route('/post', methods=['POST'])
def add_post_prestyle():
    data = request.get_json()
    if data is not None:
        if current_user.is_authenticated:
            if style_service.get_style_by_id(data["style_id"]):
                try:
                    return jsonify(post_schema.dump(post_service.add_post(data))), 200
                except Exception as e:
                    print(str(e))
            else:
                abort(404, "Style not found")
        else:
            abort(401)
    abort(400)


@login_required
@single_post.route('/post/custom', methods=['POST'])
def add_post_custom():
    data = request.get_json()
    if data is not None:
        if current_user.is_authenticated:
            new_style = style_service.add_style(data)
            try:
                return jsonify(post_schema.dump(post_service.add_post(data, new_style))), 200
            except Exception as e:
                print(str(e))
        else:
            abort(401)
    abort(400)


@ login_required
@ single_post.route('/post/<int:id>', methods=['PUT'])
def update_post(id):
    data = request.get_json()
    if data is not None:
        wanted_post = post_service.get_post(id)
        if wanted_post is not None:
            if post_service.check_auth(wanted_post):
                try:
                    return jsonify(post_schema.dump(post_service.update_post(wanted_post, data))), 200
                except Exception as e:
                    abort(400)
            else:
                abort(401)
    abort(400)


@ login_required
@ single_post.route('/post/<int:id>', methods=['GET'])
def get_post(id):
    wanted_post = post_service.get_post(id)
    if wanted_post is None:
        abort(404, "No post with this id")
    else:
        return jsonify(post_schema.dump(wanted_post)), 200


@ login_required
@ single_post.route('/user/<int:id>/posts/', methods=['GET'])
def get_posts(id):
    limit, page_num = helper_func.set_limit_and_page(request)
    if current_user.is_authenticated:
        if id is not None:
            try:
                return jsonify(posts_schema.dump(post_service.get_posts(id, page_num, limit))), 200
            except:
                abort(400)
    abort(400)


@ login_required
@ single_post.route('/user/followed/posts/', methods=['GET'])
def get_followed_posts():
    limit, page_num = helper_func.set_limit_and_page(request)
    if current_user.is_authenticated:
        return jsonify(posts_schema.dump(post_service.get_followed_posts(page_num, limit))), 200
    abort(400)


@ login_required
@ single_post.route('/post/<int:id>', methods=['DELETE'])
def delete_post(id):
    if id is not None:
        wanted_post = post_service.get_post(id)
        if wanted_post:
            if post_service.check_auth(wanted_post):
                result = jsonify(post_schema.dump(wanted_post))
                post_service.delete_post(wanted_post)
                return result, 200
            else:  # restricted access to somebody else
                abort(401)
        abort(404, "No post with this id")
    abort(400)


@ login_required
@ single_post.route('/post/<int:id>/like', methods=['PUT'])
def like_post(id):
    wanted_post = post_service.get_post(id)
    if wanted_post is not None:
        if not post_service.is_liked(wanted_post):
            return jsonify(post_schema.dump(post_service.like_post(wanted_post))), 200
        else:
            abort(400, "Already liked")
    else:
        abort(404, "Wrong post id")


@ login_required
@ single_post.route('/post/<int:id>/unlike', methods=['PUT'])
def unlike_post(id):
    wanted_post = post_service.get_post(id)
    if wanted_post is not None:
        if post_service.is_liked(wanted_post):
            return jsonify(post_schema.dump(post_service.unlike_post(wanted_post))), 200
        else:
            abort(400, "Not liked yet")
    else:
        abort(404, "Wrong post id")


@ login_required
@ single_post.route('/post/<int:id>/likes/', methods=['GET'])
def get_who_liked(id):
    limit, page_num = helper_func.set_limit_and_page(request)
    if current_user.is_authenticated:
        wanted_post = post_service.get_post(id)
        if wanted_post is not None:
            return jsonify(users_schema_basic.dump(post_service.get_who_liked(wanted_post))), 200
        else:
            abort(404, "Wrong post id")
    abort(400)
