"""
author songjie
"""
import threading

from tool_yy import curl_data, debug, Thread

lock = threading.RLock()


class GetImages(Thread):
    def __init__(self, init_db=None):
        """
        :param init_db:
        """
        super().__init__()
        self.db = None
        self.init_db = init_db
        self.src_column = ""
        self.aim_column = ""
        self.condition = None
        self.origin_table_name = ""
        self.table_name = ""

    def init(self, db_config_name, src_column, aim_column, origin_table_name, table_name, condition="status=0"):
        """
        :param db_config_name:
        :param src_column:
        :param aim_column:
        :param origin_table_name:
        :param table_name:
        :param condition:
        :return:
        """
        self.db = self.init_db(db_config_name)
        self.src_column = src_column
        self.aim_column = aim_column
        self.origin_table_name = origin_table_name
        self.table_name = table_name
        self.condition = condition

    def __del__(self):
        self.db.closeDB()

    def run(self):
        self.handle()

    def handle(self):
        """
        :return:
        """
        data = self.get_data()
        self.get_images(data, "static/images/large")

    def get_images(self, data, path, prefix=""):
        """
        :param data:
        :param path:
        :param prefix:
        :return:
        """
        self.start_thread(data, self.__get_images, path=path, prefix=prefix)

    def __get_images(self, item, path, prefix):
        """
        :param item:
        :param path:
        :param prefix:
        :return:
        """
        page_resource = self.get_page_resource(prefix + item[self.src_column])
        with open("{path}/{id}.jpg".format(path=path, id=item['id']), "wb") as f:
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
            self.__update_data(update_data, self.table_name, condition)

    @classmethod
    def get_page_resource(cls, url):
        """
        :param url:
        :return:
        """
        data = curl_data(url, open_virtual_ip=True)
        return data

    def __update_data(self, update_data, table, condition):
        """
        :param update_data:
        :param table:
        :param condition:
        :return:
        """
        update_arr = {
            "table": table,
            "set": update_data,
            "condition": condition
        }
        lock.acquire()
        self.db.update(update_arr, is_close_db=False)
        lock.release()

    def get_data(self):
        """
        :return:
        """
        data = self.db.select({
            "table": self.table_name,
            "columns": ["id", self.src_column, self.aim_column],
            "condition": [self.condition]
        }, is_close_db=False)
        return data
