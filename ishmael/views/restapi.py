# -*- coding: utf-8 -*-

import inspect
from flask import jsonify, make_response
from httplib import OK, SERVICE_UNAVAILABLE

from ishmael import app
from ishmael.dbservice import get_mongodb_client
from ishmael.utils import get_response_template

# attempt to get a mongodb collection
def get_mongodb_db_collection(collection):
	get_mongodb_client()
	db = app.mdb_client[app.config['MONGODB_DB']]
	col = db[collection]
	return col

@app.route('/count')
def count():
	try:
		url_coll = get_mongodb_db_collection(app.config['MONGODB_URLS'])
		rc = url_coll.count()
		resp = get_response_template(OK, 'success', None)
		resp['data'] = {'record_count' : rc}
		resp['message'] =  'urls record count',
		code = OK
	except:
		print ' * ' + __name__ + '.' + inspect.stack()[0][3] +  ' : datbase unavailable'
		resp = get_response_template(SERVICE_UNAVAILABLE, 'error', None)
		resp['message'] =  'malewaredb service unavailable',
		resp['data'] = None
		code = SERVICE_UNAVAILABLE 
	return make_response(jsonify(resp), code)

