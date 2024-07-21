from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "game_collection.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'FD8hf8d8yfdas*F89dfhsd*FT&DhFD^Fh3ud87&DF'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .tests import tests

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(tests, url_prefix='/')

    from .models import User, MyGame

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    login_manager.login_message_category = 'error'

    @login_manager.user_loader
    def load_user(id_num):
        return User.query.get(int(id_num))

    return app
