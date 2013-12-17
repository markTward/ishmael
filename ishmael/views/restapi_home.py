# -*- coding: utf-8 -*-

from flask import redirect, url_for, jsonify, make_response
from ishmael import app
from ishmael.utils import get_response_template, tailor_app_http_headers, get_app_message
from requests import codes

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
    if api_version not in app.config['API_VERSION_ACTIVE']: abort(codes.NOT_FOUND)

    # iniitialize restful response with common elements
    rest_response = get_response_template(codes.OK, 'success', api_version)

    # generate valid urls and instructions for accessing API
    rest_response['data'] = {'_links':[
        {'rel':'path',
        'href':url_for('find_urlinfo_by_path', api_version=app.config['API_VERSION_CURRENT'], 
                       path='', _external=True),
        'message' : get_app_message('path_api_desc')},
        {'rel':'search',
        'href':url_for('search_urlinfo_by_path', api_version=app.config['API_VERSION_CURRENT'], 
                       path='', _external=True),
        'message': get_app_message('search_api_desc')},
        {'rel':'id',
        'href':url_for('find_urlinfo_by_id', api_version=app.config['API_VERSION_CURRENT'], 
                       urlid='', _external=True),
        'message': get_app_message('id_api_desc')}]}

    # return response as json with success status code in header
    return make_response(jsonify(rest_response), codes.OK)
