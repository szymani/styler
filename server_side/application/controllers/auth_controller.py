from flask import redirect, flash, request, make_response, jsonify, Blueprint, abort
from flask_login import current_user, login_user, login_required, logout_user
from flask import current_app as app
from .. import login_manager, db
from ..models import user_model
from ..schemas import schemas
import jwt

auth = Blueprint('auth', __name__)
users_schema_basic = schemas.UserSchema(
    many=True, exclude=['password', 'email', 'messages', 'chats'])


@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if (data is not None) and not ('' in data.values()):
        if user_model.User.query.filter_by(
                login=data["login"]).first() is None:
            if user_model.User.query.filter_by(
                    email=data["email"]).first() is None:
                new_user = user_model.User(login=data["login"],
                                           password=data["password"],
                                           email=data["email"],
                                           profile_photo=data["profile_photo"])
                db.session.add(new_user)
                db.session.commit()
                return jsonify(user_schema_basic.dump(new_user)), 200
            abort(400, "Email taken")
        abort(400, "Login taken")
    abort(400)


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    this_user = user_model.User.query.filter_by(
        login=data["login"]).first()  # Validate Login Attempt
    if data and this_user and this_user.check_password(
            password=data["password"]):
        return jsonify(user_schema_basic.dump(this_user)), 200
    abort(400, 'Invalid username/password combination')


@auth.route("/logout", methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return make_response(jsonify({'message': "Successfully logged out"})), 200


@login_manager.request_loader
def load_user_from_request(request):
    auth_headers = request.headers.get('Authorization', '').split()
    if len(auth_headers) != 2:
        return None
    try:
        token = auth_headers[1]
        data = jwt.decode(token, app.config.get('SECRET_KEY'))
        this_user = user_model.User.query.filter_by(
            login=data["login"]).first()
        if this_user:
            return this_user
    except jwt.ExpiredSignatureError:
        return None
    except (jwt.InvalidTokenError, Exception) as e:
        return None
    return None


@login_manager.unauthorized_handler
def unauthorized():
    abort(401)
