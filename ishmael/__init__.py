# -*- coding: utf-8 -*-
from flask import Flask 
from flask_sslify import SSLify
from werkzeug.routing import Rule
import os

# initialize a flask app 
app = Flask(__name__)

# Acquire configuration
ishmael_config = 'config.' + os.environ['ISHMAEL_CONFIG']
app.config.from_object(ishmael_config)

# extend app with Flask-SSLify, forcing https per config setting
if app.config['USE_SSLIFY']:
    sslify = SSLify(app)

#rules
app.url_map.add(Rule('/index', endpoint='index'))
app.url_map.add(Rule('/urlinfo/<string:api_version>/path', endpoint='urlinfo_by_path_missing_data'))
app.url_map.add(Rule('/urlinfo/<string:api_version>/search', endpoint='urlinfo_by_search_missing_data'))
app.url_map.add(Rule('/urlinfo/<string:api_version>/id', endpoint='urlinfo_by_id_missing_data'))

# views
from ishmael.views import general
from ishmael.views import restapi_home
from ishmael.views import restapi_id
from ishmael.views import restapi_path
from ishmael.views import restapi_search
from ishmael.views import restapi_util

from ishmael import error
