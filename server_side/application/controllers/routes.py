from flask import request, send_file
from flask import current_app as app
from application import db, ma

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



