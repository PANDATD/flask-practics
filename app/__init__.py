from flask import Flask
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'

    from .routes.main import main_bp
    from .routes.auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    from .routes.tasks import tasks_bp
    app.register_blueprint(tasks_bp)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from app.models import users
    from app.routes.auth import SessionUser

    @login_manager.user_loader
    def load_user(user_id):
        if user_id in users:
            return SessionUser(user_id)
        return None

    return app
