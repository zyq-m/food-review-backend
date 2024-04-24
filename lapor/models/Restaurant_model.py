from ..config.db import db


class Restaurant(db.Model):
    restaurant_id = db.Column(db.String(255), primary_key=True)
    email = db.Column(db.String(255), db.ForeignKey("user.email"))
    restaurant_name = db.Column(db.String(255))
    description = db.Column(db.Text)
    category = db.Column(db.String(255))
    restaurant_open = db.Column(db.String(255))
    location = db.Column(db.Text)
    phone_no = db.Column(db.String(12))
    website_link = db.Column(db.Text)
    restaurant_img = db.Column(db.JSON)
    positive_review = db.Column(db.Integer)
    negative_review = db.Column(db.Integer)
    total_review = db.Column(db.Integer)
