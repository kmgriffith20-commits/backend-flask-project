from http import HTTPStatus

from werkzeug.exceptions import HTTPException


ERROR_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "method_not_allowed",
    500: "internal_error",
}


def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_error(exc):
        status = exc.code or 500
        if status >= 500:
            code = ERROR_CODES.get(status, "internal_error")
            message = "An internal server error occurred."
        else:
            code = ERROR_CODES.get(status, f"http_{status}")
            message = HTTPStatus(status).phrase

        response = exc.get_response()
        response.set_data(app.json.dumps({"error": code, "message": message}))
        response.content_type = "application/json"
        return response