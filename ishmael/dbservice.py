# -*- coding: utf-8 -*-

from pymongo import MongoClient
from ishmael import app

def get_mongodb_client():
	# create mongo db connection pool
	if not hasattr(app, 'db'):
		try:
			app.db = MongoClient().malwaredb
			print ' * ' + __name__ + '.' + inspect.stack()[0][3] + ' : SUCCESS: MongoClient() established' 
			return app.db
		except:
			print ' * ' + __name__ + '.' + inspect.stack()[0][3] + ' : ERROR: MongoClient() not established' 
