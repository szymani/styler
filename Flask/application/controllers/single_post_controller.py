from flask import request, send_file
from flask import current_app as app
from io import BytesIO

from application import db, ma
from application.models.single_post import SinglePost
from application.services.process_image import ProcessImage
from ..models import user, style


@app.route('/image/custom', methods=['POST'])
def add_custom():
    if request.files['content_image'] is None: return "Missing content image", 200
    if request.files['style_image'] is None: return "Missing style image", 200

    content_image = request.files['content_image']
    style_image = request.files['style_image']
    if content_image and style_image: # and allowed_file(content_image.filename) and allowed_file(style_image.filename):
        new_image = Single_post(content_image=content_image.read(), style_image=style_image.read(), style_type='Custom')
        db.session.add(new_image)
        db.session.commit()
        compute_thread = ProcessImage(new_image, app._get_current_object())
        compute_thread.start()

        return pass_schema.jsonify(new_image)
    return "Not allowed file", 200


@app.route('/image/prestyle/<style>', methods=['POST'])
def add_pre_style(style):  # * Check imput
    if request.files['content_image'] is None: return "Missing content image", 200
    content_image = request.files['content_image']
    style_image = open(app.config['STYLE_FOLDER'] + style_paths[style], 'rb')

    if content_image and style_image and allowed_file(
            content_image.filename):  # and allowed_file(style_image.filename):
        new_image = Single_post(content_image=content_image.read(), style_image=style_image.read(), style_type=style)
        # * Start Image Processing in the background
        compute_thread = ProcessImage(new_image)
        compute_thread.start()

        db.session.add(new_image)
        db.session.commit()
        return pass_schema.jsonify(new_image)
    return "Not allowed file", 200


@app.route('/image/<int:id>', methods=['GET'])
def get_image(id):
    result_image = Single_post.query.get(id)
    if result_image is None:
        return "No image with this id", 200
    else:
        if request.args.get('password') == str(result_image.password):
            if result_image.status == 0:
                return "Image not ready", 200
            elif result_image.status == -1:
                return "There have been an error", 200
            return send_file(BytesIO(result_image.result_image), attachment_filename="test.png"), 200
        else:
            return "Wrong password", 200


@app.route('/styles/', methods=['GET'])
def get_pre_styles():
    styles = style_paths.keys()
    return '[' + ', '.join(map(str, styles)) + ']', 200


@app.route('/image/ids', methods=['GET'])
def get_ids():
    ids = db.session.query(Single_post.id).all()
    ids = [value for value, in ids]
    return ' '.join(map(str, ids)), 200


@app.route('/image/<int:id>', methods=['DELETE'])
def delete_image(id):
    image = Single_post.query.get(id)
    if image is not None:
        if request.args.get('password') == str(image.password):
            if image.status is not 0:
                db.session.delete(image)
                db.session.commit()
                return send_file(BytesIO(image.result_image), attachment_filename="test.png"), 200
            else:
                return "Image is still being processed", 200
        else:
            return "Wrong password", 200
    else:
        return "No image with this id", 200