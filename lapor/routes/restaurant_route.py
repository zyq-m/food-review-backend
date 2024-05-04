from flask import Blueprint, request, jsonify, json
from ..config.db import db
from ..schema.Restaurant_schema import restaurant_schema, restaurants_schema

from ..models.Restaurant_model import Restaurant

bp = Blueprint("restaurant", __name__)


@bp.get("/restaurant/<id>")
def get_restaurant_by_id(id):
    restaurant = Restaurant.query.filter_by(restaurant_id=id).first()

    if not restaurant:
        return jsonify({"message": "Not found"}), 404

    return jsonify({"restaurant": restaurant_schema.dump(restaurant)}), 200


@bp.get("/restaurant")
def get_restaurant():
    restaurant = Restaurant.query.all()

    if not restaurant:
        return jsonify({"message": "Not found"}), 404

    return jsonify({"restaurant": restaurants_schema.dump(restaurant)}), 200


@bp.get("/restaurant/category/<category>")
def get_restaurant_category(category):
    restaurant = Restaurant.query.filter(Restaurant.category == category).first()

    if not restaurant:
        return jsonify({"message": "Not found"}), 404

    return jsonify({restaurant: restaurants_schema.dump(restaurant)}), 200


@bp.get("/restaurant/query/<name>")
def get_restaurant_by_name(name):
    restaurant = Restaurant.query.filter(Restaurant.restaurant_name.like(f"%{name}%"))

    if not restaurant:
        return jsonify({"message": "Not found"}), 404

    return jsonify({restaurant: restaurants_schema.dump(restaurant)}), 200
