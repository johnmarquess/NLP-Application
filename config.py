import os


class Config(object):
    SECRET_KEY = 'there_once_was_a_girl_from_nantucket'
    HF_ACCESS_TOKEN = os.environ.get('HF_ACCESS_TOKEN')
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    MODEL_DIR = os.path.join(BASE_DIR, 'models')
    MODEL_OUTPUTS_DIR = os.path.join(BASE_DIR, 'model_outputs')
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    REFERENCE_DATA_DIR = os.path.join(DATA_DIR, 'reference')
    RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
    CLEAN_DATA_DIR = os.path.join(DATA_DIR, 'clean')
    PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
    LABELLED_DATA_DIR = os.path.join(DATA_DIR, 'labelled')
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
