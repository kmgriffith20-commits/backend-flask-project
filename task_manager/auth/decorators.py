
from functools import wraps

import jwt
from flask import current_app, g, jsonify, request


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            return jsonify(message="Missing or invalid token"), 401

        token = auth_header[7:].strip()

        if not token:
            return jsonify(message="Missing or invalid token"), 401

        try:
            payload = jwt.decode(
                token,
                current_app.config["JWT_SECRET_KEY"],
                algorithms=["HS256"],
                options={"require": ["sub", "exp"]},
            )
            g.current_user_id = int(payload["sub"])
        except jwt.ExpiredSignatureError:
            return jsonify(message="Token has expired"), 401
        except (jwt.PyJWTError, ValueError, TypeError, KeyError):
            return jsonify(message="Invalid token"), 401
        
        return f(*args, **kwargs)

    return decorated
