"""
author songjie
"""
import threading

from tool.lib.function import debug, curl_data
from tool.lib.thread import Thread

lock = threading.RLock()


class GetImages(Thread):
    def __init__(self, init_db=None):
        super().__init__()
        self.db = init_db()

    def __del__(self):
        self.db.closeDB()

    def run(self):
        self.handle()

    def handle(self):
        data = self.get_data()
        self.get_images(data, "large", img_url="img_url_large")

    def get_images(self, data, path, img_url, prefix=""):
        self.start_thread(data, self.__get_images, path=path, img_url=img_url, prefix=prefix)

    def __get_images(self, item, path, img_url, prefix):
        page_resource = self.get_page_resource(prefix + item[img_url])
        with open("static/images/{path}/{id}.jpg".format(path=path, id=item['id']), "wb") as f:
            try:
                page_resource = page_resource.encode("utf-8")
            except Exception as e:
                debug(e)
            f.write(page_resource)
            f.close()
            update_data = {
                "status": 1
            }
            condition = ["id={id}".format(id=item['id'])]
            self.__update_data(update_data, "list", condition)

    @classmethod
    def get_page_resource(cls, url):
        data = curl_data(url, open_virtual_ip=True)
        return data

    def __update_data(self, update_data, table, condition):
        update_arr = {
            "table": table,
            "set": update_data,
            "condition": condition
        }
        lock.acquire()
        self.db.update(update_arr, is_close_db=False)
        lock.release()

    def get_data(self):
        data = self.db.select({
            "table": "list",
            "columns": ["id", "img_url", "img_url_large"],
            "condition": ["status=0"]
        }, is_close_db=False)
        return data
