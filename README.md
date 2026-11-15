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