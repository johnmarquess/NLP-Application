# config.py

class Config(object):
    """
    Common configurations
    """
    # Common configurations
    SECRET_KEY = 'your-secret-key'  # Replace with your secret key

    # Constants for data folders and allowed file extensions
    DATA_FOLDERS = {
        'raw': 'data/data_raw/',
        'saved': 'data/data_saved/',
        'processed': 'data/data_processed/'
    }
    ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx', 'pkl', 'parquet'}


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    # Other development configurations


class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False
    # Other production configurations


class TestingConfig(Config):
    """
    Testing configurations
    """
    TESTING = True
    # Other testing configurations


# Dictionary to map config names to config classes
config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig,
    test=TestingConfig
)
