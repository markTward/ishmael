# -*- coding: utf-8 -*-
"""
    restapi_path.py
    record lookup by unique path and query parameters
"""
from flask import jsonify, make_response, request
from werkzeug import url_fix

from ishmael import app
from ishmael.dbservice import get_mongodb_db_collection
from ishmael.restservice import get_urlinfo
from ishmael.utils import (get_response_template, tailor_app_http_headers, 
                           make_qs_list, qs_sort, get_app_message)
from requests import codes
import os
import urlparse

# search mongodb by netloc, path and/or query string
def get_urlinfo_by_path(urlpath, **kwargs):
    # get url collection
    url_coll = get_mongodb_db_collection(app.config['MONGODB_URLS'])

    # prepare url path for query
    url_parse_result = urlparse.urlsplit(url_fix('http://' + urlpath))
    netloc = url_parse_result.netloc.lower()
    path = url_parse_result.path

    # initialize record set
    record_set = {}

    # query database by exact search
    if 'qs' in kwargs and len(kwargs['qs']) > 0:
        # exact search on complete url netloc, path and all query string members
        app.logger.debug('path query ==> {netloc : \'' + netloc + '\', path : \'' + path + 
                         '\', qs : \'' + str(qs_sort(kwargs['qs'])) + '\'}')
        record_set = url_coll.find({'netloc' : netloc, 'path' : path, 
                                    'qs' : qs_sort(kwargs['qs']) })
    else:
        # exact search on complete url netloc, path; no query string so restrict results
        app.logger.debug('path query ==> {netloc : \'' + netloc + '\', path : \'' + path + 
                         '\', qs : {$exists : false}}')
        record_set = url_coll.find({'netloc' : netloc, 'path' : path,  
                                    'qs' : {'$exists':False}})
    return record_set

# Find an exact match
@app.route('/urlinfo/<string:api_version>/path/<path:path>', methods = ['GET'])
@tailor_app_http_headers
def find_urlinfo_by_path(api_version, path):    # check if API version requested is active
    if api_version not in app.config['API_VERSION_ACTIVE']: abort(codes.NOT_FOUND)
    rest_response, rest_response_code = get_urlinfo(api_version, get_urlinfo_by_path, path, 
                                                    qs=request.query_string, search=False)
    return make_response(jsonify(rest_response), rest_response_code)

# Error response when no url path is entered
@app.route('/urlinfo/<string:api_version>/path/', methods = ['GET'])
def missing_data_urlinfo_by_path(api_version):
    if api_version not in app.config['API_VERSION_ACTIVE']: abort(codes.NOT_FOUND)

    # produce error response
    rest_response = get_response_template(codes.UNPROCESSABLE_ENTITY, 'fail', api_version)
    rest_response['data'] = {'path' : 'url required: ' + request.path.rstrip('/') + get_app_message('path_api_example'),
                             'message': get_app_message('path_api_desc')}

    # return response as json with success status code in header
    return make_response(jsonify(rest_response), codes.UNPROCESSABLE_ENTITY)
