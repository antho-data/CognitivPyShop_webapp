"""Data models."""
from sqlalchemy import event
from werkzeug.security import generate_password_hash
from . import db
from flask_login import UserMixin

hashed_password = generate_password_hash("admin", method='sha256')

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False, unique=True)
    active = db.Column(db.Boolean())
    admin = db.Column(db.Boolean())

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Predictions(db.Model):
    __tablename__ = "classes"
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(400), nullable=False)
    sentence = db.Column(db.String(400), nullable=False)
    label1 = db.Column(db.Float, nullable=False)
    label2 = db.Column(db.Float, nullable=False)
    label3 = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Sentence {}>'.format(self.sentence)


@event.listens_for(User.__table__, 'after_create')
def init_admin_user(*args, **kwargs):
    db.session.add(User(username='superadmin', email='admin@domain.com', password=hashed_password, active=1, admin=1))
    db.session.commit()
