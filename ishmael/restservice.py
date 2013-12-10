# -*- coding: utf-8 -*-
import httplib
from bson.objectid import ObjectId

from ishmael import app
from ishmael.dbservice import get_mongodb_db_collection
from ishmael.utils import get_response_template

# acquire url information from malware data sources
def get_urlinfo(api_version, urlfunc, urlkey, **kwargs):
    try:
        urlcheck = urlfunc(urlkey, **kwargs)
        rest_response = get_response_template(httplib.OK, 'success', api_version)
        #rest_response['data'] = make_success_data(api_version, urlcheck)
        rest_response['data'] = {'back from':'restservice'}
        return (rest_response, httplib.OK)

    except Exception as ex:
        pass

