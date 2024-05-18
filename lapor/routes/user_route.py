from flask import Blueprint, request, jsonify, json
from flask_jwt_extended import jwt_required

from ..config.db import db
from ..schema.User_schema import user_schema
from ..models.User_model import User

bp = Blueprint("user", __name__)


@bp.get("/user/profile/<username>")
@jwt_required()
def get_profile(username):
    user = User.query.filter(username == username).first()

    if not user:
        return jsonify({"message": "Not found"}), 404

    return jsonify({"user": user_schema.dump(user)}), 200


@bp.put("/user/profile/<username>")
@jwt_required()
def update_profile(username):
    data = json.loads(request.data)
    user = User.query.filter(username == username).first()

    if not user:
        return jsonify({"message": "Not found"}), 404

    user.email = data["email"]

    return jsonify({"message": "Updated"}), 200


@bp.put("/user/password")
@jwt_required()
def change_password():
    data = json.loads(request.data)

    user = User.query.filter_by(email=data["email"], password=data["password"]).first()
    user.password = data["new_password"]

    db.session.commit()

    if not user:
        return jsonify({"message": "Invalid password"}), 404

    return jsonify({"message": "Password changed"}), 200
