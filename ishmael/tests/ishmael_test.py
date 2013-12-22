"""
    ishmael_test.py
    Simple unit testing for ishmael service
"""
import sys
import unittest
import os

# ishmael modules
sys.path.append('..')
sys.path.append('../..')
import config
import ishmael
from ishmael.views import restapi_path
from requests import codes

class NewTestCase(unittest.TestCase):
    # point testing to development configuration and setup an app context for testing
    def setUp(self):
        self.API = ishmael.app.config['API_VERSION_CURRENT']
        self.app = ishmael.app.test_client()

    # test Status 200/OK for /urlhome/<API>
    def testUrlInfoHomeStatus200(self):
        testurl = '/urlinfo/' + self.API
        r = self.app.get(testurl)
        self.assertEqual(r.status_code,codes.OK)

    # test Status 200/OK for /urlhome/<API>/path
    def testUrlInfoPathStatus200(self):
        testurl = '/urlinfo/' + self.API + '/path/helloishmael'
        r = self.app.get(testurl)
        self.assertEqual(r.status_code, codes.OK)

    # test db service response returned from /urlhome/<API>/path/helloishmael
    def testUrlInfoPathData(self):
        testnetloc = 'melville.io'
        testpath = '/helloishmael'
        testqs = 'call=me'
        rs = restapi_path.get_urlinfo_by_path((testnetloc + testpath), qs=testqs)
        self.assertEqual(rs[0]['netloc']+rs[0]['path'], (testnetloc + testpath))

    # test Status 200/OK for /urlhome/<API>/id
    def testUrlInfoIdStatus200(self):
        testurl = '/urlinfo/' + self.API + '/id/529175d03b17094a7dc2f745'
        r = self.app.get(testurl)
        self.assertEqual(r.status_code, codes.OK)
    
    # test Status 422 UNPROCESSABLE_ENTITY for /urlhome/<API>/id with bad object id
    def testUrlInfoIdStatus422(self):
        testurl = '/urlinfo/' + self.API + '/id/529175d03b17094a7dc2f745a'
        r = self.app.get(testurl)
        self.assertEqual(r.status_code, codes.UNPROCESSABLE_ENTITY)

if __name__ == '__main__':
    unittest.main()
