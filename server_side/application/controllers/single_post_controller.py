from flask import request, send_file, Blueprint, jsonify, make_response, abort
from flask import current_app as app
from flask_login import login_required, logout_user, current_user
from io import BytesIO
import json
import numpy as np

from application import db, ma
from ..models import User, SinglePost
from ..schemas import schemas
from ..services import helper_func, style_service
from ..services.process_image import ProcessImage


single_post = Blueprint('single_post', __name__)
post_schema = schemas.PostSchema()
posts_schema = schemas.PostSchema(many=True)
# TODO Make service for posts


@login_required
@single_post.route('/post', methods=['POST'])
def add_post_prestyle():
    data = request.get_json()
    if data is not None:
        if current_user.is_authenticated:
            if style_service.get_style_by_id(data["style_id"]):
                try:
                    new_post = SinglePost(
                        content_image=data["content_image"],
                        author_id=current_user.id,
                        description=data["description"],
                        style_id=data["style_id"],
                        isprivate=data["isprivate"])
                    db.session.add(new_post)
                    db.session.commit()
                    compute_thread = ProcessImage(
                        new_post.id, app._get_current_object())
                    compute_thread.start()
                    return jsonify(post_schema.dump(new_post)), 200
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
            # TODO Create new style
            new_style = style_service.add_style(data)
            try:
                new_post = SinglePost(
                    content_image=data["content_image"],
                    author_id=current_user.id,
                    description=data["description"],
                    style_id=new_style.id,
                    isprivate=data["isprivate"])
                db.session.add(new_post)
                db.session.commit()
                compute_thread = ProcessImage(
                    new_post.id, app._get_current_object())
                compute_thread.start()
                return jsonify(post_schema.dump(new_post)), 200
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
        wanted_post = SinglePost.query.filter(SinglePost.id == id)
        if wanted_post.first():
            if current_user.is_authenticated and wanted_post.first().author_id == current_user.id:
                try:
                    wanted_post.update({
                        "description": data["description"],
                        "content_image": data["content_image"]
                    })
                    db.session.commit()
                    return jsonify(post_schema.dump(wanted_post.first())), 200
                except Exception as e:
                    abort(400)
            else:
                abort(401)
    abort(400)


@ login_required
@ single_post.route('/post/<int:id>', methods=['GET'])
def get_post(id):
    wanted_post = SinglePost.query.get(id)
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
                wanted_post = (SinglePost.query.filter(
                    SinglePost.author_id == id).paginate(
                        page=page_num, per_page=limit).items)
                print(wanted_post)
                return jsonify(posts_schema.dump(wanted_post)), 200
            except:
                abort(400)
    abort(400)


@ login_required
@ single_post.route('/user/followed/posts/', methods=['GET'])
def get_followed_posts():
    limit, page_num = helper_func.set_limit_and_page(request)
    if current_user.is_authenticated:
        followed_users = current_user.followed
        result = []
        for followed_user in followed_users:
            result.append(followed_user.posts)
        return jsonify(posts_schema.dump(np.asarray(result).flatten())), 200
    abort(400)


@ login_required
@ single_post.route('/post/<int:id>', methods=['DELETE'])
def delete_post(id):
    if id is not None:
        wanted_post = SinglePost.query.get(id)
        if wanted_post:
            if current_user.is_authenticated and (
                    current_user.id == wanted_post.author_id
                    or current_user.user_type == 1):
                db.session.delete(SinglePost.query.get(id))
                db.session.commit()
                return jsonify(post_schema.dump(wanted_post)), 200
            else:  # restricted access to somebody else
                abort(401)
        abort(404, "No post with this id")
    abort(400)


@ login_required
@ single_post.route('/post/<int:id>/like', methods=['PUT'])
def like_post(id):
    wanted_post = SinglePost.query.get(id)
    if wanted_post is not None:
        if wanted_post.who_liked.filter(User.id == current_user.id).first() is None:
            wanted_post.who_liked.append(current_user)
            wanted_post.upvotes = wanted_post.upvotes + 1
            db.session.commit()
            return jsonify(post_schema.dump(wanted_post)), 200
        else:
            abort(400, "Already liked")
    else:
        abort(404, "Wrong post id")


@ login_required
@ single_post.route('/post/<int:id>/unlike', methods=['PUT'])
def unlike_post(id):
    wanted_post = SinglePost.query.get(id)
    if wanted_post is not None:
        if wanted_post.who_liked.filter(User.id == current_user.id).first() is not None:
            wanted_post.who_liked.remove(current_user)
            wanted_post.upvotes = wanted_post.upvotes - 1
            db.session.commit()
            return jsonify(post_schema.dump(wanted_post)), 200
        else:
            abort(400, "Not liked yet")
    else:
        abort(404, "Wrong post id")


@ login_required
@ single_post.route('/post/<int:id>/likes/', methods=['GET'])
def get_who_liked(id):
    limit, page_num = helper_func.set_limit_and_page(request)
    if current_user.is_authenticated:
        wanted_post = SinglePost.query.get(id)
        if wanted_post is not None:
            result = []
            if len(wanted_post.who_liked.all()) is not 0:
                for single_user in wanted_post.who_liked:
                    result.append(single_user.as_dict())
            return jsonify(result), 200
        else:
            abort(404, "Wrong post id")
    abort(400)
