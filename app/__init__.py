# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
migrate = Migrate()
bs = Bootstrap()


def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    bs.init_app(app)

    from app.main import bp
    app.register_blueprint(bp)

    return app


from app import models