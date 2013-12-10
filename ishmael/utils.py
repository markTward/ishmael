# -*- coding: utf-8 -*-

from flask import request, make_response
from ishmael import app
from functools import update_wrapper
import datetime

# utility function delivering restful response shell
def get_response_template(code, status, api_version):
    response_template = {'code' : code, 'status': status }
    response_template['metadata'] = {'api_version':api_version, 'response_timestamp':datetime.datetime.utcnow(), 'request':request.url}
    return response_template

# produce an ordered list of query string key=value pairs suitable for mongodb multi-key indexing
def make_qs_list(qs):
    pqs = urlparse.parse_qs(qs)
    pqsl = [{k:sorted(v)} for k,v in sorted(pqs.items())]
    return pqsl
    
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
