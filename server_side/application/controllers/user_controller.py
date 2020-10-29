from flask import request, send_file, make_response, jsonify, Blueprint, abort
from flask_login import login_required, logout_user, current_user
from io import BytesIO

from application import db, ma
from ..models import user_model, comment_model
from ..services import helper_func, user_service
from ..schemas import schemas

user = Blueprint('user', __name__)
user_schema_basic = schemas.UserSchema(
    exclude=['password', 'email', 'messages', 'chats'])
users_schema_basic = schemas.UserSchema(
    many=True, exclude=['password', 'email', 'messages', 'chats'])


@login_required
@user.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    if id is not None:
        if current_user.is_authenticated:
            wanted_user = user_service.get_user(id)
            if wanted_user is not None:
                return jsonify(user_schema_basic.dump(wanted_user)), 200
            abort(404, "User not found")
        else:  # restricted access to somebody else
            abort(401)
    abort(400)


@login_required
@user.route('/user/', methods=['GET'])
def get_user_by_login():
    limit, page_num = helper_func.set_limit_and_page(request)
    if current_user.is_authenticated:
        wanted_users = user_service.get_user_by_login(
            str(request.args.get('login')))
        if wanted_users is not None:
            wanted_users = helper_func.paginate_list(
                wanted_users, page_num, limit)
            return jsonify(users_schema_basic.dump(wanted_users)), 200
        abort(404, "No user with this login")
    else:  # restricted access to somebody else
        abort(401)


@login_required
@user.route('/user/self', methods=['GET'])
def get_self():
    if current_user.is_authenticated:
        return jsonify(user_schema_basic.dump(current_user)), 200
    else:  # restricted access to somebody else
        abort(401)


@login_required
@user.route('/user', methods=['PUT'])
def update_self():
    if user_service.check_auth(current_user.id):
        data = request.get_json()
        if data is not None:
            try:
                if user_service.if_login_free(data["login"]):
                    if user_service.if_email_free(data["email"]):
                        responseObject = {
                            'token': user_service.update_user(
                                current_user.id, data).encode_token()
                        }
                        return make_response(jsonify(responseObject)), 200
                    abort(400, "Email taken")
                abort(400, "Login taken")
            except Exception as e:
                print(str(e))
        abort(400)
    else:
        abort(401)


@login_required
@user.route('/user/<int:id>', methods=['PUT'])
def update_user(id=None):
    if current_user.is_authenticated and current_user.user_type == 1:
        data = request.get_json()
        if data is not None:
            try:
                if user_service.if_login_free(data["login"]):
                    if user_service.if_email_free(data["email"]):
                        responseObject = {
                            'token': user_service.update_user(
                                current_user.id, data).encode_token()
                        }
                        return make_response(jsonify(responseObject)), 200
                    abort(400, "Email taken")
                abort(400, "Login taken")
            except Exception as e:
                print(str(e))
        abort(400)
    else:
        abort(401)


@login_required
@user.route('/user/', methods=['DELETE'])
def delete_self():
    if current_user.is_authenticated:
        return jsonify(user_schema_basic.dump(user_service.delete_user(current_user.id))), 200
    else:  # restricted access to somebody else
        abort(401)


@login_required
@user.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    if id is not None:
        if user_service.get_user(id) is not None:
            if user_service.check_auth(id):
                return jsonify(user_schema_basic.dump(user_service.delete_user(id))), 200
            else:  # restricted access to somebody else
                abort(401)
        abort(404, "No user with this id")
    abort(400)


@login_required
@user.route('/user/<int:id>/follow', methods=['PUT'])
def follow_user(id):
    if id is not None:
        if user_service.get_user(id) is not None:
            if current_user.is_authenticated:
                if not user_service.isFollowed(id):
                    user_service.follow(id)
                    return jsonify(user_schema_basic.dump(current_user)), 200
                else:
                    abort(404, "Already followed")
            else:  # restricted access to somebody else
                abort(401)
        abort(404, "No user with this id")
    abort(400)


@ login_required
@ user.route('/user/<int:id>/unfollow', methods=['PUT'])
def unfollow_user(id):
    if id is not None:
        if user_service.get_user(id) is not None:
            if current_user.is_authenticated:
                if user_service.isFollowed(id):
                    user_service.unfollow(id)
                    return jsonify(user_schema_basic.dump(current_user)), 200
                else:
                    abort(404, "Not followed")
            else:  # restricted access to somebody else
                abort(401)
        abort(404, "No user with this id")
    abort(400)


@ login_required
@ user.route('/user/followed/', methods=['GET'])
def get_followed_self():
    limit, page_num = helper_func.set_limit_and_page(request)
    if current_user.is_authenticated:
        wanted_users = helper_func.paginate_list(
            current_user.followed, page_num, limit)
        return jsonify(users_schema_basic.dump(wanted_users)), 200
    else:  # restricted access to somebody else
        abort(401)


@ login_required
@ user.route('/user/followers/', methods=['GET'])
def get_followers_self():
    limit, page_num = helper_func.set_limit_and_page(request)
    if current_user.is_authenticated:
        wanted_users = helper_func.paginate_list(
            current_user.followers, page_num, limit)
        return jsonify(users_schema_basic.dump(wanted_users)), 200
    else:  # restricted access to somebody else
        abort(401)


@ login_required
@ user.route('/user/<int:id>/followed/', methods=['GET'])
def get_followed(id):
    limit, page_num = helper_func.set_limit_and_page(request)
    if current_user.is_authenticated:
        if id is not None:
            return jsonify(users_schema_basic.dump(user_service.get_followed(id))), 200
        else:
            abort(404, "No user with this id")
    else:  # restricted access to somebody else
        abort(401)


@ login_required
@ user.route('/user/<int:id>/followers/', methods=['GET'])
def get_followers(id):
    limit, page_num = helper_func.set_limit_and_page(request)
    if current_user.is_authenticated:
        if id is not None:
            return jsonify(users_schema_basic.dump(user_service.get_followers(id))), 200
        else:
            abort(404, "No user with this id")
    else:  # restricted access to somebody else
        abort(401)
