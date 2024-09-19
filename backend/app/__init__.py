# __init__.py

from flask import Flask
from flask_cors import CORS
from backend.app.routes import api
from backend.config.config import configs

# Create Flask application instance
webapp = Flask(
    import_name=__name__,
    static_folder=configs['STATIC_FOLDER'],
    template_folder=configs['TEMPLATE_FOLDER'],
)
CORS(webapp) # Enable CORS for all routes

# Register the Blueprint with the Flask application
webapp.register_blueprint(api)

# Define other routes or configurations as needed
webapp.secret_key = 'your_secret_key_there'

# Import views (routes) to make them accessible
from . import routes