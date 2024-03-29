from flask import request
from flask import current_app as app
import numpy as np

from application import db
from ..models import SinglePost, User
from flask_login import current_user
from ..services import tag_service
from .process_image import ProcessImage


def add_post(data, new_style=None):
    tags = tag_service.getTagsFromString(str(data["tags"]))
    if new_style is None:
        new_post = SinglePost(
            content_image=data["content_image"],
            author_id=current_user.id,
            description=data["description"],
            style_id=data["style_id"],
            isprivate=data["isprivate"])
    else:
        new_post = SinglePost(
            content_image=data["content_image"],
            author_id=current_user.id,
            description=data["description"],
            style_id=new_style.id,
            isprivate=data["isprivate"])
    [new_post.tags.append(tag) for tag in tags]
    db.session.add(new_post)
    db.session.commit()
    compute_thread = ProcessImage(
        new_post.id, app._get_current_object())
    compute_thread.start()
    return new_post


def get_post(id):
    return SinglePost.query.get(id)


def get_post_as_list(id):
    return SinglePost.query.filter(SinglePost.id == id)


def get_posts(id, page_num, limit):
    return (SinglePost.query.filter(SinglePost.author_id == id).paginate(page=page_num, per_page=limit).items)


def get_posts_by_tag(tag, page, limit):
    posts = tag_service.getPostsWithTag(tag)
    if posts != []:
        return posts.order_by(
            SinglePost.upvotes.desc()).paginate(page=page, per_page=limit).items
    else:
        return posts


def get_followed_posts(page_num, limit):
    return (SinglePost.query
            .filter(SinglePost.author_id.in_(
                [followed_user.id for followed_user in current_user.followed.all()]))
            .order_by(SinglePost.creation_date.desc())
            .paginate(page=page_num, per_page=limit).items)


def update_post(wanted_post, data):
    tags = tag_service.getTagsFromString(str(data["tags"]))
    wanted_post.update(
        description=data["description"] or wanted_post.description,
        content_image=data["content_image"].encode(
            'ascii') or wanted_post.content_image,
        isprivate=data["isprivate"]
    )
    [wanted_post.tags.append(tag) for tag in tags]
    db.session.commit()
    return wanted_post


def delete_post(wanted_post):
    db.session.delete(wanted_post)
    db.session.commit()
    return wanted_post


def check_auth(wanted_post):
    if current_user.is_authenticated:
        if wanted_post.author_id == current_user.id or current_user.user_type == 1:
            return True
    return False


def is_liked(wanted_post):
    return wanted_post.who_liked.filter(User.id == current_user.id).first() is not None


def like_post(wanted_post):
    wanted_post.who_liked.append(current_user)
    wanted_post.upvotes = wanted_post.upvotes + 1
    db.session.commit()
    return wanted_post


def unlike_post(wanted_post):
    wanted_post.who_liked.remove(current_user)
    wanted_post.upvotes = wanted_post.upvotes - 1
    db.session.commit()
    return wanted_post


def get_who_liked(wanted_post):
    result = []
    for single_user in wanted_post.who_liked:
        result.append(single_user)
    return result
