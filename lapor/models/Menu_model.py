from sqlalchemy import text
from ..config.db import db


class Menu(db.Model):
    menu_id = db.Column(db.String(255), primary_key=True, default=text("uuid_short()"))
    restaurant_id = db.Column(db.String(255), db.ForeignKey("restaurant.restaurant_id"))
    menu_name = db.Column(db.String(255), nullable=False)
    highlight = db.Column(db.JSON)
    menu = db.relationship("Restaurant", backref="menu")
