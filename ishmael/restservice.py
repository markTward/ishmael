# -*- coding: utf-8 -*-
import httplib
from bson.objectid import ObjectId

from ishmael import app
from ishmael.dbservice import get_mongodb_db_collection
from ishmael.utils import get_response_template

# acquire url information from malware data sources
def get_urlinfo(api_version, urlfunc, urlkey, **kwargs):
    try:
        print 'in restservice get_urlinfo', api_version, urlfunc, urlkey
        # attempt to find url using function, key and other optional arguments
        urlcheck = urlfunc(urlkey, **kwargs)

        # set response default values
        rest_response = get_response_template(httplib.OK, 'success', api_version)

        # modify data payload for public consumption
        #rest_response['data'] = make_success_data(api_version, urlcheck)
        rest_response['data'] = {'back from':'restservice'}

        # return response as json with success status code in header
        return (rest_response, httplib.OK)

    except Exception as ex:
        pass

# search mongodb by internal id
def get_urlinfo_by_id(id):
    print 'in get_urlinfO-by_id'
    url_coll = get_mongodb_db_collection(app.config['MONGODB_URLS'])
    print 'url_coll', url_coll
    print 'BEFORE mongodb call record set'
    record_set = {}
    record_set = url_coll.find({'_id' : ObjectId(id)})
    print 'AFTER mongodb call record set'
    return record_set

