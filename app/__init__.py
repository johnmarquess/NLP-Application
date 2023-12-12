from flask import Flask

from .blueprints.data_processor.routes import data_processor_bp
from .blueprints.file_manager.routes import file_manager_bp
from .blueprints.home.routes import main_bp
from .blueprints.model_builder.routes import model_builder_bp
from .blueprints.model_manager.routes import model_manager_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')  # Adjust as needed

    # Other blueprints and configurations
    app.register_blueprint(main_bp)
    app.register_blueprint(file_manager_bp)
    app.register_blueprint(data_processor_bp)
    app.register_blueprint(model_builder_bp)
    app.register_blueprint(model_manager_bp)

    return app
