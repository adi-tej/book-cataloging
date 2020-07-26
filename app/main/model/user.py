from flask import make_response, jsonify

from .. import db, flask_bcrypt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class User(db.Model):
    """ User Model for storing user information """
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    opshop_id = db.Column(db.Integer, db.ForeignKey('opshop.opshop_id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), nullable=False)
    register_email = db.Column(db.String(50), unique=True, nullable=False)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100))

    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User '{}'>".format(self.user_name)
