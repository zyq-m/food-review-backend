from uuid import uuid1
from flask import Blueprint, json, request, jsonify
from flask_jwt_extended import (
    jwt_required,
)

from ..schema.Restaurant_schema import restaurant_schema, restaurants_schema
from ..config.db import db
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
    name = args.get("restaurant")

    if category and name is not None:
        restaurant = Restaurant.query.filter(
            Restaurant.category == category, Restaurant.restaurant_img == name
        ).all()

    if category is not None:
        restaurant = Restaurant.query.filter(Restaurant.category == category).all()

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

    category = [{"id": uuid1(), "name": "all"}]
    for item in query:
        category.append({"id": uuid1(), "name": item.category})

    return jsonify(category=category), 200


@bp.get("/my-restaurant/<email>")
@jwt_required()
def get_my_restaurant(email):
    restaurant = Restaurant.query.filter_by(email=email).first()
    restaurant = restaurant_schema.dump(restaurant)

    if not restaurant:
        return jsonify({"message": "Not found"}), 404

    return jsonify({"restaurant": restaurant}), 200


@bp.put("/my-restaurant/<email>")
@jwt_required()
def update_restaurant(email):
    data = json.loads(request.data)
    restaurant = Restaurant.query.filter_by(email=email).first()

    if not restaurant:
        return jsonify({"message": "Not found"}), 404

    restaurant.restaurant_name = data["restaurant_name"]
    restaurant.category = data["category"]
    restaurant.phone_no = data["phone_no"]
    restaurant.website_link = data["website_link"]
    restaurant.location = data["location"]
    restaurant.description = data["description"]

    db.session.commit()

    return jsonify({"message": "Success"}), 200
