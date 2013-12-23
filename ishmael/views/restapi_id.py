# -*- coding: utf-8 -*-
"""
    restapi_id.py
    record lookup by unique id
"""
from flask import jsonify, make_response, request
from ishmael import app
from ishmael.dbservice import get_mongodb_db_collection
from ishmael.restservice import get_urlinfo
from ishmael.utils import get_response_template, tailor_app_http_headers, get_app_message
from bson.objectid import ObjectId
from requests import codes

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
	if api_version not in app.config['API_VERSION_ACTIVE']: abort(codes.NOT_FOUND)
	rest_response, rest_response_code = get_urlinfo(api_version, get_urlinfo_by_id, urlid)
	return make_response(jsonify(rest_response), rest_response_code)

# Error response when no id is entered
@app.route('/urlinfo/<string:api_version>/id/', methods = ['GET'])
def missing_data_urlinfo_by_id(api_version):
    # check if API version requested is active
    if api_version not in app.config['API_VERSION_ACTIVE']: abort(codes.NOT_FOUND)

    # produce error response
    rest_response = get_response_template(codes.UNPROCESSABLE_ENTITY, 'fail', api_version)
    rest_response['data'] = {'id' : 'id required: ' + request.path.rstrip('/') + '/<id>',
                             'message': get_app_message('id_api_desc')}

    # return response as json with success status code in header
    return make_response(jsonify(rest_response), codes.UNPROCESSABLE_ENTITY)
