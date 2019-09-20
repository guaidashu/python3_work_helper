"""
Create by yy on 2019-08-26
"""
import os
import threading

from bs4 import BeautifulSoup
from tool_yy import debug, curl_data, Thread

from app.services.ebook.change_content import ChangeContent
from app.services.ebook.devide_category import DivideCategory
from app.services.ebook.download_ebook import DownloadEBook
from app.services.ebook.get_cover_image import GetCoverImage

lock = threading.RLock()


class EBookSpider(Thread):
    """
    电子书 爬虫
    """

    def __init__(self, init_db):
        super().__init__()
        self.db = init_db("EBOOK_DATABASE_CONFIG")
        self.table = "book"
        self.url_prefix = "https://www.gutenberg.org"
        self.dict = {
            "Author": ['author', '作者获取出错', self.__get_tr_data],
            "Editor": ['editor', '编辑获取出错', self.__get_tr_data],
            "Title": ['title', '标题获取出错', self.__get_tr_data],
            "Note": ['note', '注解获取出错', self.__get_tr_data],
            "Contributor": ['contributor', '贡献者获取出错', self.__get_tr_data],
            "Language": ['language', '语言获取出错', self.__get_language],
            "LoC Class": ['loc_class', '书籍PQ，分类获取出错', self.__get_tr_data],
            "Subject": ['subject', '学科获取出错', self.__get_tr_data],
            "Category": ['category', '类别获取出错', self.__get_tr_data],
            "EBook-No.": ['ebook_no', '书号获取出错', self.__get_tr_data],
            "Release Date": ['release_date', '发布日期获取出错', self.__get_tr_data],
            "Copyright Status": ['copyright_status', '版权状态获取出错', self.__get_tr_data],
            "Downloads": ['download_status', '下载状态获取出错', self.__get_tr_data],
            "Price": ['price', '价格获取出错', self.__get_tr_data],
            "Translator": ['translator', '译者获取出错', self.__get_tr_data],
            "Uniform Title": ['uniform_title', '统一标题获取出错', self.__get_tr_data],
            "Illustrator": ['illustrator', '插画获取出错', self.__get_tr_data],
            "Commentator": ['commentator', '评论员获取出错', self.__get_tr_data],
            "Annotator": ['annotator', '注解者获取出错', self.__get_tr_data],
            "Contents": ['contents', '内容(描述)获取出错', self.__get_tr_data],
            "LoC No.": ['loc_no', '分类号获取出错', self.__get_tr_data],
            "Author of introduction, etc.": ['author_introduce', '介绍作者获取失败', self.__get_tr_data],
            "Imprint": ['imprint', '版本说明获取失败', self.__get_tr_data],
            "Compiler": ['compiler', '编者Compiler获取出错', self.__get_tr_data],
            "Alternate Title": ['alternate_title', '替代标题获取出错', self.__get_tr_data],
            "Series Title": ['series_title', '系列标题获取出错', self.__get_tr_data]
        }
        self.language = dict()

    def __del__(self):
        self.db.close()

    def run(self):
        # self.handle()
        # download_ebook = DownloadEBook(self)
        # download_ebook.run()
        # get_cover_image = GetCoverImage(self)
        # get_cover_image.run()
        # divide_category = DivideCategory(self)
        # divide_category.run()
        change_content = ChangeContent(self)
        change_content.run()

    def handle(self):
        data = self.__get_page_data()
        bs_4 = BeautifulSoup(data, "html.parser")
        ul_list = self.__get_li_list(bs_4)
        self.start_thread(ul_list, self.__handle, is_test=False)

    def __handle(self, item):
        url = self.__get_url(item)
        if not url:
            return
        url = self.url_prefix + url
        data = self.__get_book_page(url)
        bs_4 = BeautifulSoup(data, "html.parser")
        insert_arr = dict()
        insert_arr['source_url'] = self.__get_source_url(bs_4)
        if not insert_arr['source_url']:
            return
        insert_arr['book_url'] = url
        table_bs_4 = bs_4.find(name="table", attrs={"class": "bibrec"})
        td_list = table_bs_4.find_all(name="td")
        th_list = table_bs_4.find_all(name="th")
        for k, v in enumerate(th_list):
            try:
                key = v.get_text().strip()
                insert_arr[self.dict[key][0]] = self.dict[key][2](td_list[k], self.dict[key][1])
            except Exception as e:
                debug(e)
        result = self.__insert(insert_arr)
        if result != 0:
            debug("数据存储 =====> 成功")
        else:
            debug("数据存储 =====> 失败")

    @classmethod
    def __get_tr_data(cls, bs_4, info):
        """
        获取具体数据
        :param bs_4:
        :return:
        """
        try:
            data = bs_4.get_text().strip()
        except Exception as e:
            data = ""
            debug("{info}, error: {error}".format(info=info, error=e.__str__()))
        return data

    def __get_language(self, bs_4, info):
        """
        获取语言
        :param bs_4:
        :return:
        """
        try:
            try:
                unused = self.language[threading.current_thread().name]
            except Exception as e:
                debug("初始化线程{thread}的language, error: {error}".format(thread=threading.current_thread().name,
                                                                      error=e.__str__()))
                self.language[threading.current_thread().name] = ""
            if self.language[threading.current_thread().name] == "":
                self.language[threading.current_thread().name] = bs_4.get_text().strip()
            else:
                self.language[threading.current_thread().name] = self.language[
                                                                     threading.current_thread().name] + "," + bs_4.get_text().strip()
        except Exception as e:
            debug("{info}, error: {error}".format(info=info, error=e.__str__()))
        return self.language[threading.current_thread().name]

    def __insert(self, insert_arr):
        """
        数据存储函数
        :param insert_arr:
        :return:
        """
        lock.acquire()
        sql = self.db.getInsertSql(insert_arr, "book")
        result = self.db.insert(sql, is_close_db=False)
        self.language[threading.current_thread().name] = ""
        lock.release()
        return result

    @classmethod
    def __get_source_url(cls, bs_4):
        """
        获取资源链接
        :param bs_4:
        :return:
        """
        table = bs_4.find(name="table", attrs={"class": "files"})
        td = table.find(name="td", attrs={"content": "application/epub+zip"})
        try:
            source_url = td.find(name="a").attrs['href']
        except Exception as e:
            source_url = False
            debug("资源链接获取出错，线程终止, error: {error}".format(error=e.__str__()))
        return source_url

    @classmethod
    def __get_url(cls, item):
        """
        获取书籍详情页的 url
        :param item:
        :return:
        """
        try:
            url = item.find(name="a").attrs['href']
        except Exception as e:
            url = False
            debug("书籍url获取出错, 线程停止，error: {error}".format(error=e.__str__()))
        return url

    @classmethod
    def __get_li_list(cls, bs_4):
        """
        获取书籍链接 li的列表
        :return:
        """
        div = bs_4.find(name="div", attrs={"class": "pgdbbylanguage"})
        li_list = div.find_all(name="li")
        return li_list

    @classmethod
    def __get_page_data(cls):
        """
        获取书籍主页面数据
        :return:
        """
        try:
            data = curl_data("https://www.gutenberg.org/browse/languages/es")
        except Exception as e:
            data = ""
        #     debug("get index page data error: {error}".format(error=e))
        # with open("static/spider/ebook_index_page.html", "wb") as f:
        #     f.write(data.encode("utf-8"))
        #     f.close()
        # with open("static/spider/ebook_index_page.html", "rb") as f:
        #     data = f.read().decode("utf-8")
        #     f.close()
        return data

    @classmethod
    def __get_book_page(cls, url):
        """
        获取书籍详情页数据
        :param url:
        :return:
        """
        try:
            data = curl_data(url)
        except Exception as e:
            data = False
            debug("书籍详情页获取失败, error: {error}".format(error=e.__str__()))
        # with open("static/spider/ebook_book_page.html", "wb") as f:
        #     f.write(data.encode("utf-8"))
        #     f.close()
        # with open("static/spider/ebook_book_page.html", "rb") as f:
        #     data = f.read().decode("utf-8")
        #     f.close()
        return data
