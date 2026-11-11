from . import main_bp

@main_bp.route("/")
def index():
    return {"message": "Task Manager API is running"}, 200
