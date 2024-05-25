from ..config.db import db
from sqlalchemy import text


class Restaurant(db.Model):
    restaurant_id = db.Column(
        db.String(255), primary_key=True, default=text("uuid_short()")
    )
    email = db.Column(db.String(255), db.ForeignKey("user.email"))
    restaurant_name = db.Column(db.String(255))
    description = db.Column(db.Text)
    category = db.Column(db.String(255))
    restaurant_open = db.Column(db.String(255))
    location = db.Column(db.Text)
    phone_no = db.Column(db.String(12))
    website_link = db.Column(db.Text)
    restaurant_img = db.Column(db.JSON)
    highlight = db.Column(db.JSON)
    menu_img = db.Column(db.JSON)
    positive_review = db.Column(db.Integer)
    negative_review = db.Column(db.Integer)
    total_review = db.Column(db.Integer)

    reviews = db.relationship("Review", backref="restaurant")
