from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

# *  Local imports
from .auth import auth
from .config import Config
from .models import UserModel

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(username):
    return UserModel.query(username)


def create_app():
    app = Flask(__name__,
                template_folder='./templates',
                static_folder='./static')
    bootstrap = Bootstrap(app)

    app.config.from_object(Config)

    app.register_blueprint(auth)

    return app
