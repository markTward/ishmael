# -*- coding: utf-8 -*-
"""
	dbservice.py
	application-wide database services
"""
import inspect
from pymongo import MongoClient
from ishmael import app
from ishmael.utils import get_app_message

def get_mongodb_client():
	# create mongo client
	if not hasattr(app, 'mdb_client'):
		try:
			app.mdb_client = MongoClient(app.config['MONGODB_URI'])
			app.logger.debug(inspect.stack()[0][3] + ': ' + get_app_message('mongo_client_success'))
			return app.mdb_client
		except:
			app.logger.debug(inspect.stack()[0][3] + ': ' + get_app_message('mongo_client_fail'))

# attempt to get a mongodb collection
def get_mongodb_db_collection(collection):
    get_mongodb_client()
    db = app.mdb_client[app.config['MONGODB_DB']]
    col = db[collection]
    return col
