from . import main_bp

@main_bp.route("/")
def index():
    return {"message": "Task Manager API is running"}, 200

@main_bp.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200