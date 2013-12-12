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
	# provide a sample ishmael json response
	rest_response, rest_response_code = \
		get_urlinfo(app.config['API_VERSION_CURRENT'], \
		restapi_path.get_urlinfo_by_path, 'melville.io/helloishmael', qs='', \
		search=False)

	#app.logger.debug('example url ==> ' + str(example_ishmael_url))
	return render_template('index.html', results=json.dumps(rest_response, sort_keys=True, indent=3, default=json_util.default))

# Show Flask configuration vars. DEBUG ONLY!
@app.route('/config')
def show_flask_config():

	if app.config['DEBUG']:
		config_response = {'ishmael_config' : os.environ.get('ISHMAEL_CONFIG', None),
						   'flask_config':{k:str(v) for k,v in app.config.items()},
						   'request.host_url' : request.host_url,
						   'request.url_root' : request.url_root,
						   'dir(request)':dir(request)}
		return jsonify(config_response)
	else:
		abort(httplib.NOT_FOUND)

