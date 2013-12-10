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
		rest_response['request.url_charset'] = request.url_charset
		rest_response['request.mimetype'] = request.mimetype
		rest_response['request.is_multhread'] = request.is_multithread
		rest_response['request.user_agent'] = str(request.user_agent)
		rest_response['request.accept_mimetypes'] = str(request.accept_mimetypes.values())
		return make_response(jsonify(rest_response), httplib.NOT_FOUND)
	return render_template('404.html')
