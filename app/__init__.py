from flask import Flask

from config import config_by_name


def create_app(config_name):
    app = Flask(__name__)
    app.secret_key = 'your_secret_key_here'
    app.config.from_object(config_by_name[config_name])

    from .routes import main
    app.register_blueprint(main)

    return app
