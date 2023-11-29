class Config(object):
    SECRET_KEY = 'a-very-hard-to-guess-string'
    DATA_RAW = 'data/data_raw/'
    DATA_PROCESSED = 'data/data_processed/'
    DATA_SAVED = 'data/data_saved/'
    ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx'}
    DEBUG = True  # Set to False in production
    WTF_CSRF_ENABLED = True  # Prevent CSRF attacks


class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    ENV = 'development'


class TestConfig(Config):
    TESTING = True
    ENV = 'testing'
    WTF_CSRF_ENABLED = False  # Allows form testing
