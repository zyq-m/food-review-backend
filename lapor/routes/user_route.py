import os
from flask import (
    Blueprint,
    current_app,
    request,
    jsonify,
    json,
)
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename

from ..config.db import db
from ..schema.User_schema import user_schema
from ..models.User_model import User

bp = Blueprint("user", __name__)

ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}


@bp.get("/user/profile/<username>")
@jwt_required()
def get_profile(username):
    user = User.query.filter_by(user_name=username).first()

    if not user:
        return jsonify({"message": "Not found"}), 404

    return jsonify({"user": user_schema.dump(user)}), 200


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.put("/user/profile/<username>")
@jwt_required()
def update_profile(username):
    user = User.query.filter_by(user_name=username).first()

    if request.files:
        file = request.files["avatar"]

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            profile_path = current_app.config["PROFILE_PATH"]
            file_to_save = os.path.join(profile_path, filename)

            # check dir exist
            if not os.path.exists(profile_path):
                os.makedirs(profile_path)

            # check file exist
            if user.avatar:
                old_file = os.path.join(user.avatar["src"])
                os.remove(old_file)

            file.save(file_to_save)

            user.avatar = {"src": file_to_save}
            db.session.commit()

            return jsonify({"message": "Profile avatar updated successfully"})

    if not user:
        return jsonify({"message": "Not found"}), 404

    if request.data:
        data = json.loads(request.data)
        user.email = data["email"]
        db.session.commit()

    return jsonify({"message": "Profile updated"}), 200


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
