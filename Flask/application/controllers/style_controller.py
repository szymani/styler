from flask import request, send_file
from flask import current_app as app
from io import BytesIO

from application import db, ma
from ..models import user, style


@app.route('/style/add', methods=['POST'])
def add_style():
    data = request.get_json()
    if data is not None:
        new_style = style.Style(author_id=data["id"], ifprivate=data["ifprivate"], style_image=None, description="test style 1",)
        db.session.add(new_style)
        db.session.commit()
        return str(new_style.style_author_id)
    return "Empty request", 200

@app.route('/style/<int:id>', methods=['GET'])
def get_style(id):
    if id is not None:
        wanted_style = style.Style.query.get(id)
        if wanted_style is not None:
            if wanted_style.style_author.id == request.get_json()["user_id"]:
                return wanted_style.style_author.login
            return "You don't have permission to view this style", 200
        return "No style with this id", 200
    return "Empty request", 200

@app.route('/style/', methods=['GET'])
def get_styles():
    data = request.get_json()
    if data is not None:
        styles = user.User.query.get(data["user_id"]).author_of_styles
        if styles is not None:

            print(styles[0].id)
            return ' '.join(map(str, styles)), 200
        return "No styles", 200
    return "Empty request", 200