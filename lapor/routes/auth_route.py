from flask import Blueprint, request, jsonify, json
from ..config.db import db

# model
from ..models.Role_model import Role
from ..models.User_model import User
from ..models.Restaurant_model import Restaurant

bp = Blueprint("auth", __name__)


@bp.post("/sign-up")
def sign_up_user():
    # require email and password
    data = json.loads(request.data)

    # do validation
    user = User(
        email=data["email"], user_name=data["username"], password=data["password"]
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Successfully created"}), 201


@bp.post("/sign-up/restaurant")
def sign_up_restaurant():
    # require email and password
    data = json.loads(request.data)

    # do validation
    user = User(
        email=data["email"],
        user_name=data["username"],
        password=data["password"],
        role_id=2,
    )
    db.session.add(user)
    db.session.commit()

    restaurant = Restaurant(
        email=user.email,
        restaurant_name=data["restaurant_name"],
        category=data["category"],
        phone_no=data["phone_no"],
    )
    db.session.add(restaurant)
    db.session.commit()

    return jsonify({"message": "Successfully created"}), 201


@bp.post("/login")
def login():
    data = json.loads(request.data)

    user = User.query.filter_by(email=data["email"], password=data["password"]).first()

    if not user:
        return jsonify({"message": "Invalid credentials"}), 404

    # do role assignment, token creation and authorization

    return jsonify({"status": "created"}), 200


# @bp.delete("/logout")
