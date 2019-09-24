"""
Create by yy on 2019/9/16
"""
import os
import re
import shutil
import threading
import zipfile

from bs4 import BeautifulSoup
from tool_yy import Thread, debug
from tool_yy.lib.helper_context import HelperContext

lock = threading.RLock()


class ChangeContent(Thread, HelperContext):
    def __init__(self, ebook_spider):
        super().__init__()
        self.ebook_spider = ebook_spider
        self.dir = "static/spider/epub/"
        self.img_path = "static/spider/epub/cover/"
        self.tmp_path = "static/spider/epub/tmp/"
        self.result_path = "static/spider/epub/result/"

    def run(self):
        """
        启动
        :return:
        """
        self.handle()

    def handle(self):
        """
        具体逻辑调用函数
        通过调用从父类 Thread 继承来的函数 start_thread 发起线程
        :return:
        """
        data = self.get_data()
        self.start_thread(data, self.__handle, is_test=False)

    def __handle(self, item):
        """
        线程执行函数
        :param item:
        :return:
        """
        tmp_dir = self.tmp_path + "{dirname}/".format(dirname=item['id'])
        if not os.path.exists(tmp_dir):
            os.mkdir(tmp_dir)
        filename = self.dir + "{filename}.epub".format(filename=item['id'])
        try:
            self.__unzip(filename, tmp_dir)
            self.change_content(tmp_dir, item, filename)
        except Exception as e:
            debug("change content error: {error}".format(error=e))
        shutil.rmtree(tmp_dir)

    def change_content(self, tmp_dir, item, filename):
        """
        去除内容 发起函数
        然后进行压缩
        :param tmp_dir:
        :param item:
        :param filename:
        :return:
        """
        result = self.__change_content(tmp_dir, item)
        if not result:
            return
        self.compression(tmp_dir, item)

    def __change_content(self, tmp_dir, item):
        """
        去除内容 子执行函数
        :param tmp_dir:
        :param item:
        :return:
        """
        tmp_dir = tmp_dir + "OEBPS/"
        result = self.__change_0_html(tmp_dir, item)
        if not result:
            return False
        result = self.__change_top_ncx(tmp_dir, item)
        return result

    def __change_top_ncx(self, tmp_dir, item):
        """
        改变目录页的内容
        :param tmp_dir:
        :return:
        """
        filename = ""
        for name in os.listdir(tmp_dir):
            if name.endswith("ncx"):
                filename = tmp_dir + name
                break
        if filename == "":
            return False
        with open(filename, "rb") as f:
            data = f.read().decode("utf-8")
        bs4 = BeautifulSoup(data, "xml")
        result = bs4.find_all("navPoint", attrs={"playOrder": "1"})
        try:
            result = result[0].find("text")
            result = str(result)
            debug(result + " ============>    " + "<text>{title}</text>".format(title=item['title']))
            data = re.sub(result, "<text>{title}</text>".format(title=item['title']), data)
        except Exception as e:
            debug(e)
        with open(filename, "wb") as f:
            f.write(data.encode("utf-8"))
        return True

    def __change_0_html(self, tmp_dir, item):
        """
        改变第一页的内容
        :param tmp_dir:
        :return:
        """
        filename = ""
        for name in os.listdir(tmp_dir):
            if name.endswith("-0.htm.html"):
                filename = tmp_dir + name
                break
        if filename == "":
            return False
        with open(filename, "rb") as f:
            data = f.read().decode("utf-8")
        bs4 = BeautifulSoup(data, "html.parser")
        pgheader = bs4.find_all("div", attrs={"class": "pgheader"})
        try:
            unused = pgheader[0]
            pattern = "<div class=\"pgmonospaced pgheader\">[\w\W]*?</div>"
            data = re.sub(pattern, "<div class=\"pgmonospaced pgheader\">{title}</div>".format(title=item['title']),
                          data)
        except Exception as e:
            debug(e)
        top_note = bs4.find_all("table", attrs={"summary": "note"})
        try:
            unused = top_note[0]
            pattern = "<table[\w\W]*?>[\w\W]*?</table>"
            data = re.sub(pattern, "", data)
        except Exception as e:
            debug(e)
        try:
            pattern = "<a tag=\"[\w\W]*?\"/>"
            data = re.sub(pattern, "", data)
            pattern = "<a tag=\"[\w\W]*?\">[\w\W]*?</a>"
        except Exception as e:
            debug(e)
        with open(filename, "wb") as f:
            f.write(data.encode("utf-8"))
        return True

    def compression(self, tmp_dir, item):
        """
        压缩文件 发起函数
        :param tmp_dir:
        :param item:
        :return:
        """
        filename = self.result_path + "{filename}.epub".format(filename=item['id'])
        with zipfile.ZipFile(filename, 'w') as zip_file:
            self.__compression(zip_file, tmp_dir, "")

    def __compression(self, zip_file, tmp_dir, prefix):
        """
        压缩文件 子执行函数 (递归方式)
        :param zip_file:
        :param tmp_dir:
        :param prefix:
        :return:
        """
        for basename in os.listdir(tmp_dir):
            if basename.endswith("DS_Store"):
                continue
            if basename.endswith(".epub"):
                continue
            if os.path.isdir(tmp_dir + basename + "/"):
                self.__compression(zip_file, tmp_dir + basename + "/", basename)
            else:
                zip_file.write(tmp_dir + basename, prefix + "/" + basename, compress_type=zipfile.ZIP_DEFLATED)

    def __unzip(self, src, aim_dir):
        """
        解压文件
        :param src:
        :param aim_dir:
        :return:
        """
        file = zipfile.ZipFile(src)
        with self.auto_handle_exception():
            file.extractall(aim_dir)
            file.close()

    def __delete(self, item):
        """
        删除数据
        :param item:
        :return:
        """
        lock.acquire()
        result = self.ebook_spider.db.delete({
            "table": "book",
            "condition": ["id={epub_id}".format(epub_id=item['id'])]
        }, is_close_db=False)
        lock.release()
        return result

    def get_data(self):
        """
        从数据库获取数据
        :return:
        """
        data = self.ebook_spider.db.select({
            "table": self.ebook_spider.table,
            "columns": ["id", "title", "author"],
            # "limit": [0, 10]
        }, is_close_db=False)
        return data
