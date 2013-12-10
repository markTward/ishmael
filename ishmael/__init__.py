# -*- coding: utf-8 -*-
from flask import Flask 
from werkzeug.routing import Rule
import os

# initialize a flask app 
app = Flask(__name__)

# Acquire configuration
ishmael_config = 'config.' + os.environ['ISHMAEL_CONFIG']
app.config.from_object(ishmael_config)

# extend app with Flask-SSLify, forcing https per config setting
if app.config['USE_SSLIFY'] == True:
    sslify = SSLify(app)

#rules
app.url_map.add(Rule('/index', endpoint='index'))

# views
from ishmael.views import general
from ishmael.views import restapi_home
from ishmael.views import restapi_id
from ishmael.views import restapi_path
from ishmael.views import restapi_search
from ishmael.views import restapi_util

from ishmael import error
