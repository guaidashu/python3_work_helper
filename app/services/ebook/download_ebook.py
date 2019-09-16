"""
Create by yy on 2019/9/16
"""
import os

from tool_yy import Thread, curl_data, debug
from tool_yy.lib.helper_context import HelperContext


class DownloadEBook(Thread, HelperContext):
    def __init__(self, ebook_spider):
        super().__init__()
        self.ebook_spider = ebook_spider

    def run(self):
        self.handle()

    def handle(self):
        data = self.get_data()
        self.start_thread(data, self.__handle, is_test=False)

    def __handle(self, item):
        debug("下载电子书：{title}".format(title=item['title']))
        self.__download(item)

    def __download(self, item):
        # 检查文件是否已经存在
        if os.path.exists("static/spider/epub/{filename}.epub".format(filename=item['id'])):
            debug("电子书：{title} ========> 已经存在， 跳过".format(title=item['title']))
            return
        with self.auto_handle_exception(error_callback=self.__error_callback, throw_exception_flag=True, item=item):
            data = curl_data(item['source_url'])
            with open("static/spider/epub/{filename}.epub".format(filename=item['id']), "wb") as f:
                f.write(data)
                f.close()
            debug("电子书：{title} =======> 下载成功".format(title=item['title']))

    def __error_callback(self, item):
        debug("电子书：{title} ========> 下载失败".format(title=item['title']))

    def get_data(self):
        data = self.ebook_spider.db.select({
            "table": self.ebook_spider.table,
            "columns": ["id", "source_url", "title"]
        }, is_close_db=False)
        return data
