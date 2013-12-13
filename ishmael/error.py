# -*- coding: utf-8 -*-

from flask import make_response, jsonify, request, render_template
from ishmael import app
from ishmael.utils import get_response_template
import httplib

def request_wants_json():
	best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
	return (len(request.accept_mimetypes.values()) == 1 and request.accept_mimetypes.values()[0] == '*/*') or \
			(best == 'application/json' and request.accept_mimetypes[best] > request.accept_mimetypes['text/html'])

# HTTP 404 json response
@app.errorhandler(httplib.NOT_FOUND)
def http_status_404(error=None):
	if request_wants_json():
		rest_response = get_response_template(httplib.NOT_FOUND, 'fail', None)
		rest_response['data'] = None
		rest_response['message'] = error.name
		return make_response(jsonify(rest_response), httplib.NOT_FOUND)
	return render_template('404.html')

# Create a class to handle API exceptions and produce json-worthy response
class ApiExceptionIssue(Exception):
    def __init__(self, status_code=httplib.BAD_REQUEST, status_type='fail', message=None, data=None):
        Exception.__init__(self)
        self.message = message
        self.data = data
        self.status_code = status_code
        self.status_type = status_type
    def format_exception_response(self):
    	api_version = request.view_args['api_version'] if 'api_version' in request.view_args else None
        exception_response = get_response_template(self.status_code, self.status_type, api_version)
        exception_response['message'] = self.message
        exception_response['data'] = self.data
        return exception_response
       
# API exception and error handler producing json response
@app.errorhandler(ApiExceptionIssue)
def api_exceptions(error):
    return make_response(jsonify(error.format_exception_response()), error.status_code)





