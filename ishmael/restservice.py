# -*- coding: utf-8 -*-
from flask import url_for, make_response, jsonify, request
from ishmael import app
from ishmael.dbservice import get_mongodb_db_collection
from ishmael.utils import get_response_template
import httplib
from bson.objectid import ObjectId

# Create a class to handle API exceptions and produce json-worthy response
class ApiExceptionIssue(Exception):
    def __init__(self, status_code=httplib.BAD_REQUEST, status_type='fail', message=None, data=None):
        Exception.__init__(self)
        self.message = message
        self.data = data
        self.status_code = status_code
        self.status_type = status_type
    def format_exception_response(self):
        exception_response = get_response_template(self.status_code, self.status_type, request.view_args['api_version'])
        exception_response['message'] = self.message
        exception_response['data'] = self.data
        return exception_response

# API exception and error handler producing json response
@app.errorhandler(ApiExceptionIssue)
def api_exceptions(error):
    return make_response(jsonify(error.format_exception_response()), error.status_code)

# acquire url information from malware data sources
def get_urlinfo(api_version, urlfunc, urlkey, **kwargs):
    try:
        urlcheck = urlfunc(urlkey, **kwargs)
        rest_response = get_response_template(httplib.OK, 'success', api_version)
        rest_response['data'] = make_success_data(api_version, urlcheck)
        return (rest_response, httplib.OK)
    except Exception as ex:
        except_type = type(ex).__name__
        if app.config['TESTING']:
            except_info = {}
            except_info['type'] = except_type
            except_info['module'] = type(ex).__module__
        # try to raise a well-formatted jsend-like response based upon type of error
        if except_type in ['ConnectionFailure', 'AutoReconnect']:
            raise ApiExceptionIssue(status_type='error',
                                  status_code=httplib.SERVICE_UNAVAILABLE,
                                  data={'args':ex.args} if app.config['TESTING'] else None,
                                  message=except_type)
        elif except_type == 'InvalidId':
            raise ApiExceptionIssue(status_type='fail',
                                  status_code=httplib.UNPROCESSABLE_ENTITY,
                                  data={type(ex).__name__ : ex.args},
                                  message=except_info if app.config['TESTING'] else None)
        else:
            raise ApiExceptionIssue(status_type='fail',
                                  status_code=httplib.BAD_REQUEST,
                                  data=request.url,
                                  message=except_info if app.config['TESTING'] else 'unknown issue with request')

# Create simple jsend-like response
def make_success_data(version, record_set):
	# raw db fields to be excluded from payload
	exclude_from_payload = ['_id','netloc', 'path', 'urlDEPTH','qs','qsLIST']

	# set common response elements
	data = {'record_count' : record_set.count()}

	if record_set.count() > 0:
		# extract individual records from record set
		data['urls'] = []
		for r in record_set:
			# initialize url record excluding some db fields from payload
			newurl = {k:v for k,v in r.items() if k not in exclude_from_payload}

			# recreate url including with query string if it exists
			if 'qs' in r:
			    newurl['url'] = r['netloc'] + r['path'] + '?' + r['qs']
			else:
			    newurl['url'] = r['netloc'] + r['path']
			# add api home and internal id/self links
			newurl['_links'] = [{'rel' : 'home', 'href' : url_for('get_urlinfo_home', api_version = version, _external = True)}]
			newurl['_links'].append({'rel' : 'self',
				'href' : url_for('find_urlinfo_by_id', api_version = version, urlid = str(r['_id']), _external = True)})
			# flag record found in db
			newurl['is_in_database'] = True

			# append current url to list of record set urls
			data['urls'].append(newurl)
	else:
		# flag record not found in db
		data['is_in_database'] = False
		# provide link to API home
		data['_links'] = [{'rel' : 'home', 'href' : url_for('get_urlinfo_home', api_version = version, _external = True)}]

	return data

