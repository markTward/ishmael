from werkzeug import url_fix
import datetime
import urlparse

# need access to main app & utilities
import sys
sys.path.append('..')
import ishmael
from ishmael.utils import qs_sort, make_qs_list

def create_url(coll, netloc, path, qs, is_malware, cdate, vdate, source):
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
                'is_malware' : is_malware,
                'source' : source}

    # create a hash for the qs in not null
    if qs != '':
        newentry['qs'] = qs_sort(qs)
        newentry['qsLIST'] = make_qs_list(qs)

    # add verified and port if not null
    if vdate < datetime.datetime.today(): newentry['verified'] = vdate
    return coll.insert(newentry)
