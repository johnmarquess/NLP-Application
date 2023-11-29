from flask import Flask

from app.config import Config
from .routes.data_management import data_management_bp
from .routes.data_modeling import data_modeling_bp
from .routes.file_handling import file_handling_bp
from .routes.main import main_bp
from .routes.reporting import reporting_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(file_handling_bp)
    app.register_blueprint(data_management_bp)
    app.register_blueprint(data_modeling_bp)
    app.register_blueprint(reporting_bp)
    app.register_blueprint(main_bp)

    return app
