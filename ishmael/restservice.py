# -*- coding: utf-8 -*-
from flask import url_for, make_response, jsonify, request
from ishmael import app
from ishmael.dbservice import get_mongodb_db_collection
from ishmael.error import ApiExceptionIssue
from ishmael.utils import get_response_template
from bson.objectid import ObjectId
from requests import codes

# acquire url information from malware data sources
def get_urlinfo(api_version, urlfunc, urlkey, **kwargs):
    try:
        urlcheck = urlfunc(urlkey, **kwargs)
        rest_response = get_response_template(codes.OK, 'success', api_version)
        rest_response['data'] = make_success_data(api_version, urlcheck)
        return (rest_response, codes.OK)
    except Exception as ex:
        except_type = type(ex).__name__
        except_info = {}
        if app.config['DEBUG']:
            except_info['type'] = except_type
            except_info['module'] = type(ex).__module__
            
        # try to raise a well-formatted jsend-like response based upon type of error
        if except_type in ['ConnectionFailure', 'AutoReconnect']:
            raise ApiExceptionIssue(status_type='error',
                                  status_code=codes.SERVICE_UNAVAILABLE,
                                  data={'args':ex.args} if app.config['DEBUG'] else None,
                                  message=except_type)
        elif except_type == 'InvalidId':
            raise ApiExceptionIssue(status_type='fail',
                                  status_code=codes.UNPROCESSABLE_ENTITY,
                                  data={type(ex).__name__ : ex.args},
                                  message=except_info if app.config['DEBUG'] else None)
        else:
            raise ApiExceptionIssue(status_type='fail',
                                  status_code=codes.BAD_REQUEST,
                                  data=request.url,
                                  message=except_info if app.config['DEBUG'] else 'unknown issue with request')

# Create simple jsend-like response
def make_success_data(version, record_set):
	# raw db fields to be excluded from payload
	exclude_from_payload = ['_id'] if app.config['DEBUG'] else ['_id','netloc', 'path', 'urlfull','qs','qsLIST']

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

