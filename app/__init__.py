# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
migrate = Migrate()
bs = Bootstrap()


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app)
    bs.init_app(app)

    from app.main import bp
    app.register_blueprint(bp)

    return app


from app import models