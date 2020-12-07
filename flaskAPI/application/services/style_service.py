from application.schemas.schemas import TagSchema
from application.services.user_service import follow
from application.services import user_service
from flask import request
from sqlalchemy import desc

from application import db, ma
from ..models import Style, User
from flask_login import current_user
from ..services import helper_func, tag_service


def add_style(data):
    tags = tag_service.getTagsFromString(str(data["tags"]))
    new_style = Style(
        author_id=current_user.id, isprivate=data["isprivate"],
        style_image=data["style_image"], description=data["description"])
    [new_style.tags.append(tag) for tag in tags]
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
    return Style.query.get(id)


def get_as_list(id):
    return Style.query.filter(Style.id == id)


def add_to_fav(style):
    if len(current_user.fav_styles.filter(Style.id == style.id).all()) == 0:
        current_user.fav_styles.append(style)
        db.session.commit()
    return style


def remove_from_fav(style):
    if len(current_user.fav_styles.filter(Style.id == style.id).all()) != 0:
        current_user.fav_styles.remove(style)
        db.session.commit()
    return style


def get_random_styles(limit, page):
    return Style.query.filter(Style.isprivate == False).order_by(
        desc(Style.creation_date)).paginate(
        page=page, per_page=limit).items


def get_all_styles(limit, page, id):
    all = []
    if id is None:
        followed = get_followed_styles(limit, page)
        fav = get_fav_styles(limit, page)
        your = get_your_styles(limit, page)
        all = followed + fav + your
    else:
        followed = get_followed_styles(limit, page, id)
        fav = get_fav_styles(limit, page, id)
        your = get_your_styles(limit, page, id)
        all = followed + fav + your
    all.sort(key=lambda x: x.creation_date, reversed=True)
    return helper_func.paginate_list(all, page, limit)


def get_your_styles(limit, page, id):
    if id is None:
        return current_user.author_of_styles.order_by(Style.creation_date.desc()).paginate(page=page, per_page=limit).items
    else:
        wanted_user = user_service.get_user(id)
        return wanted_user.author_of_styles.order_by(Style.creation_date.desc()).paginate(page=page, per_page=limit).items


def get_styles_by_tag(tag, limit, page):
    styles = tag_service.getStylesWithTag(tag)
    if styles != []:
        return styles.order_by(
            Style.upvotes.desc()).paginate(page=page, per_page=limit).items
    else:
        return styles


def get_fav_styles(limit, page, id):
    if id is None:
        return current_user.fav_styles.order_by(Style.creation_date.desc()).paginate(page=page, per_page=limit).items
    else:
        wanted_user = user_service.get_user(id)
        return wanted_user.fav_styles.order_by(Style.creation_date.desc()).paginate(page=page, per_page=limit).items


def get_followed_styles(limit, page, id):
    if id is None:
        return (Style.query
                .filter(Style.style_author_id.in_(
                    [followed_user.id for followed_user in current_user.followed.all()]))
                .order_by(Style.creation_date.desc())
                .paginate(page=page, per_page=limit).items)
    else:
        wanted_user = user_service.get_user(id)
        return (Style.query
                .filter(Style.style_author_id.in_(
                    [followed_user.id for followed_user in wanted_user.followed.all()]))
                .order_by(Style.creation_date.desc())
                .paginate(page=page, per_page=limit).items)


def delete_style(wanted_style):
    db.session.delete(wanted_style)
    db.session.commit()
    return wanted_style


def update_style(wanted_style, data):
    tags = tag_service.getTagsFromString(str(data["tags"]))
    wanted_style.update(
        description=data["description"] or wanted_style.description,
        style_image=data["style_image"].encode(
            'ascii') or wanted_style.style_image,
        isprivate=data["isprivate"]
    )
    wanted_style.tags = []
    [wanted_style.tags.append(tag) for tag in tags]
    db.session.commit()
    return wanted_style


def is_liked(wanted_style):
    return wanted_style.who_liked.filter(User.id == current_user.id).first() is not None


def like_style(wanted_style):
    wanted_style.who_liked.append(current_user)
    wanted_style.upvotes = wanted_style.upvotes + 1
    db.session.commit()
    return wanted_style


def unlike_style(wanted_style):
    wanted_style.who_liked.remove(current_user)
    wanted_style.upvotes = wanted_style.upvotes - 1
    db.session.commit()
    return wanted_style


def get_who_liked(wanted_style):
    result = []
    for single_user in wanted_style.who_liked:
        result.append(single_user)
    return result
