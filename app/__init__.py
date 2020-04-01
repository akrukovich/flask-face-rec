"""Application package."""
from config import Config

from flask import Flask

from flask_bootstrap import Bootstrap

from flask_migrate import Migrate

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
bs = Bootstrap()


def create_app(config_class=Config):
    """
    Application factory function.

    Return application instance after setting up all the configuration
    Args:
        config_class: Config class

    Returns:
        app: Flask application instance.

    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    bs.init_app(app)

    from app.main import bp
    app.register_blueprint(bp)

    return app


from app import models
