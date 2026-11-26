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
    try:
        page = int(request.args.get("page", "1"))
        per_page = int(request.args.get("per_page", "20"))
    except ValueError:
        return jsonify(
            error="validation_error",
            message="page and per_page must be integers",
        ), 400

    if page < 1:
        return jsonify(
            error="validation_error",
            message="page must be a positive integer",
        ), 400

    if not 1 <= per_page <= 50:
        return jsonify(
            error="validation_error",
            message="per_page must be a positive integer no greater than 50",
        ), 400

    owner_filter = Task.user_id == g.current_user_id
    count_query = db.select(db.func.count(Task.id)).where(owner_filter)
    total = db.session.execute(count_query).scalar_one()

    pages = (total + per_page - 1) // per_page
    tasks = []
    if page <= pages:
        query = (
            db.select(Task)
            .where(owner_filter)
            .order_by(Task.id.asc())
            .limit(per_page)
            .offset((page - 1) * per_page)
        )
        tasks = db.session.scalars(query).all()

    return jsonify(
        tasks=[
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
        ],
        page=page,
        per_page=per_page,
        total=total,
        pages=pages,
    ), 200

@tasks_bp.get("/tasks/<int:task_id>")
@token_required
def get_task(task_id):
    query = db.select(Task).where(
        Task.id == task_id,
        Task.user_id == g.current_user_id,
    )
    task = db.session.execute(query).scalar_one_or_none()

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

@tasks_bp.patch("/tasks/<int:task_id>")
@token_required
def update_task(task_id):
    query = db.select(Task).where(
        Task.id == task_id,
        Task.user_id == g.current_user_id,
    )
    task = db.session.execute(query).scalar_one_or_none()
    if task is None:
        return jsonify(error="not_found", message="Task not found"), 404
    
    if task.status == "done":
        return jsonify(
            error="forbidden",
            message="Completed tasks cannot be edited",
        ), 403
    
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="validation_error", message="Expected a JSON object"), 400

    if data.keys() - {"title", "description", "status", "due_date"}:
        return jsonify(
            error="validation_error",
            message="Only title, description, status, and due_date can be updated",
        ), 400

    if "title" in data:
        title = data["title"]
        if not isinstance(title, str) or not 1 <= len(title.strip()) <= 120:
            return jsonify(
                error="validation_error",
                message="Title must be between 1 and 120 characters",
            ), 400
        data["title"] = title.strip()

    if "description" in data:
        description = data["description"]
        if description is not None and not isinstance(description, str):
            return jsonify(
                error="validation_error",
                message="Description must be a string or null",
            ), 400

    if "status" in data and data["status"] not in ("pending", "in_progress", "done"):
        return jsonify(
            error="validation_error",
            message="Status must be pending, in_progress, or done",
        ), 400

    if "due_date" in data and data["due_date"] is not None:
        try:
            due_date = date.fromisoformat(data["due_date"])
            if due_date.isoformat() != data["due_date"]:
                raise ValueError
        except (TypeError, ValueError):
            return jsonify(
                error="validation_error",
                message="Due date must use YYYY-MM-DD",
            ), 400
        data["due_date"] = due_date

    for field, value in data.items():
        setattr(task, field, value)
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
    ), 200

@tasks_bp.delete("/tasks/<int:task_id>")
@token_required
def delete_task(task_id):
    query = db.select(Task).where(
        Task.id == task_id,
        Task.user_id == g.current_user_id,
    )
    task = db.session.execute(query).scalar_one_or_none()

    if task is None:
        return jsonify(error="not_found", message="Task not found"), 404

    db.session.delete(task)
    db.session.commit()
    return "", 204