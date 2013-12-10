# -*- coding: utf-8 -*-

from flask import request
import datetime

# utility function delivering restful response shell
def get_response_template(code, status, api_version):
    response_template = {'code' : code, 'status': status }
    response_template['metadata'] = {'api_version':api_version, 'response_timestamp':datetime.datetime.utcnow(), 'request':request.url}
    return response_template
