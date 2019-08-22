"""
Create by yy on 2019-08-17
"""
import threading
from time import sleep

from bs4 import BeautifulSoup
from tool_yy import debug, curl_data, Thread

lock = threading.RLock()


class GameSpider(Thread):
    def __init__(self, init_db):
        super().__init__()
        self.db = init_db("GAME_DATABASE_CONFIG")

    def __del__(self):
        self.db.close()

    def run(self):
        self.distribution_category()
        # self.handle()

    def handle(self):
        data = self.__get_index_page_data("https://codecanyon.net/search/game?page=46")
        data = BeautifulSoup(data, "html.parser")
        page, is_continue = self.__get_next_page(data)
        current_page = 46
        while is_continue:
            game_li_list = self.__get_game_li_list(data)
            self.start_thread(game_li_list, self.__handle, is_test=False)
            debug("第{page}页结束".format(page=current_page))
            current_page = current_page + 1
            for s in range(15):
                debug("开始倒计时：{time}秒".format(time=s))
                sleep(1)
            data = self.__get_index_page_data(page)
            will_get_page = page
            data = BeautifulSoup(data, "html.parser")
            page, is_continue = self.__get_next_page(data)
            if not is_continue:
                for s in range(100):
                    debug("开始倒计时：{time}秒".format(time=s))
                    sleep(1)
                data = self.__get_index_page_data(will_get_page)
                data = BeautifulSoup(data, "html.parser")
                page, is_continue = self.__get_next_page(data)

    def __handle(self, item):
        try:
            game_page_url = item.find(name="a").attrs['href']
            game_page = GamePage(game_page_url, self)
            game_page.run()
        except Exception as e:
            debug(e)

    @classmethod
    def __get_game_li_list(cls, bs_html):
        game_ul = bs_html.find_all(name="ul", attrs={"class": "_2tY3C"})
        try:
            game_li = game_ul[0].find_all(name="li", attrs={"class": "_1cn3x"})
        except Exception as e:
            game_li = list()
            debug(e)
        return game_li

    @classmethod
    def __get_next_page(cls, data):
        next_page = data.find(name="a", attrs={"class", "k89zG"})
        is_continue = True
        try:
            next_page = "https://codecanyon.net" + next_page.attrs['href']
        except Exception as e:
            debug("get next page error: {error}".format(error=e.__str__()))
            next_page = ""
            is_continue = False
        return next_page, is_continue

    @classmethod
    def __get_index_page_data(cls, url):
        data = curl_data(url=url, open_virtual_ip=True)
        # with open("static/spider/page_index.html", "wb") as f:
        #     f.write(data.encode("utf-8"))
        #     f.close()
        # with open("static/spider/page_index.html", "rb") as f:
        #     data = f.read().decode("utf-8")
        #     f.close()
        return data

    def distribution_category(self):
        """
        分配分类  一共六个分类
        :return:
        """
        data = self.db.select({
            "table": "game"
        }, is_close_db=False)
        for item in data:
            self.__update(item)

    def __update(self, item):
        category = item["id"] % 6 + 1
        update_arr = {
            "table": "game",
            "condition": ["id={id}".format(id=item["id"])],
            "set": {
                "category": category
            }
        }
        lock.acquire()
        self.db.update(update_arr, is_close_db=False)
        lock.release()


