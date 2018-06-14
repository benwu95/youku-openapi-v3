import time
import hashlib
import json
try:
    from urllib.parse import urlencode
except ImportError:
    from urlparse import urlencode


class YoukuOpenApi(object):
    def __init__(self, key_file, tcp='https'):
        if tcp in ['http', 'https']:
            self.tcp = tcp
        else:
            self.tcp = 'https'
        self.url = self.tcp + '://openapi.youku.com/router/rest.json?opensysparams='

        self.__use_proxy = 0
        with open(key_file) as f:
            param = json.load(f)
            self.access_token = param['access_token']
            self.client_id = param['client_id']
            self.secret_key = param['secret_key']
            self.redirect_uri = param['redirect_uri']
            if param['proxies']:
                self.proxies = param['proxies']
                self.__use_proxy = 1

    def get_time(self):
        return str(int(time.time()))

    def get_checksum_md5(self, checksum):
        return hashlib.md5(checksum).hexdigest()

    def get_param_checksum(self, param):
        checksum = ''
        for k in sorted(param.keys()):
            checksum += (k + str(param[k]))
        return checksum

    def get_api_url(self, sys_param, other_param, url=None):
        if url is None:
            return self.url + json.dumps(sys_param) + '&' + urlencode(other_param)
        else:
            return url + '&' + urlencode(other_param)
