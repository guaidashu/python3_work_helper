"""
Create by yy on 2019-08-17
"""
import re
import threading

from bs4 import BeautifulSoup
from tool_yy import debug, curl_data, Thread

lock = threading.RLock()


class GameSpider(Thread):
    def __init__(self, init_db):
        super().__init__()
        self.db = init_db("INSOMNIA_MUSIC_DATABASE_CONFIG")

    def __del__(self):
        self.db.close()

    def run(self):
        self.handle()

    def handle(self):
        data = self.get_index_page_data()
        game_li_list = self.get_game_li_list(data)
        self.start_thread(game_li_list, self.__handle, is_test=True)

    def __handle(self, item):
        try:
            game_page_url = item.find(name="a").attrs['href']
            game_first_page = GameFirstPage(game_page_url, self)
            game_first_page.run()
        except Exception as e:
            debug(e)

    def get_game_li_list(self, data):
        bs_html = BeautifulSoup(data, "html.parser")
        game_ul = bs_html.find_all(name="ul", attrs={"class": "_2tY3C"})
        try:
            game_li = game_ul[0].find_all(name="li", attrs={"class": "_1cn3x"})
        except Exception as e:
            game_li = list()
            debug(e)
        return game_li

    def get_index_page_data(self):
        url = "https://codecanyon.net/search/game"
        # data = curl_data(url=url, open_virtual_ip=True)
        # with open("static/spider/page_index.html", "wb") as f:
        #     f.write(data.encode("utf-8"))
        #     f.close()
        with open("static/spider/page_index.html", "rb") as f:
            data = f.read().decode("utf-8")
            f.close()
        return data


class GameFirstPage:
    def __init__(self, url, game_spider):
        self.url = url
        self.game_spider = game_spider

    def __del__(self):
        pass

    def run(self):
        self.handle()

    def handle(self):
        page_data = self.get_page_data()
        debug(page_data)

    def get_page_data(self):
        data = curl_data(self.url)
        bs_html = BeautifulSoup(data, "html.parser")
        live_url = bs_html.find(name="a", attrs={"class": "live-preview"})
        try:
            live_url = live_url[0]
        except:
            live_url = False
        if not live_url:
            return live_url
        else:
            with open("static/spider/page_first.html", "wb") as f:
                f.write(data.encode("utf-8"))
                f.close()
        return data