class GamePage:
    def __init__(self, url, game_spider):
        self.url = url
        self.game_spider = game_spider

    def __del__(self):
        pass

    def run(self):
        self.handle()

    def handle(self):
        game_url, data = self.__get_page_data()
        if not game_url:
            return
        self.__handle(game_url, data)

    def __handle(self, game_url, data):
        insert_arr = dict()
        data = BeautifulSoup(data, "html.parser")
        insert_arr['game_url'] = self.__get_game_url(game_url)
        insert_arr['title'] = self.__get_title(data)
        insert_arr['game_describe'] = self.__get_describe(data)
        insert_arr['img'] = self.__get_img(data)
        insert_arr['cover_img'] = self.__get_cover_img(data)
        if insert_arr['game_url'] != '':
            self.__insert(insert_arr)

    def __insert(self, insert_arr):
        lock.acquire()
        sql = self.game_spider.db.getInsertSql(insert_arr, "game")
        result = self.game_spider.db.insert(sql, is_close_db=False)
        lock.release()
        if result == 0:
            debug("游戏：{name} ============> 插入成功".format(name=insert_arr['title']))
        else:
            debug("游戏：{name} ============> 插入成功".format(name=insert_arr['title']))

    @classmethod
    def __get_cover_img(cls, data):
        cover_img = data.find(name="div", attrs={"class": "item-preview-image__gallery"})
        cover_str = ""
        try:
            cover_img = cover_img.find_all(name="a")
            for k, item in enumerate(cover_img):
                if k == 0:
                    cover_str = item.attrs['href']
                else:
                    cover_str = cover_str + "," + item.attrs['href']
        except Exception as e:
            debug("get cover img error: {error}".format(error=e.__str__()))
            cover_str = ""
        return cover_str

    @classmethod
    def __get_img(cls, data):
        img_bs4 = data.find(name="div", attrs={"class": "-preview-live"})
        try:
            img_bs4 = img_bs4.find(name="img")
            img_bs4 = img_bs4.attrs['src']
        except Exception as e:
            debug("get img error: {error}".format(error=e.__str__()))
            img_bs4 = ""
        return img_bs4

    def __get_game_url(self, game_url):
        data = self.__get_frame_page(game_url)
        data = BeautifulSoup(data, "html.parser")
        game_url = data.find(name="iframe", attrs={"class": "full-screen-preview__frame"})
        try:
            game_url = game_url.attrs['src']
        except Exception as e:
            debug("get game_url error: {error}".format(error=e.__str__()))
            game_url = ""
        return game_url

    @classmethod
    def __get_frame_page(cls, url):
        url = "https://codecanyon.net" + url
        data = curl_data(url, open_virtual_ip=True)
        # with(open("static/spider/game_frame_page.html", "rb")) as f:
        #     data = f.read().decode("utf-8")
        #     f.close()
        # with open("static/spider/game_frame_page.html", "wb") as f:
        #     f.write(data.encode("utf-8"))
        #     f.close()
        return data

    @classmethod
    def __get_title(cls, data):
        try:
            title_bs4 = data.find(name="div", attrs={"class": "item-header__title"})
            title_bs4 = title_bs4.find(name="h1").get_text().strip()
        except Exception as e:
            debug("get title error: {error}".format(error=e.__str__()))
            title_bs4 = ""
        return title_bs4

    @classmethod
    def __get_describe(cls, data):
        try:
            describe = data.find(name="div", attrs={"class": "user-html__with-lazy-load"})
            describe = str(describe)
        except Exception as e:
            debug("get describe error: {error}".format(error=e.__str__()))
            describe = ""
        return describe

    def __get_page_data(self):
        data = curl_data(self.url)
        # with open("static/spider/page_first.html", "rb") as f:
        #     data = f.read().decode("utf-8")
        #     f.close()
        bs_html = BeautifulSoup(data, "html.parser")
        live_url = bs_html.find(name="a", attrs={"class": "live-preview"})
        try:
            live_url = live_url.attrs['href']
        except Exception as e:
            live_url = False
            debug("游戏播放页链接获取失败，error：" + e.__str__())
        if not live_url:
            return live_url, None
        else:
            # with open("static/spider/page_first.html", "wb") as f:
            #     f.write(data.encode("utf-8"))
            #     f.close()
            pass
        return live_url, data


class GameImage:
    def __init__(self, game_spider):
        self.game_spider = game_spider

    def __del__(self):
        pass

    def run(self):
        self.handle()

    def handle(self):
        pass
        # self.__handle(data)
