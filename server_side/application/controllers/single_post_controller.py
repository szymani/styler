from flask import request, send_file, Blueprint, jsonify, make_response
from flask import current_app as app
from flask_login import login_required, logout_user, current_user
from io import BytesIO
import json

from application import db, ma
from ..models import user_model, comment_model, single_post_model
from ..services import helper_func
from ..services.process_image import ProcessImage


single_post = Blueprint('single_post', __name__)


@app.route('/image/custom', methods=['POST'])
def add_custom():
    if request.files['content_image'] is None:
        return "Missing content image", 200
    if request.files['style_image'] is None:
        return "Missing style image", 200

    content_image = request.files['content_image']
    style_image = request.files['style_image']
    # and allowed_file(content_image.filename) and allowed_file(style_image.filename):
    if content_image and style_image:
        new_image = Single_post(content_image=content_image.read(
        ), style_image=style_image.read(), style_type='Custom')
        db.session.add(new_image)
        db.session.commit()
        compute_thread = ProcessImage(new_image, app._get_current_object())
        # compute_thread.start()

        return pass_schema.jsonify(new_image)
    return "Not allowed file", 200


@app.route('/image/<int:id>', methods=['POST'])
def add_pre_style(style_id):  # * Check imput
    if request.files['content_image'] is None:
        return "Missing content image", 200
    content_image = request.files['content_image']
    style_image = open(app.config['STYLE_FOLDER'] + style_paths[style], 'rb')

    if content_image and style_image and allowed_file(
            content_image.filename):  # and allowed_file(style_image.filename):
        new_image = Single_post(content_image=content_image.read(
        ), style_image=style_image.read(), style_type=style)
        # * Start Image Processing in the background
        compute_thread = ProcessImage(new_image)
        compute_thread.start()

        db.session.add(new_image)
        db.session.commit()
        return pass_schema.jsonify(new_image)
    return "Not allowed file", 200


@login_required
@single_post.route('/post/', methods=['POST'])
def add_post_presyle():
    data = request.get_json()
    if data is not None:
        if current_user.is_authenticated:
            try:
                new_post = single_post_model.SinglePost(
                    content_image=data["content_image"],
                    author_id=current_user.id,
                    description=data["description"],
                    style_id=data["style_id"])

                compute_thread = ProcessImage(new_post)
                compute_thread.start()
                db.session.add(new_post)
                db.session.commit()
                return new_post.as_dict(), 200
            except Exception as e:
                print(str(e))
        else:
            abort(401)
    abort(400)


@login_required
@single_post.route('/post/', methods=['POST'])
def add_post_custom():
    data = request.get_json()
    if data is not None:
        if current_user.is_authenticated:
            # TODO Create new style
            id = 0

            try:
                new_post = single_post_model.SinglePost(
                    content_image=data["content_image"],
                    author_id=current_user.id,
                    description=data["description"],
                    style_id=id)
                compute_thread = ProcessImage(new_post)
                compute_thread.start()
                db.session.add(new_post)
                db.session.commit()
                return new_post.as_dict(), 200
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
        wanted_post = single_post_model.SinglePost.query.get(id)
        if wanted_post:
            if current_user.is_authenticated and wanted_post.first().author_id == current_user.id:
                try:
                    wanted_post.update({
                        "description": data["description"],
                        "content_image": data["content_image"]
                    })
                    db.session.commit()
                    return wanted_post.first().as_dict(), 200
                except Exception as e:
                    abort(400)
            else:
                abort(401)
    abort(400)


@ login_required
@ single_post.route('/post/<int:id>', methods=['GET'])
def get_post(id):
    wanted_post = single_post_model.SinglePost.query.get(id)
    if wanted_post is None:
        abort(404, "No post with this id")
    else:
        return wanted_post.as_dict(), 200


@ login_required
@ single_post.route('/user/<int:id>/posts/', methods=['GET'])
def get_posts(id):
    limit, page_num = helper_func.set_limit_and_page(request)
    if current_user.is_authenticated:
        if id is not None:
            try:
                wanted_posts = single_post_model.SinglePost.query.filter(
                    single_post_model.SinglePost.author_id == id).paginate(
                        page=page_num, per_page=limit)
            except:
                return str([]), 200
            if len(wanted_posts.items) is not 0:
                result = []
                for wanted_post in wanted_posts.items:
                    result.append(wanted_post.as_dict())
                return jsonify(result), 200
            else:
                abort(404)
    abort(400)


@ login_required
@ single_post.route('/user/followed/posts/', methods=['GET'])
def get_followed_posts():
    limit, page_num = helper_func.set_limit_and_page(request)
    if current_user.is_authenticated:
        try:
            followed_users = current_user.followed
        except:
            return str([]), 200
        result = []
        for followed_user in followed_users:
            if len(followed_user.posts) is not 0:
                for single_post in followed_user.posts:
                    result.append(single_post.as_dict())
        return jsonify(result), 200
    abort(400)


@ login_required
@ single_post.route('/post/<int:id>', methods=['DELETE'])
def delete_post(id):
    if id is not None:
        wanted_post = single_post_model.SinglePost.query.get(id)
        if wanted_post:
            if current_user.is_authenticated and (
                    current_user.id == wanted_post.author_id
                    or current_user.user_type == 1):
                db.session.delete(single_post_model.SinglePost.query.get(id))
                db.session.commit()
                return wanted_post.as_dict(), 200
            else:  # restricted access to somebody else
                abort(401)
        abort(404, "No post with this id")
    abort(400)


@ login_required
@ single_post.route('/post/<int:id>/like', methods=['PUT'])
def like_post(id):
    wanted_post = single_post_model.SinglePost.query.get(id)
    if wanted_post is not None:
        if wanted_post.who_liked.filter(user_model.User.id == current_user.id).first() is None:
            wanted_post.who_liked.append(current_user)
            wanted_post.upvotes = wanted_post.upvotes + 1
            db.session.commit()
            return wanted_post.as_dict(), 200
        else:
            abort(400, "Already liked")
    else:
        abort(404, "Wrong post id")


@ login_required
@ single_post.route('/post/<int:id>/unlike', methods=['PUT'])
def unlike_post(id):
    wanted_post = single_post_model.SinglePost.query.get(id)
    if wanted_post is not None:
        if wanted_post.who_liked.filter(user_model.User.id == current_user.id).first() is not None:
            wanted_post.who_liked.remove(current_user)
            wanted_post.upvotes = wanted_post.upvotes - 1
            db.session.commit()
            return wanted_post.as_dict(), 200
        else:
            abort(400, "Not liked yet")
    else:
        abort(404, "Wrong post id")


@ login_required
@ single_post.route('/post/<int:id>/likes/', methods=['GET'])
def get_who_liked(id):
    limit, page_num = helper_func.set_limit_and_page(request)
    if current_user.is_authenticated:
        wanted_post = single_post_model.SinglePost.query.get(id)
        if wanted_post is not None:
            result = []
            if len(wanted_post.who_liked.all()) is not 0:
                for single_user in wanted_post.who_liked:
                    result.append(single_user.as_dict())
            return jsonify(result), 200
        else:
            abort(404, "Wrong post id")
    abort(400)
