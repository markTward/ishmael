# -*- coding: utf-8 -*-

from flask import jsonify, make_response, request
from werkzeug import url_fix

from ishmael import app
from ishmael.dbservice import get_mongodb_db_collection
from ishmael.restservice import get_urlinfo
from ishmael.utils import get_response_template, tailor_app_http_headers, make_qs_list, qs_sort

import os
import httplib
import urllib
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

    # query database
    if 'search' in kwargs and kwargs['search'] == True:
        # open search
        if 'qs' in kwargs and len(kwargs['qs']) > 0:
            app.logger.debug('dbservice: open search by urlDEPTH and qsLIST')
            app.logger.debug(str(make_qs_list(kwargs['qs'])))
            # positive match for any depth of url netloc, path and any number of query string members
            record_set = url_coll.find({'urlDEPTH' : (netloc + path), 'qsLIST' : {'$all' :  make_qs_list(kwargs['qs'])}})
        else:
            app.logger.debug('dbservice: open search by urlDEPTH')
            # positive match for any depth of url netloc, path
            record_set = url_coll.find({'urlDEPTH' : (netloc + path) })
    return record_set

# Search for all records matching host, port and path criteria
@app.route('/urlinfo/<string:api_version>/search/<path:path>', methods = ['GET'])
@tailor_app_http_headers
def search_urlinfo_by_path(api_version, path):
    if api_version not in app.config['API_VERSION_ACTIVE']: abort(httplib.NOT_FOUND)
    rest_response, rest_response_code = get_urlinfo(api_version, get_urlinfo_by_path, path, qs=request.query_string, search=True)

    # return response as json with success status code in header
    return make_response(jsonify(rest_response), rest_response_code)

# Error response when no search path is entered
@app.route('/urlinfo/<string:api_version>/search', methods = ['GET'])
@app.route('/urlinfo/<string:api_version>/search/', methods = ['GET'])
def urlinfo_by_search_missing_data(api_version):
    # check if API version requested is active
    if api_version not in app.config['API_VERSION_ACTIVE']: abort(httplib.NOT_FOUND)

    # produce error response
    rest_response = get_response_template(httplib.UNPROCESSABLE_ENTITY, 'fail', api_version)
    rest_response['data'] = {'path' : 'url required: ' + request.path.rstrip('/') + '/<host:port>/<full_path>/<query_string>',
                             'message':'search for a general match on the URL host, port and path.  returns 0, 1 or many records.'}

    # return response as json with success status code in header
    return make_response(jsonify(rest_response), httplib.UNPROCESSABLE_ENTITY)
