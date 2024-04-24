from flask import Blueprint, request, jsonify, json
from ..config.db import db

from ..models.Restaurant_model import Restaurant

bp = Blueprint("restaurant", __name__)


@bp.get("/restaurant/<id>")
def get_restaurant_by_id(id):
    restaurant = Restaurant.query.filter_by(restaurant_id=id).first()

    if not restaurant:
        return jsonify({"message": "Not found"}), 404

    return jsonify(restaurant), 200


@bp.get("/restaurant")
def get_restaurant():
    restaurant = Restaurant.query.all()

    if not restaurant:
        return jsonify({"message": "Not found"}), 404

    return jsonify(restaurant), 200
