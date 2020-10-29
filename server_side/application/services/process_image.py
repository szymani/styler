from threading import Thread
from ..models import single_post_model
# from Fast_lite.fast_algorithm import change_style
from flask import current_app as app
from application import db


class ProcessImage(Thread):
    def __init__(self, id, app_context):
        Thread.__init__(self)
        self.id = id
        self.app_context = app_context

    def run(self):
        with self.app_context.app_context():
            image = single_post_model.SinglePost.query.get(self.id)
            # image.result_image = change_style(image.content_image, image.style_image)
            image.status = 1
            app.logger.info("{Id: " + str(self.id) +
                            " --> Status " + str(image.status) + "}")
            db.session.commit()
