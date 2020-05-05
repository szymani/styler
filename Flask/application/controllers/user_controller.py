from flask import request, send_file, make_response
from flask import current_app as app
from io import BytesIO

from application import db, ma
from ..models import user, style

@app.route('/user/add', methods=['POST'])
def add_user():
    data = request.get_json()
    headers = {"Content-Type": "application/json"}
    if data is not None:
        if user.User.query.filter_by(login=data["login"]).first() is None:
            new_user = user.User(login= data["login"], password=data["password"])
            db.session.add(new_user)
            db.session.commit()
            return new_user.login, 200
        return "Login already exists", 200
    return "Empty request", 200

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    if id is not None:
        wanted_user = user.User.query.get(id)
        if wanted_user is not None:
            return wanted_user.login
        return "No user with this id", 200
    return "Empty request", 200