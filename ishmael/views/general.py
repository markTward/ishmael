# -*- coding: utf-8 -*-


from flask import render_template, jsonify, abort, request, url_for
from ishmael import app
from ishmael.restservice import get_urlinfo
from ishmael.views import restapi_path
import os
import json
from bson import BSON
from bson import json_util

@app.endpoint('index')
@app.route('/')
def index():
	try:
		rest_response, rest_response_code = \
			get_urlinfo(app.config['API_VERSION_CURRENT'], \
			restapi_path.get_urlinfo_by_path, 'melville.io/helloishmael', qs='call=me', \
			search=False)
	except Exception as ex:
		rest_response = {'message' : 'our regrets, but there seems to be a problem'}
		if app.config['DEBUG']:
			rest_response['type'] = type(ex).__name__
			rest_response['module'] = type(ex).__module__
	results = json.dumps(rest_response, sort_keys=True, indent=3, default=json_util.default)
	return render_template('index.html', results=results)  

# Show Flask configuration vars. DEBUG ONLY!
@app.route('/config')
def show_flask_config():

	if app.config['DEBUG']:
		config_response = {'ishmael_config' : os.environ.get('ISHMAEL_CONFIG', None),
						   'flask_config':{k:str(v) for k,v in app.config.items()},
						   'request.host_url' : request.host_url,
						   'request.url_root' : request.url_root,
						   'app.debug':app.debug}
		return jsonify(config_response)
	else:
		abort(httplib.NOT_FOUND)

