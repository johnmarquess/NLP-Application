class Config(object):
    SECRET_KEY = 'a-secret-key'
    DATA_RAW = 'path/to/data_raw/'
    DATA_PROCESSED = 'path/to/data_processed/'
    ALLOWED_FILETYPES = ['.csv', '.xls', '.xlsx']
    # Other configurations


class DevelopmentConfig(Config):
    DEBUG = True
    # Other development-specific configurations


class ProductionConfig(Config):
    DEBUG = False
    # Other production-specific configurations
