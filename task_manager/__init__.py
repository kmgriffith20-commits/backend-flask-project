import os
from flask import Flask
from dotenv import load_dotenv
from config import config_by_name
from .extensions import db, migrate

load_dotenv()

def create_app(config_name=None):
    app = Flask(__name__)

    config_name = config_name or os.getenv(
        "FLASK_ENV", "development"
    )

    app.config.from_object(
        config_by_name[config_name]
    )

    db.init_app(app)
    migrate.init_app(app, db)

    from .main import main_bp
    app.register_blueprint(main_bp)

    from . import models

    from .auth.routes import auth_bp
    app.register_blueprint(auth_bp)
    
    return app
