# -*- coding: utf-8 -*-
import inspect
from pymongo import MongoClient
from ishmael import app

def get_mongodb_client():
	# create mongo client
	if not hasattr(app, 'mdb_client'):
		try:
			app.mdb_client = MongoClient(app.config['MONGODB_URI'])
			print ' * ' + __name__ + '.' + inspect.stack()[0][3] + ' : SUCCESS: MongoClient() established' 
			return app.mdb_client
		except:
			print ' * ' + __name__ + '.' + inspect.stack()[0][3] + ' : ERROR: MongoClient() not established' 

# search mongodb by internal id
def get_urlinfo_by_id(client, id):
    # initialize a mongodb client
    url_coll = get_mongodb_db_collection(client, app.config.MONGODB_URLS)

    # initialize record set
    record_set = {}

    # find record using internal id
    #app.logger.debug('dbservice: search by ObjectId')
    record_set = url_coll.find({'_id' : ObjectId(id)})

    return record_set
