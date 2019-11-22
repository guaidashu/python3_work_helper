"""
Create by yy on 2019/11/22
"""
from tool_yy import debug, curl_data

__all__ = ['SubscribeHttp']


class SubscribeHttp(object):
    def __init__(self):
        pass

    def __del__(self):
        pass

    def run(self):
        url = 'http://dat.c4fungames.com/dm/at/lp'
        curl_data(url)
