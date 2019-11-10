"""
Create by yy on 2019/10/17
"""
import time

from tool_yy import debug, curl_data, get_cookie


class Liuduoduo(object):
    """
    刷票测试
    """

    def __init__(self):
        self.host = "http://fyxqt.fuyuxiangqi.cn"
        self.path = "/wxtp/web/aipainew/webBarrageAction!getBarrageList.action"
        self.url = self.host + self.path
        self.get_cookie_url = None
        # 微信id， 不变的
        self.wx_id = "a62ab5bb-f5c9-4409-bb45-5bfc7af8f860"
        # 选手的id
        self.id = "9991c3cf-e669-459c-9f13-e5874f244a10"
        self.cookie = None

    def run(self):
        header = self.__get_header()
        params = self.__get_params()
        self.cookie = self.__get_cookie()
        data = curl_data(url=self.url, value=params, header=header, cookie=self.cookie)
        debug(data)
        # self.vote()

    def __get_header(self):
        return {
            "User-Agent": "Mozilla/5.0 (Linux; U; Android 9.0; zh-cn; GT-S5660 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1 MicroMessenger/4.5.255",
            "Referer": self.get_cookie_url,
            "Origin": "http://fyxqt.fuyuxiangqi.cn",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest"
        }

    def __get_params(self):
        return {
            "hdId": self.wx_id,
            "barUserId": self.id,
            "barrageType": "peopleType"
        }

    def __get_cookie(self):
        header = {
            "User-Agent": "Mozilla/5.0 (Linux; U; Android 9.0; zh-cn; GT-S5660 Build/GINGERBREAD) AppleWebKit/533.1 "
                          "(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1 MicroMessenger/4.5.255",
            # "Origin": "http://fyxqt.fuyuxiangqi.cn",
            # "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            # "X-Requested-With": "XMLHttpRequest"
        }
        self.get_cookie_url = "http://fyxqt.fuyuxiangqi.cn/wxtp/PageJumpServlet/e4Lb71x?txid={wx_id}&id={id}&" \
                              "type=user&upId=db4ce741-25d7-4d1e-93c5-de938d7ce24f&askPage=1&t={time_stamp}&askType=0" \
            .format(wx_id=self.wx_id, id=self.id, time_stamp=int(time.time() * 1000))
        debug(self.get_cookie_url)
        # data = curl_data(self.get_cookie_url, header=header)
        # debug(data)
        cookie = get_cookie(self.get_cookie_url, header=header)
        debug(cookie)
        # cookie["user"] = "8e570c43-2745-48b1-9404-5f3a65fc46f1"
        return cookie
        # return {
        #     "JSESSIONID": "540DE6E23E97E70AFCD632EF1CBDC699",
        #     "user": "8e570c43-2745-48b1-9404-5f3a65fc46f1",
        #     "tgw_l7_route": "06914b689b6e3fa4f738ccdbc2fb6dcd"
        # }

    def vote(self):
        url = "http://fyxqt.fuyuxiangqi.cn/wxtp/web/aipainew/aipainewAction!dianji.action?t={time_stamp}".format(
            time_stamp=int(time.time() * 1000))
        params = {
            "id": self.id,
            "hdid": self.wx_id,
            "yz": ""
        }
        header = self.__get_header()
        data = curl_data(url, value=params, cookie=self.cookie, header=header)
        debug(data)
