# -*- coding: utf-8 -*-

import inspect

from flask import jsonify, make_response, request

from ishmael import app
from ishmael.dbservice import get_mongodb_db_collection
from ishmael.utils import get_response_template, tailor_app_http_headers, get_app_message
from bson.objectid import ObjectId
from requests import codes

@app.route('/urlinfo/<string:api_version>/count', methods = ['GET'])
def count(api_version):
	try:
		url_coll = get_mongodb_db_collection(app.config['MONGODB_URLS'])
		rc = url_coll.count()
		resp = get_response_template(codes.OK, 'success', None)
		resp['data'] = {'record_count' : rc}
		resp['message'] =  'urls record count',
		code = codes.OK
	except:
		app.logger.debug(inspect.stack()[0][3] +  ': ' + get_app_message('db_na'))
		resp = get_response_template(codes.SERVICE_UNAVAILABLE, 'error', None)
		resp['message'] =  'malewaredb service unavailable',
		resp['data'] = None
		code = codes.SERVICE_UNAVAILABLE 
	return make_response(jsonify(resp), code)

