from sqlalchemy.exc import IntegrityError
from ..models import User
from ..extensions import db
from werkzeug.security import generate_password_hash
from flask import Blueprint, jsonify, request

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(
            code="validation_error",
            message="Request body must be a JSON object"
        ), 400

    email = data.get("email")
    password = data.get("password")

    if not isinstance(email, str) or not email.strip():
        return jsonify(
            code="validation_error",
            message="Email is required"
        ), 400

    if not isinstance(password, str) or not password.strip():
        return jsonify(
            code="validation_error",
            message="Password is required"
        ), 400


    if len(email) > 255:
        return jsonify(
            code="validation_error",
            message="Email must be at most 255 characters"
        ), 400

    if len(password) > 255:
        return jsonify(
            code="validation_error",
            message="Password must be at most 255 characters"
        ), 400

    user = User(
        email=email.strip(),
        password_hash=generate_password_hash(password)
    )
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify(
            code="duplicate_email",
            message="Email is already in use"
        ), 409

    return jsonify({
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at.isoformat()
    }), 201
