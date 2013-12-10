# -*- coding: utf-8 -*-

from flask import redirect, url_for, jsonify, make_response
import httplib

from ishmael import app
from ishmael.utils import get_response_template, tailor_app_http_headers

# API Home: redirects to current version
@app.route('/urlinfo', methods = ['GET'])
@app.route('/urlinfo/', methods = ['GET'])
def redirect_urlinfo_current_api():
    return redirect(url_for('get_urlinfo_home', api_version = app.config['API_VERSION_CURRENT']))

# API Current Version
@app.route('/urlinfo/<string:api_version>', methods = ['GET'])
@app.route('/urlinfo/<string:api_version>/', methods = ['GET'])
@tailor_app_http_headers
def get_urlinfo_home(api_version):
    # check if API version requested is active
    if api_version not in app.config['API_VERSION_ACTIVE']: abort(httplib.NOT_FOUND)

    # iniitialize restful response with common elements
    rest_response = get_response_template(httplib.OK, 'success', api_version)

    # generate valid urls and instructions for accessing API
    rest_response['data'] = {'_links':[
#        {'rel':'path',
#        'href':url_for('find_urlinfo_by_path', api_version=app.config['API_VERSION_CURRENT'], path='', _external=True),
#        'message':'search for an exact match on the URL path and query string.  returns 0 or 1 record.'},
#        {'rel':'search',
#        'href':url_for('search_urlinfo_by_path', api_version=app.config['API_VERSION_CURRENT'], path='', _external=True),
#        'message':'search for a general match on the URL host, port and path.  returns 0, 1 or many records.'},
        {'rel':'id',
        'href':url_for('find_urlinfo_by_id', api_version=app.config['API_VERSION_CURRENT'], urlid='', _external=True),
        'message':'search for an exact match on the database id assigned to the URL.  returns 0 or 1 record.'}]}

    # return response as json with success status code in header
    return make_response(jsonify(rest_response), httplib.OK)
