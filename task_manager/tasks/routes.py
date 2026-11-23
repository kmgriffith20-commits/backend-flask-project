from datetime import date

from flask import Blueprint, g, jsonify, request

from ..auth.decorators import token_required
from ..extensions import db
from ..models import Task, User

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.post("/tasks")
@token_required
def create_task():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="validation_error", message="Expected a JSON object"), 400

    title = data.get("title")
    if not isinstance(title, str) or not 1 <= len(title.strip()) <= 120:
        return jsonify(
            error="validation_error",
            message="Title must be between 1 and 120 characters",
        ), 400

    description = data.get("description")
    if description is not None and not isinstance(description, str):
        return jsonify(
            error="validation_error", message="Description must be a string or null"
        ), 400

    status = data.get("status", "pending")
    if status not in ("pending", "in_progress", "done"):
        return jsonify(
            error="validation_error",
            message="Status must be pending, in_progress, or done",
        ), 400

    due_date = data.get("due_date")
    if due_date is not None:
        try:
            parsed_date = date.fromisoformat(due_date)
            if parsed_date.isoformat() != due_date:
                raise ValueError
        except (TypeError, ValueError):
            return jsonify(
                error="validation_error", message="Due date must use YYYY-MM-DD"
            ), 400
        due_date = parsed_date

    if db.session.get(User, g.current_user_id) is None:
        return jsonify(error="unauthorized", message="User account not found"), 401

    task = Task(
        title=title.strip(),
        description=description,
        status=status,
        due_date=due_date,
        user_id=g.current_user_id,
    )
    db.session.add(task)
    db.session.commit()

    return jsonify(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        status=task.status,
        due_date=task.due_date.isoformat() if task.due_date else None,
        created_at=task.created_at.isoformat(),
        updated_at=task.updated_at.isoformat(),
    ), 201

@tasks_bp.get("/tasks")
@token_required
def list_tasks():
    query = db.select(Task).where(Task.user_id == g.current_user_id)
    tasks = db.session.scalars(query).all()

    return jsonify([
        {
            "id": task.id,
            "user_id": task.user_id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat(),
        }
        for task in tasks
    ]), 200

@tasks_bp.get("/tasks/<int:task_id>")
@token_required
def get_task(task_id):
    task = db.session.get(Task, task_id)

    if task is None:
        return jsonify(error="not_found", message="Task not found"), 404

    return jsonify(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        status=task.status,
        due_date=task.due_date.isoformat() if task.due_date else None,
        created_at=task.created_at.isoformat(),
        updated_at=task.updated_at.isoformat(),
    ), 200