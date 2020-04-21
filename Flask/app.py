from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from random import randrange
from threading import Thread
from werkzeug.utils import secure_filename
import copy
import time
import os
from io import BytesIO

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
style_paths = {'to_day': 'today.jpg', 'to_night': 'night.jpg'}
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = basedir + '/static/images/'
app.config['STYLE_FOLDER'] = basedir + '/static/styles/'
db = SQLAlchemy(app)
ma = Marshmallow(app)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Image Class/Model
class Image(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=False)
  content_image = db.Column(db.LargeBinary)
  style_image = db.Column(db.LargeBinary)
  result_image = db.Column(db.LargeBinary)
  password = db.Column(db.Integer)
  style_type = db.Column(db.String(200))
  status = db.Column(db.Integer)

  def __init__(self, content_image, style_type, name='Default name', password='123123', style_image=None):
    self.name = name
    self.content_image = content_image
    self.style_image = style_image
    self.result_image = None
    # self.password = randrange(10000000)
    self.password = password
    self.style_type = style_type
    self.status = 0


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

class ProcessImage(Thread):
  def __init__(self, data):
    Thread.__init__(self)
    self.data = data

  def run(self):
    time.sleep(3)
    # TODO Process the image
    # TODO Apply style transfer

    image = Image.query.get(self.data.id)
    image.status = 1
    image.result_image = image.style_image
    app.logger.info("{Id: " + str(self.data.id) + " --> Status " + str(image.status) + "}")
    db.session.commit()


@app.route('/image/custom', methods=['POST'])
def add_custom():
  #* Check imput
  if request.files['content_image'] is None: return "Missing content image", 200
  if request.files['style_image'] is None: return "Missing style image", 200

  content_image = request.files['content_image']
  style_image = request.files['style_image']
  if content_image and style_image and allowed_file(content_image.filename) and allowed_file(style_image.filename):
    new_image = Image(content_image=content_image.read(), style_image=style_image.read(), style_type='Custom')
    #* Start Image Processing in the background
    compute_thread = ProcessImage(new_image)
    compute_thread.start()

    db.session.add(new_image)
    db.session.commit()
    return pass_schema.jsonify(new_image)
  return "Not allowed file", 200


@app.route('/image/prestyle/<style>', methods=['POST'])
def add_pre_style(style):  #* Check imput
  if request.files['content_image'] is None: return "Missing content image", 200
  content_image = request.files['content_image']
  style_image = open(app.config['STYLE_FOLDER'] + style_paths[style],'rb')

  if content_image and style_image and allowed_file(content_image.filename):# and allowed_file(style_image.filename):
    new_image = Image(content_image=content_image.read(), style_image=style_image.read(), style_type=style)
    #* Start Image Processing in the background
    compute_thread = ProcessImage(new_image)
    compute_thread.start()

    db.session.add(new_image)
    db.session.commit()
    return pass_schema.jsonify(new_image)
  return "Not allowed file", 200


@app.route('/image/<int:id>', methods=['GET'])
def get_image(id):
  result_image = Image.query.get(id)
  if result_image is None:
    return "No image with this id", 200-
  else:
    if request.args.get('password') == str(result_image.password):
      if result_image.status == 0:
        return "Image not ready", 200
      elif result_image.status == -1:
        return "There have been an error", 200
      #? Delete the file after or not?
      return send_file(BytesIO(result_image.result_image), attachment_filename="test.png"), 200
    else:
      return "Wrong password", 200

@app.route('/styles/', methods=['GET'])
def get_styles():
  styles = style_paths.keys()
  return '[' + ', '.join(map(str, styles)) + ']', 200


@app.route('/image/ids', methods=['GET'])
def get_ids():
  ids = db.session.query(Image.id).all()
  ids = [value for value, in ids]
  return ' '.join(map(str, ids)), 200


@app.route('/image/<int:id>', methods=['DELETE'])
def delete_image(id):
  image = Image.query.get(id)
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


# Run Server
if __name__ == '__main__':
  app.run(debug=True)
