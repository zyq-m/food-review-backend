from flask import Blueprint, request, jsonify, json
from ..config.db import db

from ..models.User_model import User

bp = Blueprint("user", __name__)


@bp.get("/user/<username>")
def get_profile(username):
    user = User.query.filter(username=username).first()

    if not user:
        return jsonify({"message": "Not found"}), 404

    return jsonify({"email": user.email, "username": user.username}), 200
