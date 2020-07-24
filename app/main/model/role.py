
# from .. import db
#
# class Role(db.Model):
#     __tablename__ = 'role'
#     role_id = db.Column(db.Integer, primary_key=True)
#     role_name = db.Column(db.String(20))
#     users = db.relationship('User', backref='role', lazy='dynamic')