# -*- coding: utf-8 -*-
"""
    config.py
"""
import os

class Config(object):
    # Flask App
    DEBUG = False
    TESTING = False
    USE_SSLIFY = False

    # RESTful API settings
    API_VERSION_CURRENT = '1'
    API_VERSION_ACTIVE = ['1']
    API_VERSION_DEPRECATED = []

    #HTTP Headers
    DEFAULT_LANGUAGE = 'en'
    
    #MongoDB
    MONGODB_SERVER_ID = None

class ConfigDev(Config):
    # Flask App
    DEBUG = True
    TRAP_BAD_REQUEST_ERRORS = True
    USE_SSLIFY = False

    # Database service sources and settings
    MONGODB_URI = os.environ.get('ISHMAEL_MONGODB_URI', 'mongodb://localhost:27017/')
    MONGODB_DB = 'malwaredb'
    MONGODB_URLS = 'urls'
    MONGODB_SERVER_ID = 'Kbr607MrEdx86Q'

class ConfigStg(Config):
    #Flask App
    USE_SSLIFY = True

    # Database service sources and settings
    MONGODB_URI = os.environ.get('MONGOHQ_URL')
    MONGODB_DB = 'app20251520'
    MONGODB_URLS = 'urls'
    MONGODB_SERVER_ID = 'f2XHlkjkayYHWg'

class ConfigProd(Config):
    pass

class ConfigTest(Config):
    TESTING = True
    
# eclipse    
class ConfigPyDev(ConfigDev):
    DEBUG_WITH_APTANA = True

# heroku foreman 
class ConfigDevFm(ConfigDev):
    DEBUG = False

del os

