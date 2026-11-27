# Task Manager API

A Flask-based REST API that allows users to register, authenticate, and manage their own tasks securely.

## Features

- User registration and login
- Secure password hashing
- JWT authentication
- Role-based authorization
- Task creation and retrieval
- Task ownership protection
- PostgreSQL database integration
- Database migrations
- Docker containerization
- Production deployment
- Health check endpoint

## Technology Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Alembic
- JWT
- PostgreSQL
- Docker
- Docker Compose
- Gunicorn
- Render
- Neon PostgreSQL

## Running with Docker Compose

### Prerequisites

- Git
- Docker Desktop
- Docker Compose

### 1. Clone the Repository

```bash
git clone --branch unit4-docker https://github.com/kmgriffith20-commits/backend-flask-project.git
cd backend-flask-project
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder credentials with your own local development values.

The environment variables include:

- FLASK_ENV
- SECRET_KEY
- JWT_SECRET_KEY
- DATABASE_URL
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_DB

Docker Compose constructs the database connection URL using the PostgreSQL environment variables.

The `.env` file is excluded from Git through `.gitignore`. Never commit real credentials or production secrets.

### 3. Build the Docker Image

```bash
docker build -t task-manager-api:latest .
```

### 4. Start the Containers

```bash
docker compose up -d
```

### 5. Apply Database Migrations

```bash
docker compose exec web flask --app task_manager db upgrade
```

### 6. Verify Running Services

```bash
docker compose ps
```

### 7. Test the Health Endpoint

```bash
curl -i http://localhost:5001/health
```

Expected HTTP status:

```text
HTTP/1.1 200 OK
```

The local API is available at:

http://localhost:5001

### 8. Stop the Application

```bash
docker compose down
```

Do not use `docker compose down -v` unless you intentionally want to delete the stored database data.

## Local Development Without Docker

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure local environment variables, including a JWT secret and a suitable database URL.

For SQLite development, use:

```bash
export FLASK_ENV=development
export DATABASE_URL=sqlite:///dev.db
export JWT_SECRET_KEY=local-development-only-secret
```

Apply migrations:

```bash
flask --app task_manager db upgrade
```

Start Flask:

```bash
flask --app task_manager run --debug
```

The default Flask development URL is:

http://127.0.0.1:5000

## Database Models

### User

- ID
- Email
- Password hash
- Role
- Creation timestamp

### Task

- ID
- User ID
- Title
- Description
- Status
- Due date
- Creation timestamp
- Update timestamp

The User and Task models have a one-to-many relationship. Each user can own multiple tasks.

## Authentication and Authorization

Users register with an email and password. Passwords are securely hashed before being stored.

Successful login returns a JWT access token. Protected endpoints require a valid bearer token.

Task ownership checks prevent users from accessing another user's tasks. Administrative endpoints require the appropriate user role.

## Main API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /health | Application health check |
| POST | /register | Register a user |
| POST | /login | Authenticate a user |
| GET | /me | Retrieve authenticated user |
| GET | /api/profile | Retrieve user profile |
| PATCH | /api/profile | Update user profile |
| GET | /api/admin/ping | Admin-only endpoint |
| POST | /tasks | Create a task |
| GET | /tasks | List owned tasks |
| GET | /tasks/{id} | Retrieve an owned task |

## Project Organization

- task_manager/__init__.py: Flask application factory
- task_manager/models.py: Database models
- task_manager/auth/routes.py: Authentication routes
- task_manager/tasks/routes.py: Task routes
- task_manager/auth/decorators.py: Authentication and authorization
- config.py: Application configuration
- migrations/: Database migrations
- Dockerfile: Application container configuration
- docker-compose.yml: Web and database services
- .env.example: Example environment configuration
- .gitignore: Excluded private and generated files

## Database and Migrations

The application uses Flask-SQLAlchemy and Alembic migrations.

Development supports SQLite or PostgreSQL.

Testing uses an in-memory SQLite database.

Production uses Neon PostgreSQL through the DATABASE_URL environment variable.

## Database Persistence

PostgreSQL 16 uses a named Docker volume called `postgres_data` to preserve records across container restarts and recreation.

### Persistence Test Results

- Created a task named Docker Persistence Test.
- Retrieved task ID 1 successfully.
- Removed both containers using docker compose down.
- Recreated both containers using docker compose up -d.
- Retrieved the same task with HTTP 200 OK.
- Verified that the task ID, status, description, and creation timestamp remained unchanged.

Result: PASS.

## Fresh Clone Verification

The project was tested from a fresh Git clone using Docker Compose.

Verification included:

- Docker image build
- Container startup
- Database migrations
- Health endpoint
- User registration
- User authentication
- Task creation and retrieval
- Task ownership isolation between two users

Result: PASS.

## Security Verification

The following security behaviors were tested:

- Incorrect password rejection
- Duplicate email rejection
- Expired JWT rejection
- Unauthorized administrative access rejection
- Task ownership isolation
- Unauthorized task retrieval returning HTTP 404

Additional authentication test evidence is documented in AUTH_TESTS.md.

## Production Deployment

The Task Manager API is deployed to Render using Docker and Gunicorn, with a cloud-hosted Neon PostgreSQL database.

### Deployment Details

- Hosting: Render
- Database: Neon PostgreSQL
- Containerization: Docker
- Application Server: Gunicorn
- Authentication: JWT
- Database Migrations: Alembic
- Release Version: v1.0

### Live API

https://task-manager-api-d2at.onrender.com

### Health Check

https://task-manager-api-d2at.onrender.com/health

### Production Verification

| Endpoint | HTTP Status | Result |
|---|---|---|
| GET /health | 200 OK | PASS |
| POST /register | 201 Created | PASS |
| POST /login | 200 OK | PASS |
| POST /tasks | 201 Created | PASS |
| GET /tasks/1 | 200 OK | PASS |

### Production Environment Variables

- DATABASE_URL
- JWT_SECRET_KEY
- SECRET_KEY
- FLASK_ENV

Sensitive production credentials are managed through environment variables and are not included in the repository.

## Deployment Summary

The application successfully connects to Neon PostgreSQL, applies database migrations, registers and authenticates users, and creates and retrieves tasks through authenticated API requests.

All five planned production endpoint tests passed successfully.

## Future Improvements

- Expand automated test coverage.
- Improve API documentation.
- Add continuous integration testing.

## Author

Katie Griffith

AI Software Engineering Student — Maestro College