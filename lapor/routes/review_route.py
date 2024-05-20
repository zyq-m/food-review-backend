from datetime import datetime
from flask import Blueprint, request, jsonify, json
from flask_jwt_extended import jwt_required
from ..config.db import db
from sqlalchemy import exc

from ..models.Review_model import Review
from ..models.User_model import User
from ..schema.Review_schema import reviews_schema

bp = Blueprint("review", __name__)


# restaurant can view their feedbacks from customers
@bp.get("/restaurant/<id>/review")
@jwt_required()
def get_restaurant_reviews(id):
    review = Review.query.filter_by(restaurant_id=id).all()

    if not review:
        return jsonify({"message": "Not found"}), 404

    return jsonify(reviews_schema.dump(review)), 200


# user can view feedbacks made towards restaurant
@bp.get("/user/<username>/review")
@jwt_required()
def get_user_reviews(username):
    user = User.query.filter_by(user_name=username).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    review = Review.query.filter_by(email=user.email).all()

    if not review:
        return jsonify({"message": "Not found"}), 404

    return jsonify({"review": reviews_schema.dump(review)}), 200


@bp.post("/review")
@jwt_required()
def create_review():
    data = json.loads(request.data)

    try:
        review = Review(
            restaurant_id=data["restaurant_id"],
            email=data["email"],
            review_description=data["review"],
            timestamp=datetime.now(),
        )

        db.session.add(review)
        db.session.commit()

        return jsonify(
            {
                "message": "Review successfully submited",
            }
        ), 201
    except exc.IntegrityError:
        return jsonify(
            {
                "message": "You only can submit 1 review on each restaurant",
            }
        ), 400


@bp.put("/review/edit/<id>")
@jwt_required()
def edit_review(id):
    data = json.loads(request.data)
    review = Review.query.filter_by(review_id=id).first()

    if not review:
        return jsonify({"message": "Not found"}), 404

    review.review_description = data["edited_review"]
    db.session.commit()

    return jsonify({"message": "Review successfully updated"}), 200


@bp.delete("/review/delete/<id>")
@jwt_required()
def delete_review(id):
    review = Review.query.filter_by(review_id=id).first()

    if not review:
        return jsonify({"message": "Not found"}), 404

    db.session.delete(review)
    db.session.commit()

    return jsonify({"message": "Review successfully remove"}), 200
