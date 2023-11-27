class Config(object):
    SECRET_KEY = 'a-very-hard-to-guess-string'
    DATA_RAW = 'data/data_raw/'
    DATA_PROCESSED = 'data/data_processed/'
    DATA_SAVED = 'data/data_saved/'
    ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx'}
    DEBUG = True  # Set to False in production
