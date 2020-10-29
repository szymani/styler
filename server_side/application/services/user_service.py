from application import db
from ..models import User
from flask_login import current_user


def get_user(id):
    return User.query.get(id)


def if_users_exist(list_of_users):
    for user in list_of_users:
        try:
            User.query.get(id)
        except:
            return False
    return True


def get_user_by_login(name):
    return User.query.filter(User.login.contains(name)).all()


def if_login_free(login):
    if User.query.filter_by(login=login).first() is not None:
        if User.query.filter_by(login=login).first().id != current_user.id:
            False
    return True


def if_email_free(email):
    if User.query.filter_by(email=email).first() is not None:
        if User.query.filter_by(email=email).first().id != current_user.id:
            False
    return True


def update_user(id, data):
    updated_user = get_user(id)
    updated_user.update(
        login=data["login"] or updated_user.login,
        password=data["password"] or updated_user.password,
        email=data["email"] or updated_user.email,
        profile_photo=data["profile_photo"].encode(
            'ascii') or updated_user.profile_photo,
        description=data["description"] or updated_user.description)
    db.session.commit()
    return updated_user


def add_user():
    pass


def delete_user(id):
    user = get_user(id)
    db.session.delete(user)
    db.session.commit()
    return user


def check_auth(id):
    return current_user.is_authenticated and (current_user.id == id or
                                              current_user.user_type == 1)


def follow(id):
    try:
        current_user.followed.append(
            get_user(id))
    except:
        pass
    db.session.commit()
    return get_user(id), 200


def unfollow(id):
    try:
        current_user.followed.remove(
            get_user(id))
    except:
        pass
    db.session.commit()
    return get_user(id), 200


def isFollowed(id):
    return (len(current_user.followed.filter(User.id == id).all())) != 0


def get_followers(id):
    return User.query.filter_by(id=id).first().followers


def get_followed(id):
    return User.query.filter_by(id=id).first().followed
