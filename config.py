import os


class Config(object):
    SECRET_KEY = 'there_once_was_a_girl_from_nantucket'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
    CLEAN_DATA_DIR = os.path.join(DATA_DIR, 'clean')
    PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
    MODELS_DIR = os.path.join(BASE_DIR, 'model_outputs')
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
    TEMPLATES_AUTO_RELOAD = True
    # Other common configurations


class ProductionConfig(Config):
    # Production-specific configurations
    DEBUG = False


class DevelopmentConfig(Config):
    # Development-specific configurations
    DEBUG = True


class TestingConfig(Config):
    # Testing-specific configurations
    TESTING = True
