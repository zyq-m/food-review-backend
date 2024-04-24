from flask import Blueprint, request, jsonify, json
from ..config.db import db

from ..models.Review_model import Review
from ..models.User_model import User

bp = Blueprint("review", __name__)


# restaurant can view their feedbacks from customers
@bp.get("/restaurant/<id>/review")
def get_restaurant_reviews(id):
    review = Review.query.filter_by(restaurant_id=id).all()

    if not review:
        return jsonify({"message": "Not found"}), 404

    return jsonify(review), 200


# user can view feedbacks made towards restaurant
@bp.get("/user/<username>/review")
def get_user_reviews(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    review = Review.query.filter_by(email=user.email)

    if not review:
        return jsonify({"message": "Not found"}), 404

    return jsonify(review), 200


@bp.post("/review")
def create_review():
    data = json.loads(request.data)

    review = Review(
        restaurant_id=data["restaurant_id"],
        email=data["email"],
        review_description=data["review"],
    )
    db.session.add(review)
    db.session.commit()

    return jsonify({"message": "Review successfully submited"}), 201


@bp.put("/review/edit/<id>")
def edit_review(id):
    data = json.loads(request.data)
    review = Review.query.filter_by(review_id=id).first()

    if not review:
        return jsonify({"message": "Not found"}), 404

    review = data["edited_review"]
    db.session.commit()

    return jsonify({"message": "Review successfully updated"}), 200


@bp.put("/review/delete/<id>")
def delete_review(id):
    review = Review.query.filter_by(review_id=id).first()

    if not review:
        return jsonify({"message": "Not found"}), 404

    db.session.delete(review)
    db.session.commit()

    return jsonify({"message": "Review successfully remove"}), 200
