"""
Create by yy on 2019/9/16
"""
import threading

from tool_yy import Thread

lock = threading.RLock()


class DivideCategory(Thread):
    def __init__(self, ebook_spider):
        super().__init__()
        self.ebook_spider = ebook_spider

    def run(self):
        self.handle()

    def handle(self):
        data = self.get_data()
        self.start_thread(data, self.__handle, is_test=False)

    def __handle(self, item):
        update_arr = dict()
        update_arr['category_id'] = self.__get_category_id(item['id'])
        self.__update(update_arr, item['id'])

    def __update(self, update_arr, book_id):
        lock.acquire()
        self.ebook_spider.db.update({
            "table": self.ebook_spider.table,
            "condition": ["id={book_id}".format(book_id=book_id)],
            "set": update_arr
        }, is_close_db=False)
        lock.release()

    def __get_category_id(self, book_id):
        return book_id % 6 + 1

    def get_data(self):
        return self.ebook_spider.db.select({
            "table": self.ebook_spider.table,
            "columns": ["id"],
        }, is_close_db=False)
