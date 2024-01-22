import random
from flask import Flask
from flask_socketio import SocketIO
import string
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

# Create Flask application, RESTful API, and SQLAlchemy database instances
app = Flask(__name__)
api = Api()
db = SQLAlchemy()
socketio = SocketIO()

# Function to generate a random string of a specified length
def generate_random_string(length):
    characters = string.ascii_letters + string.digits  # includes both uppercase and lowercase letters and digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

# Decorator to handle exceptions in API routes
def api_handle_exception(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except AssertionError as exception_message:
            # Rollback database changes in case of AssertionError
            db.session.rollback()
            return {"message": "{}.".format(str(exception_message))}, 400
        except TypeError as e:
            # Rollback database changes in case of TypeError
            db.session.rollback()
            return {"message": str(e)}, 404
        except AttributeError as e:
            # Rollback database changes in case of AttributeError
            db.session.rollback()
            return {"message": "Data not found"}, 404
        except IntegrityError as e:
            # Rollback database changes in case of IntegrityError
            db.session.rollback()
            return {"message": str(e)}, 500
        except Exception as e:
            # Rollback database changes in case of other exceptions
            db.session.rollback()
            return {"message": str(e)}, 500
        finally:
            # Remove the database session in all cases
            db.session.remove()
    
    return wrapper  # Return the decorated function
