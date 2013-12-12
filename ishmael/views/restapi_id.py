# -*- coding: utf-8 -*-

import inspect
import httplib

from flask import jsonify, make_response, request
from bson.objectid import ObjectId

from ishmael import app
from ishmael.dbservice import get_mongodb_db_collection
from ishmael.restservice import get_urlinfo
from ishmael.utils import get_response_template, tailor_app_http_headers

# search mongodb by internal id
def get_urlinfo_by_id(id):
    url_coll = get_mongodb_db_collection(app.config['MONGODB_URLS'])
    app.logger.debug('_id query ==> {\'_id\' : ObjectId(\'' + str(id) + '\')}')
    record_set = {}
    record_set = url_coll.find({'_id' : ObjectId(id)})
    return record_set

# Route to query malware db services by 'self' id provided by API
@app.route('/urlinfo/<string:api_version>/id/<string:urlid>', methods = ['GET'])
@tailor_app_http_headers
def find_urlinfo_by_id(api_version, urlid):
	if api_version not in app.config['API_VERSION_ACTIVE']: abort(httplib.NOT_FOUND)
	rest_response, rest_response_code = get_urlinfo(api_version, get_urlinfo_by_id, urlid)
	print 'find_urlinfo just before RETURN'
	return make_response(jsonify(rest_response), rest_response_code)

# Error response when no id is entered
@app.route('/urlinfo/<string:api_version>/id', methods = ['GET'])
@app.route('/urlinfo/<string:api_version>/id/', methods = ['GET'])
def urlinfo_by_id_missing_data(api_version):
    # check if API version requested is active
    if api_version not in app.config['API_VERSION_ACTIVE']: abort(httplib.NOT_FOUND)

    # produce error response
    rest_response = get_response_template(httplib.UNPROCESSABLE_ENTITY, 'fail', api_version)
    rest_response['data'] = {'id' : 'id required: ' + request.path + '/<id>',
                             'message':'search for an exact match on the database id assigned to the URL.  returns 0 or 1 record.'}

    # return response as json with success status code in header
    return make_response(jsonify(rest_response), httplib.UNPROCESSABLE_ENTITY)
