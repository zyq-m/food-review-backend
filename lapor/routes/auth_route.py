from flask import Blueprint, request, jsonify, json
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    create_refresh_token,
)

from ..config.db import db

# model
from ..models.Role_model import Role
from ..models.User_model import User
from ..models.Restaurant_model import Restaurant

# schema
from ..schema.User_schema import user_schema

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
    try:
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
    except IntegrityError as err:
        db.session.rollback()
        print(err)

        return jsonify({"message": "Account existed"}), 500
    except SQLAlchemyError as err:
        db.session.rollback()
        print(err)

        return jsonify({"message": "Error"}), 500


@bp.post("/login")
def login():
    data = json.loads(request.data)

    user = User.query.filter_by(email=data["email"], password=data["password"]).first()

    if not user:
        return jsonify({"message": "Invalid credentials"}), 404

    # do role assignment, token creation and authorization
    access_token = create_access_token(identity=user_schema.dump(user))
    refresh_token = create_refresh_token(identity=user_schema.dump(user))
    return jsonify(access_token=access_token, refresh_token=refresh_token)


# @bp.delete("/logout")


@bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)
