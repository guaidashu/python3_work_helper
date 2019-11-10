"""
Create by yy on 2019-08-21
"""
import time
import urllib.parse

from tool_yy import debug, Thread, curl_data, md5


class FilesSpider(Thread):
    def __init__(self, init_db=None):
        super().__init__()
        self.db = init_db("GAME_DATABASE_CONFIG")

    def __del__(self):
        pass

    def run(self):
        time_stamp = int(time.time() * 1000)
        debug(int(time_stamp))
        url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx522d8304a0b93f75&redirect_uri=http%3A%2F%2Ffyxqx.fuyuxiangqi.cn%2Fwxtp%2FPageJumpServlet%2Fu94z6dI%3Ftxid%3Da62ab5bb-f5c9-4409-bb45-5bfc7af8f860%26id%3D9991c3cf-e669-459c-9f13-e5874f244a10%26type%3Duser%26upId%3Ddb4ce741-25d7-4d1e-93c5-de938d7ce24f%26askPage%3D1%26t%3D1571304429611%26askType%3D0%26ymdomain%3Dfyxqt.fuyuxiangqi.cn%2Fwxtp%2F&response_type=code&scope=snsapi_userinfo&state=tdahui&connect_redirect=1"
        result = urllib.parse.urlparse(url)
        args = urllib.parse.parse_qs(result.query)
        debug(args)
        debug(urllib.parse.unquote(url))
        call_back_url = "http://fyxqx.fuyuxiangqi.cn/wxtp/PageJumpServlet/u94z6dI?txid=a62ab5bb-f5c9-4409-bb45-5bfc7af8f860&id=9991c3cf-e669-459c-9f13-e5874f244a10&type=user&upId=db4ce741-25d7-4d1e-93c5-de938d7ce24f&askPage=1&t=1571304429611&askType=0&ymdomain=fyxqt.fuyuxiangqi.cn/wxtp/"
        # debug(md5(1567785699))
        # self.test()

    def handle(self):
        # url = "https://i.ytimg.com/vi/9OHkwJpS6u4/hqdefault.jpg?sqp=-oaymwEZCPYBEIoBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLDEO8flAyYWStTIWI3aLoirwz73yg"
        # url = "https://i.ytimg.com/vi/9OHkwJpS6u4/hqdefault.jpg"
        # url = "https://www.google.com/"
        url = "http://192.168.50.177:8083/download"
        # url = "https://www386.hlsmp4.com/token=b2LDM4PEjOWh5XvREsjfdw/1567685699/0.0.0.0/67/f/9b/11b5f88fd13540ae36950a5a0daa19bf-480p.mp4"
        header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
            # "upgrade-insecure-requests": "1"
        }
        data = curl_data(url, value={"name": "ok"}, header=header, open_virtual_ip=True)
        debug(data)
        # with open("static/files/test.mp4", "wb") as f:
        #     f.write(data)
        #     f.close()

    def test(self):
        url = "https://www.crunchyroll.com/videos/anime/popular/ajax_page?pg=3"
        data = curl_data(url, referer="https://www.crunchyroll.com/videos/anime/popular/ajax_page?pg=3", open_virtual_ip=True)
        debug(data)
