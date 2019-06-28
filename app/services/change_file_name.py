"""
author songjie
"""
import re
import threading

from tool.lib.function import debug
from tool.lib.thread import Thread

lock = threading.RLock()


class ChangeFileName(Thread):
    def __init__(self, init_db=None):
        super().__init__()
        self.db = init_db("BLOG_DATABASE_CONFIG")

    def __del__(self):
        self.db.closeDB()

    def run(self):
        data = self.get_image_list()
        self.start_thread(data, self.handle, is_test=False)

    def handle(self, item):
        try:
            show_img = item["show_img"]
            show_img = re.findall("upload/([\w\W]*.)", show_img)[0]
            origin_img = item["origin_img"]
            origin_img = re.findall("upload/([\w\W]*.)", origin_img)[0]
            update_arr = {
                "show_img": show_img,
                "origin_img": origin_img
            }
            lock.acquire()
            self.db.update({
                "table": "blog_article",
                "set": update_arr,
                "condition": ["id={id}".format(id=item["id"])]
            }, is_close_db=False)
            lock.release()
        except:
            pass

    def get_image_list(self):
        select_arr = {
            "table": "blog_article",
            "columns": ["id", "show_img", "origin_img"]
        }
        data = self.db.select(select_arr, is_close_db=False)
        return data
