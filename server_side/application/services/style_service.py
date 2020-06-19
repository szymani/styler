from flask import request
from sqlalchemy import desc

from application import db, ma
from ..models import user_model, style_model
from flask_login import current_user
from ..services import helper_func


def add_style(data):
    new_style = style_model.Style(
        author_id=current_user.id, isprivate=data["isprivate"], style_image=data["style_image"], description=data["description"])
    db.session.add(new_style)
    db.session.commit()
    return new_style


def check_auth(wanted_style):
    try:
        return (current_user.is_authenticated and (wanted_style.style_author.id == current_user.id or current_user.user_type == 1))
    except:
        return (current_user.is_authenticated and (wanted_style.first().style_author.id == current_user.id or current_user.user_type == 1))


def check_auth_view(wanted_style):
    try:
        return (current_user.is_authenticated and (wanted_style.style_author.id == current_user.id or current_user.user_type == 1 or wanted_style.isprivate == False))
    except:
        return (current_user.is_authenticated and (wanted_style.style_author.id == current_user.id or current_user.user_type == 1 or wanted_style.isprivate == False))


def get_style_by_id(id):
    return style_model.Style.query.get(id)


def get_as_list(id):
    return style_model.Style.query.filter(style_model.Style.id == id)


def add_to_fav(style):
    current_user.fav_styles.append(style)
    db.session.commit()
    return style


def get_all_styles(limit, page):
    return style_model.Style.query.filter(style_model.Style.isprivate == False).order_by(
        desc(style_model.Style.creation_date)).paginate(
        page=page, per_page=limit).items


def get_your_styles(limit, page):
    return current_user.author_of_styles.order_by(
        desc(style_model.Style.creation_date)).paginate(
        page=page, per_page=limit).items


def get_fav_styles(limit, page):
    return helper_func.paginate_list(current_user.fav_styles.all(), page_num=page, limit=limit)


def get_followed_styles(limit, page):
    styles = []
    for followed in current_user.followed.all():
        for style in followed.author_of_styles.all():
            styles.append(style)
    styles.sort(key=lambda style: style.creation_date, reverse=True)
    return helper_func.paginate_list(styles, page_num=page, limit=limit)


def delete_style(wanted_style):
    db.session.delete(wanted_style)
    db.session.commit()
    return wanted_style


def update_style(wanted_style, data):
    wanted_style.update(data)
    db.session.commit()
    return wanted_style
