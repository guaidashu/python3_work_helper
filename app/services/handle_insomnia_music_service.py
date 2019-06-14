"""
author songjie
"""
from app.libs.get_file_info import GetFileInfo
from tool.lib.function import debug
from tool.lib.thread import Thread


class HandleInsomniaMusicService(Thread):
    def __init__(self, init_db=None):
        Thread.__init__(self)
        self.db = init_db("INSOMNIA_MUSIC_DATABASE_CONFIG")

    def __del__(self):
        self.db.closeDB()

    def run(self):
        file_list = self.get_file_list()
        self.start_thread(file_list["dir_list"], self.handle, is_test=True)

    def get_file_list(self):
        get_file_info = GetFileInfo("/Volumes/资料/insomnia_music/music_final", "", level=2)
        return get_file_info.get_file_list()

    def get_music_list(self):
        pass

    def handle(self, item):
        self.start_thread(item["file_list"], self.__handle, is_test=True, )

    def __handle(self, item):
        debug(item)
