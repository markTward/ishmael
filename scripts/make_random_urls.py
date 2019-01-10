#i -*- coding: utf-8 -*-
from import_utils import create_url
from pymongo import MongoClient
from werkzeug import url_fix
import config
import datetime
import os
import random
import string
import sys
import urllib
import urlparse

# establish db client for current environment
sys.path.append('..')
app_config = getattr(config,os.environ['ISHMAEL_CONFIG'])
client = MongoClient(app_config.MONGODB_URI)
db = client[app_config.MONGODB_DB]

print app_config
print client
print db

def id_gen_basic(size=6, chars=unicode(string.ascii_letters + string.digits + '_-')):
    return ''.join(random.choice(chars) for x in range(size))

#def id_gen_path(size=6, chars=unicode(string.ascii_letters + string.digits + '_-' + u'åÅéÉîÎøØüÜ')):
def id_gen_path(size=6, chars=unicode(string.ascii_letters + string.digits + '_-')):
    return ''.join(random.choice(chars) for x in range(size))

#def id_gen_qs_val(size=6, chars=unicode(string.ascii_letters + string.digits +  u'åÅéÉîÎøØüÜ' + '!@#$%^&*() -_.,;:?=')):
def id_gen_qs_val(size=6, chars=unicode(string.ascii_letters + string.digits + '_-')):
    return ''.join(random.choice(chars) for x in range(size))

def make_urls(n, source):
    rcount = 0
    for i in range(1,n):
        # fake a host
        host = id_gen_basic(random.choice(range(8,24))) + '.' + random.choice(['com','org','net', 'io', 'info'])
        #host = 'melville.' + random.choice(['com','org','net', 'io', 'info'])

        # fake a random number of ports including null
        random_hosts = random.choice(range(1,6))
        for j in range(1,random_hosts):
            # create a random port with an occasional blank one
            r = random.choice(range(1,7))
            port = str(random.choice(range(10000,30000))) if (r%6 != 0) else ''
            # fake multiple page entries per host:port
            random_ports = random.choice(range(1,6))
            for k in range(1,random_ports):
                hostport = host + (':' + port) if port != '' else host
                newentry = {}

                # fake a random number of pages per host:port
                random_pages = random.choice(range(1,6))
                for l in range(1,random_pages):
                    # vary the directory depth for each page
                    random_dir_depth = random.choice(range(1,6))
                    path = ''
                    for m in range(1,random_dir_depth):
                        path = path + id_gen_path(random.choice(range(5,16))) + '/'
                    iurl = 'http://' + hostport + '/' + path + id_gen_path(random.choice(range(5,16))) + '.html'

                    # create multiple entries per page with different query strings 
                    random_qs_args = random.choice(range(1,6))
                    already_has_null_qs = False
                    for page in range(1,random_qs_args):
                        # a creation and verified date
                        cdate = datetime.datetime.utcnow() - datetime.timedelta(days=random.choice(range(10,1000)))
                        vdate = cdate + datetime.timedelta(days=random.choice(range(1,100)))

                        # fake malware designation
                        is_malware = random.choice([True,False])

                        # fake a query string with a random number of k=v args
                        qs_dict = {}
                        qs_str = ''
                        qsrandom = random.choice(range(0,4))
                        for nargs in range(0,qsrandom):
                           # force unicode (for sanity)
                           #k = id_gen_basic(random.choice(range(1,2))).encode('utf8')
                           #v = id_gen_qs_val(random.choice(range(1,2))).encode('utf8')
                           k = id_gen_basic(random.choice(range(1,9))).encode('utf8')
                           v = id_gen_qs_val(random.choice(range(1,9))).encode('utf8')
                           qs_dict[k] = v
                        if qs_dict != {}:
                            qs_str = urllib.urlencode(qs_dict)
                            up = urlparse.urlsplit(url_fix(iurl + '?' + qs_str))
                        else:
                            up = urlparse.urlsplit(url_fix(iurl))

                        # insert the new record 
                        if (qs_dict == {} and not already_has_null_qs) or (qs_dict != {}):
                            id = create_url(db.urls, up.netloc.lower(), up.path, qs_str, is_malware, cdate, vdate, source)
                            already_has_null_qs = True
                            rcount = rcount +  1
                            if rcount % 10001 == 0: print rcount, id, iurl
                            if n < 100: print id, up.netloc.lower(), up.path, up.query

    print 'total records ==>', rcount

if __name__ == '__main__':
    print sys.argv
    if sys.argv[1] != None:
        n = int(sys.argv[1])
    else:
        sys.exit()
    
    if sys.argv[2] != None:
        source = sys.argv[2]
    else:
        source = None
    
    print 'make n, source ==>', n, source
    make_urls(n, source)
