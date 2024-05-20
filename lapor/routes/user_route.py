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

    # upload file
    if request.files:
        file = request.files["avatar"]

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            path = current_app.config["PROFILE_PATH"]
            act_path = os.path.join("lapor", path)
            img_path = os.path.join(path, filename)
            img_path_to_save = os.path.join(act_path, filename)

            # check dir exist
            if not os.path.exists(act_path):
                os.makedirs(act_path)

            # check file exist
            if user.avatar:
                old_file = os.path.join("lapor", user.avatar["src"])
                os.remove(old_file)

            file.save(img_path_to_save)

            user.avatar = {"src": img_path}
            db.session.commit()

            return jsonify(
                {
                    "message": "Profile avatar updated successfully",
                    "avatar": user.avatar,
                }
            )

    if not user:
        return jsonify({"message": "Not found"}), 404

    if request.data:
        data = json.loads(request.data)
        user.email = data["email"]
        user.name = data["name"]
        db.session.commit()

    return jsonify({"message": "Profile updated", "user": user_schema.dump(user)}), 200


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
