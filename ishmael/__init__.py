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
app.url_map.add(Rule('/urlinfo', endpoint = 'redirect_urlinfo_current_api'))
app.url_map.add(Rule('/urlinfo/<string:api_version>', endpoint = 'get_urlinfo_home'))
app.url_map.add(Rule('/urlinfo/<string:api_version>/path', endpoint='missing_data_urlinfo_by_path'))
app.url_map.add(Rule('/urlinfo/<string:api_version>/search', endpoint='missing_data_urlinfo_by_search'))
app.url_map.add(Rule('/urlinfo/<string:api_version>/id', endpoint='missing_data_urlinfo_by_id'))

# views
from ishmael.views import general
from ishmael.views import restapi_home
from ishmael.views import restapi_id
from ishmael.views import restapi_path
from ishmael.views import restapi_search
from ishmael.views import restapi_util

from ishmael import error
