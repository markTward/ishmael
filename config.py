# -*- coding: utf-8 -*-
"""
    config.py
"""
import os

class Config(object):
    # Flask App
    DEBUG = False
    TESTING = False
    USE_SSLIFY = True

    # RESTful API settings
    API_VERSION_CURRENT = '1'
    API_VERSION_ACTIVE = ['1']
    API_VERSION_DEPRECATED = []

    #HTTP Headers
    DEFAULT_LANGUAGE = 'en'

class ConfigDev(Config):
    # Flask App
    DEBUG = True
    TESTING = True
    TRAP_BAD_REQUEST_ERRORS = True
    USE_SSLIFY = False

    # Database service sources and settings
    MONGODB_URI = os.environ.get('ISHMAEL_MONGODB_URI', 'mongodb://localhost:27017/')
    MONGODB_DB = 'malwaredb'
    MONGODB_URLS = 'urls'

class ConfigDevFM(ConfigDev):
    DEBUG = False

class ConfigStg(Config):
    #Flask App
    USE_SSLIFY = True

    # Database service sources and settings
    MONGODB_URI = os.environ.get('MONGOHQ_URL')
    MONGODB_DB = 'app19786004'
    MONGODB_URLS = 'urls'

class ConfigProd(Config):
    pass

del os
