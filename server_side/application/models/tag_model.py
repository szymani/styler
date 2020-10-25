from application import db


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def as_dict(self):
        return {
            c.name: str(getattr(self, c.name))
            for c in self.__table__.columns if c.name != "password"
        }

    def __repr__(self):
        return '<User {}>'.format(self.login)
