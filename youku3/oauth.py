from youku3.base import YoukuOpenApi

import requests
import webbrowser
import re
import json
try:
    from urllib.parse import urlencode
except ImportError:
    from urlparse import urlencode


class YoukuOAuth(YoukuOpenApi):
    def __init__(self, proxies=None, **kwargs):
        super(YoukuOAuth, self).__init__(**kwargs)
        self.__use_proxy = 0
        if proxies:
            self.proxies = proxies
            self.__use_proxy = 1
        self.sys_param = {
            'action': '',
            'client_id': self.client_id,
            'timestamp': '',
            'version': '3.0'
        }

    def get_authorize_code(self, redirect_uri):
        '''
        return:
            authorize code
        '''
        url = self.tcp + '://openapi.youku.com/v2/oauth2/authorize?'
        param = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': redirect_uri
        }

        webbrowser.open_new(url + urlencode(param))
        redirect_url = input("Enter the redirect url: ")
        code = re.findall(r'/\?code=(.*)&state=', redirect_url)[-1]
        return code

    def get_access_token(self):
        '''
        Get a access token.
        return:
            access token, refresh token
        '''
        self.sys_param['action'] = 'youku.user.authorize.token.get'
        self.sys_param['timestamp'] = self.get_time()

        # get sign
        other_param = {'code': self.get_authorize_code()}
        sign = self.get_md5_sign(self.sys_param, other_param)
        self.sys_param.update({'sign': sign})

        post_url = self.get_api_url(sys_param=self.sys_param, other_param=other_param)
        del self.sys_param['sign']
        if self.__use_proxy == 1:
            html = requests.post(post_url, proxies=self.proxies)
        else:
            html = requests.post(post_url)

        resp = json.loads(html.text)
        return resp['token']['accessToken'], resp['token']['refreshToken']

    def refresh_access_token(self, refresh_token):
        '''
        Use refresh token to get new access token.
        return:
            access token, refresh token
        '''
        self.sys_param['action'] = 'youku.user.authorize.token.refresh'
        self.sys_param['timestamp'] = self.get_time()

        # get sign
        other_param = {'refreshToken': refresh_token}
        sign = self.get_md5_sign(self.sys_param, other_param)
        self.sys_param.update({'sign': sign})

        post_url = self.get_api_url(sys_param=self.sys_param, other_param=other_param)
        del self.sys_param['sign']
        if self.__use_proxy == 1:
            html = requests.post(post_url, proxies=self.proxies)
        else:
            html = requests.post(post_url)

        resp = json.loads(html.text)
        return resp['token']['accessToken'], resp['token']['refreshToken']
