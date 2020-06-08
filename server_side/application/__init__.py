from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_cors import CORS

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()


def create_app(testing=False):
    app = Flask(__name__, instance_relative_config=False)
    CORS(app)
    if testing is False:
        app.config.from_object('config.Config')
    else:
        app.config.from_object('config.TestConfig')

    db.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from application.controllers import routes, user_controller, comment_controller, auth_controller, single_post_controller, style_controller, messages_controller
        from application.errors import errors
        app.register_blueprint(auth_controller.auth)
        app.register_blueprint(user_controller.user)
        app.register_blueprint(comment_controller.comment)
        app.register_blueprint(single_post_controller.single_post)
        app.register_blueprint(messages_controller.message)
        app.register_blueprint(style_controller.style)
        app.register_blueprint(errors.error_handlers)
        try:
            db.create_all()  # Create database tables for our data models
        except:  # If database already exists there might be some errors
            pass
        return app
