from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "game_collection.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'FD8hf8d8yfdas*F89dfhsd*FT&DhFDhxy7^#$9cvhd7^DD^Fh3ud87&DF'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, MyGame

    with app.app_context():
        db.create_all()

    return app
