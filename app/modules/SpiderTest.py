"""
Create by yy on 2019-08-08
"""
import requests
from tool_yy import debug, curl_data
from lxml import etree


class SpiderTest:
    def __init__(self):
        pass

    def run(self):
        pass

    def test(self):
        # url = "https://www.crunchyroll.com/videos/anime"
        url = "https://www.crunchyroll.com/videos/anime/popular/ajax_page?pg=1"
        res = requests.get(url)
        data = res.text
        debug(data)
        with open("./test.html", "wb") as f:
            f.write(data.encode("utf-8"))
            f.close()
        html = etree.parse("./test.html", etree.HTMLParser())
        result = html.xpath("//*[@id='main_content']//li/@id")
        debug(result)

    def test_ip(self):
        url = "https://a-vrv.akamaized.net/evs/1631771ddd0df6e6f7c60770955fe64f/assets/p/6bbmnx58kgajfsd_,1278465.mp4,1278467.mp4,1278463.mp4,1278461.mp4,1278451.mp4,.urlset/fragment-21-f1-a1-x3.m4s?t=exp=1565753706~acl=/evs/1631771ddd0df6e6f7c60770955fe64f/assets/*~hmac=be0ef2b7b8215367e2069db78781d28627a051399f80b10240d73da945ffc162"
        # url = "https://nl.tan90.club/"
        data = curl_data(
            url=url,
            referer="https://static.crunchyroll.com/vilos/player.html", open_virtual_ip=True)
        with open("test.mp4", "wb") as f:
            f.write(data)
            f.close()
        debug(data)
