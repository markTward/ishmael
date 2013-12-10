# -*- coding: utf-8 -*-
from flask import Flask 
from werkzeug.routing import Rule

app = Flask(__name__)

# views
from ishmael.views import general

#rules
app.url_map.add(Rule('/index', endpoint='index'))
