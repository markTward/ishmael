# -*- coding: utf-8 -*-

from ishmael import app
from flask import render_template, jsonify, abort
import os

@app.endpoint('index')
@app.route('/')
def index():
	return render_template('index.html')

# Show Flask configuration vars. DEBUG ONLY!
@app.route('/config')
def show_flask_config():

	if app.config['DEBUG']:
		config_response = {'ishmael_config' : os.environ.get('ISHMAEL_CONFIG', None),
						   'flask_config':{k:str(v) for k,v in app.config.items()}}
		return jsonify(config_response)
	else:
		abort(httplib.NOT_FOUND)

