from flask import request, send_file
from flask import current_app as app
from io import BytesIO

from application import db, ma
from application.models.single_post import SinglePost
from application.services.process_image import ProcessImage
from ..models import user, style

style_paths = {'to_day': 'today.jpg', 'to_night': 'night.jpg'}

# Image Schema
class ImageSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'content_image', 'style_image', 'result_image', 'password', 'style_type', 'status')


class ImagePassSchema(ma.Schema):
    class Meta:
        fields = ('id', 'password', 'status')


# Init schema
image_schema = ImageSchema()
pass_schema = ImagePassSchema()



