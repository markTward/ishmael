# -*- coding: utf-8 -*-
"""
    utils.py
    common application-wide utilities
"""
from flask import request, make_response
from ishmael import app
from functools import update_wrapper
import urlparse
import datetime

# utility function delivering restful response shell
def get_response_template(code, status, api_version):
    response_template = {'code' : code, 'status': status }
    response_template['metadata'] = {'api_version':api_version, 
                                     'response_timestamp':datetime.datetime.utcnow(), 
                                     'request':request.url,
                                     'server' : app.config['MONGODB_SERVER_ID']}
    return response_template

# produce an ordered list of query string key=value pairs suitable for mongodb multi-key indexing
def make_qs_list(qs):
    pqs = urlparse.parse_qs(qs)
    pqsl = [{k:sorted(v)} for k,v in sorted(pqs.items())]
    return pqsl
    
# produce a sorted query string matching index    
def qs_sort(qs):
    return ('&'.join(sorted(qs.split('&')))).strip('&')

# Decorator modifying HTTP header
def tailor_app_http_headers(f):
    def new_func(*args, **kwargs):
       resp = make_response(f(*args, **kwargs))
       resp.cache_control.no_cache = True
       resp.headers['Content-Language'] = app.config['DEFAULT_LANGUAGE']
       return resp
    return update_wrapper(new_func, f)

# placeholder for reusable application-wide messages and text
def get_app_message(key):
    app_messages = {
        'path_api_desc' : 'search for an exact match on the URL path and query string.  returns 0 or 1 record.',
        'path_api_example' : '/<host:port>/<full_path>/<query_string>',
        'search_api_desc' : 'search for a general match on the URL host, port and path.  returns 0, 1 or many records.',
        'search_api_example' : '/<host:port>/<full_path>/<query_string>',
        'id_api_desc' : 'search for an exact match on the database id assigned to the URL.  returns 0 or 1 record.',
        'db_na' : 'data services unavailable at this time',
        'mongo_client_fail' : 'ERROR: MongoClient() not established',
        'mongo_client_success' : 'SUCCESS: MongoClient() established',
        'except_unknown_issue' : 'unknown issue with request'
        }
    return app_messages.get(key)

# return default scheme for app: http / https
def get_app_scheme():
    return 'https' if ('USE_SSLIFY' in app.config and app.config['USE_SSLIFY']) == True else 'http'
