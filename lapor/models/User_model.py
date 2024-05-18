from ..config.db import db


class User(db.Model):
    email = db.Column(db.String(255), primary_key=True)
    role_id = db.Column(
        db.Integer, db.ForeignKey("role.role_id"), default=1
    )  # 1 = user
    user_name = db.Column(db.String(12))
    avatar = db.Column(db.JSON)
    password = db.Column(db.Text)
    active = db.Column(db.SmallInteger, default=1)
