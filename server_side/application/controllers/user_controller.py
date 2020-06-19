from flask import request, send_file, make_response, jsonify, Blueprint, abort
from flask_login import login_required, logout_user, current_user
from io import BytesIO

from application import db, ma
from ..models import user_model, comment_model
from ..services import helper_func

user = Blueprint('user', __name__)


@login_required
@user.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    if id is not None:
        if current_user.is_authenticated:
            wanted_user = user_model.User.query.get(id)
            if wanted_user is not None:
                return wanted_user.as_dict(), 200
            abort(404, "User not found")
        else:  # restricted access to somebody else
            abort(401)
    abort(400)


@login_required
@user.route('/user/', methods=['GET'])
def get_user_by_login():
    limit, page_num = helper_func.set_limit_and_page(request)
    if current_user.is_authenticated:
        wanted_users = user_model.User.query.filter(
            user_model.User.login.contains(str(request.args.get('login'))))
        if wanted_users is not None:
            result = []
            for i in range((page_num - 1) * limit, page_num * limit):
                try:
                    result.append(wanted_users.all()[i].as_dict())
                except:
                    break
            return jsonify(result), 200
        abort(404, "No user with this login")
    else:  # restricted access to somebody else
        abort(401)


@login_required
@user.route('/user/self', methods=['GET'])
def get_self():
    print(request.headers.get('Authorization', '').split())
    if current_user.is_authenticated:
        return current_user.as_dict(), 200
    else:  # restricted access to somebody else
        abort(401)


@login_required
@user.route('/user/', methods=['PUT'])
def update_self():
    if current_user.is_authenticated:
        data = request.get_json()
        if data is not None:
            if (user_model.User.query.filter_by(login=data["login"]).first() is
                    None) or (current_user.id
                              == user_model.User.query.filter_by(
                                  login=data["login"]).first().id):
                if (user_model.User.query.filter_by(
                        email=data["email"]).first() is
                        None) or (current_user.if_this_user(
                            user_model.User.query.filter_by(
                                email=data["email"]).first().id)):
                    updated_user = user_model.User.query.get(current_user.id)
                    updated_user.update(login=data["login"],
                                        password=data["password"],
                                        email=data["email"],
                                        profile_photo=data["profile_photo"])
                    db.session.commit()
                    return updated_user.as_dict(), 200
                abort(400, "Email taken")
            abort(400, "Login taken")
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
                if (user_model.User.query.filter_by(
                        login=data["login"]).first() is
                        None) or (id == user_model.User.query.filter_by(
                            login=data["login"]).first().id):
                    if (user_model.User.query.filter_by(
                            email=data["email"]).first() is
                            None) or (id == user_model.User.query.filter_by(
                                login=data["email"]).first().id):
                        updated_user = user_model.User.query.get(id)
                        updated_user.update(
                            login=data["login"],
                            password=data["password"],
                            email=data["email"],
                            profile_photo=data["profile_photo"])
                        db.session.commit()
                        return updated_user.as_dict(), 200
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
        this_user = current_user
        db.session.delete(this_user)
        db.session.commit()
        return this_user.as_dict(), 200
    else:  # restricted access to somebody else
        abort(401)


@login_required
@user.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    if id is not None:
        if user_model.User.query.get(id) is not None:
            if current_user.is_authenticated and (current_user.id == id or
                                                  current_user.user_type == 1):
                this_user = user_model.User.query.get(id)
                db.session.delete(this_user)
                db.session.commit()
                return this_user.as_dict(), 200
            else:  # restricted access to somebody else
                abort(401)
        abort(404, "No user with this id")
    abort(400)


@login_required
@user.route('/user/<int:id>/follow', methods=['PUT'])
def follow_user(id):
    if id is not None:
        if user_model.User.query.get(id) is not None:
            if current_user.is_authenticated:
                if (len(current_user.followed.filter(user_model.User.id == id).all())) is 0:
                    this_user = current_user
                    this_user.followed.append(user_model.User.query.get(id))
                    db.session.commit()
                    responseObject = {
                        'followed': [({
                            'id': follow.id,
                        }) for follow in this_user.followed],
                    }
                    return make_response(
                        jsonify(responseObject)), 200
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
        if user_model.User.query.get(id) is not None:
            if current_user.is_authenticated:
                if (len(current_user.followed.filter(user_model.User.id == id).all())) is not 0:
                    this_user = current_user
                    try:
                        this_user.followed.remove(
                            user_model.User.query.get(id))
                    except:
                        pass
                    db.session.commit()
                    responseObject = {
                        'followed': [({
                            'id': follow.id,
                        }) for follow in this_user.followed],
                    }
                    return make_response(jsonify(responseObject)), 200
                else:
                    abort(404, "Not followed")
            else:  # restricted access to somebody else
                abort(401)
        abort(404, "No user with this id")
    abort(400)


@ login_required
@ user.route('/user/followed/', methods=['GET'])
def get_followed_self():
    print(current_user)
    limit, page_num = helper_func.set_limit_and_page(request)

    if current_user.is_authenticated:
        result = []
        for i in range((page_num - 1) * limit, page_num * limit):
            try:
                result.append(current_user.followed[i].as_dict())
            except:
                break
        return jsonify(result), 200
    else:  # restricted access to somebody else
        abort(401)


@ login_required
@ user.route('/user/followers/', methods=['GET'])
def get_followers_self():
    limit, page_num = helper_func.set_limit_and_page(request)
    if current_user.is_authenticated:
        result = []
        for i in range((page_num - 1) * limit, page_num * limit):
            try:
                result.append(current_user.followers[i].as_dict())
            except:
                break
        return jsonify(result), 200
    else:  # restricted access to somebody else
        abort(401)


@ login_required
@ user.route('/user/<int:id>/followed/', methods=['GET'])
def get_followed(id):
    limit, page_num = helper_func.set_limit_and_page(request)
    if current_user.is_authenticated:
        wanted_user = user_model.User.query.get(id)
        if wanted_user is not None:
            result = []
            for i in range((page_num - 1) * limit, page_num * limit):
                try:
                    result.append(wanted_user.followed[i].as_dict())
                except:
                    break
            return jsonify(result), 200
        else:
            abort(404, "No user with this id")
    else:  # restricted access to somebody else
        abort(401)


@ login_required
@ user.route('/user/<int:id>/followers/', methods=['GET'])
def get_followers(id):
    limit, page_num = helper_func.set_limit_and_page(request)
    if current_user.is_authenticated:
        wanted_user = user_model.User.query.get(id)
        if wanted_user is not None:
            result = []
            for i in range((page_num - 1) * limit, page_num * limit):
                try:
                    result.append(wanted_user.followers[i].as_dict())
                except:
                    break
            return jsonify(result), 200
        else:
            abort(404, "No user with this id")
    else:  # restricted access to somebody else
        abort(401)
