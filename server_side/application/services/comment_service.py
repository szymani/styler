from flask import request
from sqlalchemy import desc

from application import db, ma
from ..models import user_model, comment_model
from flask_login import current_user
from ..services import helper_func


def add_comment(id, data):
    new_comment = comment_model.Comment(
        author_id=current_user.id,
        post_id=id,
        description=data["description"])
    db.session.add(new_comment)
    db.session.commit()
    return new_comment


def get_comment(id):
    return comment_model.Comment.query.get(id)


def get_as_list(id):
    print("adsd ")
    return comment_model.Comment.query.filter(comment_model.Comment.id == id)


def check_auth(wanted_comment):
    try:
        return (current_user.is_authenticated and (wanted_comment.comment_author.id == current_user.id or current_user.user_type == 1))
    except:
        return (current_user.is_authenticated and (wanted_comment.first().comment_author.id == current_user.id or current_user.user_type == 1))


def delete_comment(wanted_comment):
    db.session.delete(wanted_comment)
    db.session.commit()
    return wanted_comment


def update_comment(wanted_comment, data):
    wanted_comment.update(data)
    db.session.commit()
    return wanted_comment


def get_comments(id, page_num, limit):
    return comment_model.Comment.query.filter(
        comment_model.Comment.post_id == id).paginate(
        page=page_num, per_page=limit)
