from uuid import uuid1
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    jwt_required,
)

from ..schema.Restaurant_schema import restaurant_schema, restaurants_schema

from ..models.Restaurant_model import Restaurant

bp = Blueprint("restaurant", __name__)


@bp.get("/restaurant/<id>")
@jwt_required()
def get_restaurant_by_id(id):
    restaurant = Restaurant.query.filter_by(restaurant_id=id).first()

    reviews = []
    for item in restaurant.reviews:
        reviews.append(
            {
                "review_id": item.review_id,
                "email": item.email,
                "review_description": item.review_description,
                "timestamp": item.timestamp,
                "review_sentiment": item.review_sentiment,
            }
        )

    restaurant = restaurant_schema.dump(restaurant)
    restaurant.update({"reviews": reviews})

    if not restaurant:
        return jsonify({"message": "Not found"}), 404

    return jsonify({"restaurant": restaurant}), 200


@bp.get("/restaurant")
@jwt_required()
def get_restaurant():
    restaurant = Restaurant.query.all()

    if not restaurant:
        return jsonify({"message": "Not found"}), 404

    return jsonify({"restaurant": restaurants_schema.dump(restaurant)}), 200


@bp.get("/restaurant/search")
@jwt_required()
def get_restaurant_by_query():
    args = request.args
    category = args.get("category")
    name = args.get("name")

    if category and name is not None:
        restaurant = Restaurant.query.filter(
            Restaurant.category == category, Restaurant.restaurant_img == name
        ).all()

    if category is not None:
        restaurant = Restaurant.query.filter(Restaurant.category == category).all()

    if category is not None and category == "all":
        restaurant = Restaurant.query.all()

    if name is not None:
        restaurant = Restaurant.query.filter(
            Restaurant.restaurant_name.like(f"%{name}%")
        ).all()

    if not restaurant:
        return jsonify({"message": "Not found"}), 404

    return jsonify({"restaurant": restaurants_schema.dump(restaurant)}), 200


@bp.get("/restaurant/category")
@jwt_required()
def get_restaurant_category():
    query = (
        Restaurant.query.add_column(Restaurant.category)
        .with_entities(Restaurant.category)
        .group_by(Restaurant.category)
        .all()
    )

    if query is None:
        return jsonify({"message": "Catergory not available"})

    category = []
    for item in query:
        category.append({"id": uuid1(), "name": item.category})

    return jsonify(category=category), 200
