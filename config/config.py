class Config:
    SECRET_KEY = 'your_secret_key'
    DATA_RAW_FOLDER = 'data/data_raw/'
    DATA_PROCESSED_FOLDER = 'data/data_processed/'
    DATA_SAVED = 'data/data_saved/'
    ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx', 'pkl', 'parquet'}
    # Other general configurations


class DevelopmentConfig(Config):
    DEBUG = True
    # Development-specific configurations


class TestingConfig(Config):
    TESTING = True
    # Testing-specific configurations


class ProductionConfig(Config):
    DEBUG = False
