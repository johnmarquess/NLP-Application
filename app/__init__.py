from flask import Flask
import os
from app.config import DevelopmentConfig, ProductionConfig, TestConfig
from .routes.data_management import data_management_bp
from .routes.data_modeling import data_modeling_bp
from .routes.file_handling import file_handling_bp
from .routes.main import main_bp
from .routes.data_preprocessing import data_preprocessing_bp


def create_app():

    env = os.getenv('FLASK_ENV', 'development')
    if env == 'development':
        config_class = DevelopmentConfig
    elif env == 'testing':
        config_class = TestConfig
    else:
        config_class = ProductionConfig

    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(file_handling_bp)
    app.register_blueprint(data_management_bp)
    app.register_blueprint(data_modeling_bp)
    app.register_blueprint(data_preprocessing_bp)
    app.register_blueprint(main_bp)

    return app
