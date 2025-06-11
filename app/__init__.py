from flask import Flask
from app.config import DEBUG, PORT

def create_app():
    """
    Create and configure the Flask application
    """
    app = Flask(__name__)
    
    # Register blueprints
    from app.routes.slack_routes import slack_bp
    app.register_blueprint(slack_bp, url_prefix='/slack')
    
    return app 