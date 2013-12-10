# -*- coding: utf-8 -*-

import inspect
import httplib

from flask import jsonify, make_response, request
from bson.objectid import ObjectId

from ishmael import app
from ishmael.dbservice import get_mongodb_db_collection
#from ishmael.restservice import get_urlinfo
from ishmael.utils import get_response_template

# search mongodb by internal id
def get_urlinfo_by_id(id):
	print 'in get_urlinfO-by_id'
	url_coll = get_mongodb_db_collection(app.config['MONGODB_URLS'])
	print 'url_coll', url_coll
	print 'BEFORE mongodb call record set'
	record_set = {}
	record_set = url_coll.find({'_id' : ObjectId(id)})
	print 'AFTER mongodb call record set'
	return record_set

# acquire url information from malware data sources
def get_urlinfo(api_version, urlfunc, urlkey, **kwargs):
    try:
        # attempt to find url using function, key and other optional arguments
        print 'calling from get_urlinfo', api_version, urlfunc, urlkey
        urlcheck = urlfunc(urlkey, **kwargs)
        print 'back from get_urlinfo', api_version, urlfunc, urlkey

        # set response default values
        rest_response = get_response_template(httplib.OK, 'success', api_version)

        # modify data payload for public consumption
        #rest_response['data'] = make_success_data(api_version, urlcheck)
        rest_response['data'] = {'temp data':'real coming soon'}

        # return response as json with success status code in header
        return (rest_response, httplib.OK)

    except Exception as ex:
		print 'exception'

# Route to query malware db services by 'self' id provided by API
@app.route('/urlinfo/<string:api_version>/id/<string:urlid>', methods = ['GET'])
#@tailor_app_http_headers
def find_urlinfo_by_id(api_version, urlid):
	if api_version not in app.config['API_VERSION_ACTIVE']: abort(httplib.NOT_FOUND)
	print ' * ' + __name__ + '.' + inspect.stack()[0][3] +  ' : request.view_args' + str(request.view_args)
	rest_response, rest_response_code = get_urlinfo(api_version, get_urlinfo_by_id, urlid)
	print ' * ' + __name__ + '.' + inspect.stack()[0][3] +  ' : back from get_urlinf_by_id'
	return make_response(jsonify(rest_response), rest_response_code)

@app.route('/count')
def count():
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

