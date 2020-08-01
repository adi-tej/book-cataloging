from flask import make_response, jsonify

from .. import db, flask_bcrypt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class User(db.Model):
    """ User Model for storing user information """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    opshop_id = db.Column(db.Integer, db.ForeignKey('opshop.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100))

    def encrypt_password(self, password):
        self.password = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return "<User '{}'>".format(self.name)
