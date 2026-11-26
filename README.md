This project is a Flask-based Task Manager API.

## Setup

1. Clone the repository:
   git clone https://github.com/kmgriffith20-commits/backend-flask-project.git

2. Navigate to the project folder:
   cd backend-flask-project

3. Create a virtual environment:
   python3 -m venv .venv

4. Activate the virtual environment:
   source .venv/bin/activate

5. Install dependencies:
   pip install -r requirements.txt

6. Start the Flask application:

   flask --app 'task_manager:create_app' run --debug

7. Open the application in your browser:

   http://127.0.0.1:5000  


 ## Environment Variables

This project uses two environment variables:

- SECRET_KEY: Used for Flask security.
- DATABASE_URL: Specifies the database connection.

The .env.example file contains sample configuration values.

To create a local environment file, copy .env.example to .env and replace the placeholder values with your own settings.

The .env file should remain private and should not be uploaded to GitHub.

- FLASK_ENV: Selects the application configuration.
  Defaults to development if not specified.


## Database and Migrations

This project uses Flask-SQLAlchemy to manage its database.

Development uses a SQLite database configured as sqlite:///dev.db.

Testing uses an in-memory SQLite database.

Production uses the DATABASE_URL environment variable.

Flask-Migrate is included in the project setup to support database migrations.

Database migration commands and procedures will be documented as the project develops.

## Running with Docker Compose

### Prerequisites

- Docker Desktop
- Docker Compose

### Environment Configuration

Create a `.env` file in the project root with the following example values:

```env
POSTGRES_USER=task_user
POSTGRES_PASSWORD=fake_password
POSTGRES_DB=task_manager
JWT_SECRET_KEY=fake_jwt_secret
```

Replace placeholder credentials with your own local values.
Never commit the `.env` file to GitHub.

### Build and Start the Application

```bash
docker build -t task-manager-api:latest .
docker compose up -d
```

### Apply Database Migrations

```bash
docker compose exec web flask --app task_manager db upgrade
```

### Verify Services

```bash
docker compose ps
curl http://localhost:5001/health
```

The API is available at http://localhost:5001.

### Database Persistence

PostgreSQL 16 uses a named Docker volume called `postgres_data` to preserve database records across container restarts and recreation.

### Stop the Application

```bash
docker compose down
```

Do not use `docker compose down -v` unless you intentionally want to delete the stored database data.

### Persistence Test Results

- Created a task named Docker Persistence Test.
- Retrieved task ID 1 successfully.
- Removed both containers using docker compose down.
- Recreated both containers using docker compose up -d.
- Retrieved the same task with HTTP 200 OK.
- Verified that the task ID, status, description, and creation timestamp remained unchanged.

Result: PASS. Database persistence was successfully verified.

## Production Deployment

The Task Manager API is successfully deployed to Render using Docker and Gunicorn, with a cloud-hosted Neon PostgreSQL database.

### Deployment Details

- **Hosting:** Render
- **Database:** Neon PostgreSQL
- **Containerization:** Docker
- **Application Server:** Gunicorn
- **Authentication:** JWT
- **Database Migrations:** Alembic
- **Release Version:** v1.0
- **Live API:** https://task-manager-api-d2at.onrender.com
- **Health Check:** https://task-manager-api-d2at.onrender.com/health

### Production Verification

| Endpoint | HTTP Status | Result |
|---|---|---|
| GET /health | 200 OK | PASS |
| POST /register | 201 Created | PASS |
| POST /login | 200 OK | PASS |
| POST /tasks | 201 Created | PASS |
| GET /tasks/1 | 200 OK | PASS |

### Environment Variables

- DATABASE_URL
- JWT_SECRET_KEY
- SECRET_KEY
- FLASK_ENV

Sensitive credentials are managed through environment variables and are not included in the repository.

### Deployment Summary

The application successfully connects to Neon PostgreSQL, applies database migrations, registers and authenticates users, and creates and retrieves tasks through authenticated API requests.

All five planned production endpoint tests passed successfully.