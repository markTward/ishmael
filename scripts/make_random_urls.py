#i -*- coding: utf-8 -*-
from pymongo import MongoClient
import random
import datetime
import string
import sys
import os 
import urllib
import urlparse
from werkzeug import url_fix

# establish db client for current environment
sys.path.append('..')
import config
app_config = getattr(config,os.environ['ISHMAEL_CONFIG'])

# produce an ordered list of query string key=value pairs suitable for mongodb multi-key indexing
def make_qs_list(qs):
    pqs = urlparse.parse_qs(qs)
    pqsl = [{k:sorted(v)} for k,v in sorted(pqs.items())]
    return pqsl

def qs_sort(qs):
    return ('&'.join(sorted(qs.split('&')))).strip('&')

def make_url_array(url):
    url_array = []
    url_split = url.split('/')
    url_depth = len(url_split)
    for i in range(url_depth):
        if i == 0:
            url_array.append('/'.join(url_split))
        else:
            url_array.append(('/'.join(url_split) + '/'))

        if len(url_split) == 1 and len(url_split[0].split(':')) == 2:
            url_array.append(url_split[0].split(':')[0] + '/')
        url_split.pop(-1)
    return url_array

client = MongoClient(app_config.MONGODB_URI)
db = client[app_config.MONGODB_DB]

def id_gen_basic(size=6, chars=unicode(string.ascii_letters + string.digits + '_-')):
    return ''.join(random.choice(chars) for x in range(size))

def id_gen_path(size=6, chars=unicode(string.ascii_letters + string.digits + '_-' + u'åÅéÉîÎøØüÜ')):
    return ''.join(random.choice(chars) for x in range(size))

def id_gen_qs_val(size=6, chars=unicode(string.ascii_letters + string.digits +  u'åÅéÉîÎøØüÜ' + '!@#$%^&*() -_.,;:?=')):
    return ''.join(random.choice(chars) for x in range(size))

def create_url(coll, netloc, path, qs, is_malware, cdate, vdate):
    # create mongo connection if none provided
    if coll == None:
        c = MongoClient()
        db = c.malwaredb
        coll = db.urls

    # set defaults if nothing provided
    if cdate == None:
        cdate = datetime.datetime.utcnow() - datetime.timedelta(days=random.choice(range(10,1000)))
    if vdate == None:
        vdate = cdate + datetime.timedelta(days=random.choice(range(1,100)))
    if is_malware == None:
        is_malware = random.choice([True,False])

    iurl = 'http://' + netloc + path

    if qs != '':
        up = urlparse.urlsplit(url_fix(iurl + '?' + qs))
    else:
        up = urlparse.urlsplit(url_fix(iurl))

    # prep a new pentry
    newentry = {'netloc' : up.netloc.lower(),
                'path' : up.path,
                'urlfull' : up.netloc.lower() + up.path,
                'created' : cdate,
                'is_malware' : is_malware}

    # create a hash for the qs in not null
    if qs != '':
        newentry['qs'] = qs_sort(qs)
        newentry['qsLIST'] = make_qs_list(qs)

    # add verified and port if not null
    if vdate < datetime.datetime.today(): newentry['verified'] = vdate

    return coll.insert(newentry)

def make_urls(n):
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

                        # add verified and port if not null
                        if vdate < datetime.datetime.today(): newentry['verified'] = vdate

                        # insert the new record 
                        if (qs_dict == {} and not already_has_null_qs) or (qs_dict != {}):
                            try:
                                id = create_url(db.urls, up.netloc.lower(), up.path, qs_str, is_malware, cdate, vdate)
                                already_has_null_qs = True
                                rcount = rcount +  1
                                if rcount % 10001 == 0: print rcount, id, iurl
                                #print id, up.netloc.lower(), up.path, up.query
                            except:
                                print 'INSERT EXCEPTION ==>', newentry
    print 'total records ==>', rcount

if __name__ == '__main__':
    if sys.argv[1] != None:
        n = int(sys.argv[1])
        print 'make n ==>', n
	make_urls(n)
