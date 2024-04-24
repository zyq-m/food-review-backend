from ..config.db import db
from sqlalchemy import text


class Review(db.Model):
    review_id = db.Column(
        db.UUID(as_uuid=True),
        default=text("uuid_generate_v4()"),
        primary_key=True,
    )
    restaurant_id = db.Column(db.String(255), db.ForeignKey("restaurant.restaurant_id"))
    email = db.Column(db.String(255), db.ForeignKey("user.email"))
    review_description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default="NOW()")
    review_sentiment = db.Column(db.SmallInteger)
