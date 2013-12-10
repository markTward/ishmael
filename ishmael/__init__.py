# -*- coding: utf-8 -*-
from flask import Flask 
from werkzeug.routing import Rule
import os

app = Flask(__name__)

# Acquire configuration
ishmael_config = 'config.' + os.environ['ISHMAEL_CONFIG']
app.config.from_object(ishmael_config)

# views
from ishmael.views import general
from ishmael.views import restapi

#rules
app.url_map.add(Rule('/index', endpoint='index'))
