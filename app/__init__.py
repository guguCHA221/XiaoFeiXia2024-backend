import os

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__, static_folder='static', template_folder='templates')
    CORS(app)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)

    from app.routes import auth, lost_items, suit_rentals, users
    app.register_blueprint(auth.bp)
    app.register_blueprint(lost_items.bp)
    app.register_blueprint(suit_rentals.bp)
    app.register_blueprint(users.bp)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(app.static_folder + '/' + path):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.template_folder, 'index.html')

    return app
