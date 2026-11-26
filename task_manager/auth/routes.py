from flask import current_app
from datetime import datetime, timedelta, timezone
import jwt
from werkzeug.security import check_password_hash
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

@auth_bp.route("/login", methods=["POST"])
def login():
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

    user = User.query.filter_by(email=email.strip()).first()

    if user is None or not check_password_hash(user.password_hash, password):
        return jsonify(message="Invalid email or password"), 401

    secret = current_app.config["JWT_SECRET_KEY"]
    lifetime = current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]

    if not secret:
        return jsonify(message="JWT configuration missing"), 500

    payload = {
        "sub": str(user.id),
        "role": "user",
        "exp": datetime.now(timezone.utc) + timedelta(seconds=lifetime)
    }

    token = jwt.encode(payload, secret, algorithm="HS256")
    return jsonify(access_token=token), 200

from .decorators import token_required
from flask import g

@auth_bp.route("/me", methods=["GET"])
@token_required
def me():
    return jsonify(user_id=g.current_user_id), 200

@auth_bp.route("/api/profile", methods=["GET"])
@token_required
def get_profile():
    user_id = g.current_user_id
    user = User.query.get(user_id)

    if user is None:
        return jsonify(message="User not found"), 404

    return jsonify(
        id=user.id,
        email=user.email
    ), 200

@auth_bp.route("/api/profile", methods=["PATCH"])
@token_required
def update_profile():
    user = User.query.get(g.current_user_id)

    if user is None:
        return jsonify(message="User not found"), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(message="Valid JSON is required"), 400

    if set(data.keys()) != {"email"}:
        return jsonify(message="Only email can be updated"), 400

    email = data["email"]

    if not isinstance(email, str):
        return jsonify(message="Email must be a string"), 400

    email = email.strip().lower()

    if not email or "@" not in email or "." not in email.split("@")[-1]:
        return jsonify(message="Invalid email address"), 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user and existing_user.id != user.id:
        return jsonify(message="Email already registered"), 409

    user.email = email
    db.session.commit()

    return jsonify(id=user.id, email=user.email), 200

@auth_bp.route("/api/admin/ping", methods=["GET"])
@token_required
def admin_ping():
    user = User.query.get(g.current_user_id)

    if user is None:
        return jsonify(message="User not found"), 401

    if user.role != "admin":
        return jsonify(message="Admin access required"), 403

    return jsonify(message="Admin access granted"), 200
