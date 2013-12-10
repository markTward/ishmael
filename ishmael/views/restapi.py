# -*- coding: utf-8 -*-

import inspect
import httplib

from flask import jsonify, make_response, request
from bson.objectid import ObjectId

from ishmael import app
from ishmael.dbservice import get_mongodb_db_collection
from ishmael.restservice import get_urlinfo, get_urlinfo_by_id
from ishmael.utils import get_response_template

# Route to query malware db services by 'self' id provided by API
@app.route('/urlinfo/<string:api_version>/id/<string:urlid>', methods = ['GET'])
#@tailor_app_http_headers
def find_urlinfo_by_id(api_version, urlid):
	if api_version not in app.config['API_VERSION_ACTIVE']: abort(httplib.NOT_FOUND)
	print ' * ' + __name__ + '.' + inspect.stack()[0][3] +  ' : request.view_args' + str(request.view_args)
	rest_response, rest_response_code = get_urlinfo(api_version, get_urlinfo_by_id, urlid)
	print ' * ' + __name__ + '.' + inspect.stack()[0][3] +  ' : back from get_urlinf_by_id'
	return make_response(jsonify(rest_response), rest_response_code)

@app.route('/urlinfo/<string:api_version>/count', methods = ['GET'])
def count(api_version):
	try:
		url_coll = get_mongodb_db_collection(app.config['MONGODB_URLS'])
		rc = url_coll.count()
		resp = get_response_template(httplib.OK, 'success', None)
		resp['data'] = {'record_count' : rc}
		resp['message'] =  'urls record count',
		code = httplib.OK
	except:
		print ' * ' + __name__ + '.' + inspect.stack()[0][3] +  ' : datbase unavailable'
		resp = get_response_template(httplib.SERVICE_UNAVAILABLE, 'error', None)
		resp['message'] =  'malewaredb service unavailable',
		resp['data'] = None
		code = httplib.SERVICE_UNAVAILABLE 
	return make_response(jsonify(resp), code)

