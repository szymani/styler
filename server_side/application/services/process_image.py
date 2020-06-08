from threading import Thread
from application.models.single_post_model import SinglePost
# from Fast_lite.fast_algorithm import change_style
from flask import current_app as app
from application import db


class ProcessImage(Thread):
    def __init__(self, data, app_context):
        Thread.__init__(self)
        self.data = data
        self.app_context = app_context

    def run(self):
        with self.app_context.app_context():
            image = Single_post.query.get(self.data.id)
            # image.result_image = change_style(image.content_image, image.style_image)
            image.status = 1
            app.logger.info("{Id: " + str(self.data.id) +
                            " --> Status " + str(image.status) + "}")
            db.session.commit()
