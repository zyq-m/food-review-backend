from ..config.db import db


class Token(db.Model):
    token_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), db.ForeignKey("user.email"))
    token_value = db.Column(db.Text, nullable=False)
