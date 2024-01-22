from datetime import timedelta
from importlib import import_module
import os
from flask import app

from flask.cli import load_dotenv

# Import extensions and resources from the current package
from .extensions import api, db, socketio, app
from .resources import ns


# Dynamically import all modules in the "model" folder
def import_all_modules():
    model_folder = os.path.join(os.path.dirname(__file__), "model")

    for file in os.listdir(model_folder):
        if file.endswith(".py") and file != "__init__.py":
            # Get module name without file extension
            module_name = file[:-3]
            # Import the module dynamically
            module = import_module(f"app.model.{module_name}")
            # Make the module accessible globally
            globals()[module_name] = module
            
# Create a Flask application
def create_app():
    # Load environment variables from a .env file
    load_dotenv()

    # Configure the Flask app with database and JWT settings
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"{os.getenv('DB_CONNECTION')}+mysqlconnector://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@localhost/{os.getenv('DB_DATABASE')}"
    app.config["DEBUG"] = os.getenv("DEBUG")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_KEY")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
        seconds=int(os.getenv("JWT_EXPIRE_TOKEN", 4800))
    )

    # Initialize Flask extensions
    api.init_app(app)
    db.init_app(app)
    socketio.init_app(app)

    # Add Flask-RESTful namespace
    api.add_namespace(ns)

    # Dynamically import all modules in the "model" folder
    import_all_modules()

    # Create database tables within the app context
    with app.app_context():
        db.create_all()

    return app  # Return the configured Flask app