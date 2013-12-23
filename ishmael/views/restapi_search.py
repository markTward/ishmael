# -*- coding: utf-8 -*-
"""
    restapi_search.py
    record lookup by partial path and any combination 
    of query string parameters
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
import re

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

    # prepare regex of url for search
    url_regx = '^' + re.escape(netloc + path)
    
    # query database
    if 'search' in kwargs and kwargs['search']:
        # open search
        if 'qs' in kwargs and len(kwargs['qs']) > 0:
            app.logger.debug('search query ==> {urlfull : {$regex : /' + str(url_regx) + '/}, ' + 
                             'qsLIST:{$all : ' + str(make_qs_list(kwargs['qs'])) + '}}')

            # positive match for any depth of url netloc, path and any number of query string members
            record_set = url_coll.find({'urlfull' : {'$regex':url_regx}, 
                                        'qsLIST' : {'$all' :  make_qs_list(kwargs['qs'])}})
        else:
            app.logger.debug('search query ==> {urlfull : {$regex : /' + str(url_regx) + '/}}')
            # positive match for any depth of url netloc, path
            record_set = url_coll.find({'urlfull' : {'$regex':url_regx}})
    return record_set

# Search for all records matching host, port and path criteria
@app.route('/urlinfo/<string:api_version>/search/<path:path>', methods = ['GET'])
@tailor_app_http_headers
def search_urlinfo_by_path(api_version, path):
    if api_version not in app.config['API_VERSION_ACTIVE']: abort(codes.NOT_FOUND)
    rest_response, rest_response_code = get_urlinfo(api_version, get_urlinfo_by_path, path, 
                                                    qs=request.query_string, search=True)

    # return response as json with success status code in header
    return make_response(jsonify(rest_response), rest_response_code)

# Error response when no search path is entered
@app.route('/urlinfo/<string:api_version>/search/', methods = ['GET'])
def missing_data_urlinfo_by_search(api_version):
    # check if API version requested is active
    if api_version not in app.config['API_VERSION_ACTIVE']: abort(codes.NOT_FOUND)

    # produce error response
    rest_response = get_response_template(codes.UNPROCESSABLE_ENTITY, 'fail', api_version)
    rest_response['data'] = {'path' : 'url required: ' + request.path.rstrip('/') + get_app_message('search_api_example'),
                             'message': get_app_message('search_api_desc')}

    # return response as json with success status code in header
    return make_response(jsonify(rest_response), codes.UNPROCESSABLE_ENTITY)

