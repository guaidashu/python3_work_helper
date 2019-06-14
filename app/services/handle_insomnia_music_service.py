"""
author songjie
"""
from pydub.utils import mediainfo

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

    def handle(self, item):
        self.start_thread(item["file_list"], self.__handle, is_test=False, path=item["path"], name=item["dir_name"])

    def __handle(self, item, path, name):
        music_time = self.__get_music_time(path + name + "/" + item)
        debug(music_time)

    def __get_music_time(self, path):
        song = mediainfo(path)
        music_time = float(song["duration"])
        debug(music_time)
        music_time = int(music_time + 0.5)
        minutes = self.__get_minutes(music_time)
        time = {
            "second": music_time,
            "minutes": minutes
        }
        return time

    def __get_minutes(self, music_time):
        s = str(music_time // 60) + ":" + str(music_time % 60)
        return s
