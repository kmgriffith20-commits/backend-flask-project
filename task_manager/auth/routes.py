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

    return jsonify({"email": email}), 201
