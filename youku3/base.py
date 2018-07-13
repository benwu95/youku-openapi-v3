import time
import hashlib
import json
try:
    from urllib.parse import urlencode
except ImportError:
    from urlparse import urlencode


class YoukuOpenApi(object):
    def __init__(self, client_id, secret_key, tcp='https'):
        self.client_id = client_id
        self.secret_key = secret_key
        if tcp in ['http', 'https']:
            self.tcp = tcp
        else:
            self.tcp = 'https'
        self.url = self.tcp + '://openapi.youku.com/router/rest.json?opensysparams='

    def get_time(self):
        return str(int(time.time()))

    def get_md5_sign(self, sys_param, other_param):
        '''
        https://doc.open.youku.com/?docid=317#anchort4
        '''
        check_param = sys_param
        check_param.update(other_param)
        checksum = ''
        for k in sorted(check_param.keys()):
            checksum += (k + str(check_param[k]))
        return hashlib.md5((checksum + self.secret_key).encode('utf-8')).hexdigest()

    def get_api_url(self, sys_param, other_param, url=None):
        if url is None:
            return self.url + json.dumps(sys_param) + '&' + urlencode(other_param)
        else:
            return url + '&' + urlencode(other_param)
