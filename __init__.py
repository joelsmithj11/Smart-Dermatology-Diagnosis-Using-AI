from flask import Flask
from flask_login import LoginManager
from app.utils.db import init_db
import os

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.secret_key = "dev-secret-key-change-this"  # TODO: Use environment variable
    
    # Init DB
    init_db()

    # Init Login Manager
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Register Blueprints
    from app.routes_auth import auth_bp
    from app.routes_main import main_bp
    from app.routes_admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    from flask import session
    from app.utils.translations import get_translation

    @app.context_processor
    def inject_get_text():
        def get_text(key):
            lang = session.get('lang', 'en')
            return get_translation(key, lang)
        return dict(get_text=get_text)

    return app
