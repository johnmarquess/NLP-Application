import os

from flask import current_app


def get_saved_files():
    data_saved_path = os.path.join(current_app.root_path, current_app.config['DATA_SAVED'])
    return os.listdir(data_saved_path)
