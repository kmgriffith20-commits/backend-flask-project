from .extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(
        db.String(20),
        nullable=False,
        default="user",
        server_default="user"
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now()
    )

class Task(db.Model):
    __tablename__ = "tasks"

    __table_args__ = (
        db.CheckConstraint(
            "length(trim(title)) BETWEEN 1 AND 120",
            name="ck_tasks_title_length",
        ),
        db.CheckConstraint(
            "status IN ('pending', 'in_progress', 'done')",
            name="ck_tasks_status",
        ),
    )

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(
        db.String(20),
        nullable=False,
        server_default="pending",
    )
    due_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),
        onupdate=db.func.now(),
    ) 