"""
author songjie
"""
import re
import shutil
import threading

from pydub.utils import mediainfo

from app.libs.get_file_info import GetFileInfo
from tool.lib.function import debug
from tool.lib.thread import Thread

lock = threading.RLock()


class HandleInsomniaMusicService(Thread):
    def __init__(self, init_db=None):
        Thread.__init__(self)
        self.aim_pos = "/Volumes/资料/insomnia_music/music_finally/"
        self.db = init_db("INSOMNIA_MUSIC_DATABASE_CONFIG")

    def __del__(self):
        self.db.closeDB()

    def run(self):
        file_list = self.get_file_list()
        self.start_thread(file_list["dir_list"], self.handle, is_test=False)

    def get_file_list(self):
        get_file_info = GetFileInfo("/Volumes/资料/insomnia_music/music_final", "", level=2)
        # get_file_info = GetFileInfo("static", "", level=2)
        return get_file_info.get_file_list()

    def handle(self, item):
        # 存储类型并获得对应的类型的主键id 值
        lock.acquire()
        category_id = self.__insert({"name": item["dir_name"]}, "music_category")
        lock.release()
        # category_id = 1
        self.start_thread(item["file_list"],
                          self.__handle,
                          is_test=False,
                          path=item["path"],
                          name=item["dir_name"],
                          category_id=category_id)

    def __handle(self, item, path, name, category_id):
        insert_arr = dict()
        seconds, minutes = self.__get_music_time(path + name + "/" + item)
        singer, song = self.__get_singer_and_name(item)
        insert_arr["singer"] = singer
        insert_arr["minutes"] = minutes
        insert_arr["second"] = seconds
        insert_arr["name"] = song
        insert_arr["category"] = category_id
        result = self.__insert(insert_arr, "music_list")
        if result:
            shutil.copy(path + name + "/" + item, self.aim_pos + str(result) + ".mp3")
        debug(name + " => " + item)

    def __insert(self, insert_arr, table):
        lock.acquire()
        sql = self.db.getInsertSql(insert_arr, table)
        result = self.db.insertLastId(sql, is_close_db=False)
        lock.release()
        return result

    def __get_music_time(self, path):
        song = mediainfo(path)
        try:
            music_time = float(song["duration"])
            music_time = int(music_time + 0.5)
            minutes = self.__get_minutes(music_time)
        except:
            music_time = "00:00"
            minutes = "00:00"
        return music_time, minutes

    def __get_minutes(self, music_time):
        minutes = music_time // 60
        if minutes < 10:
            minutes = "0" + str(minutes)
        seconds = music_time % 60
        if seconds < 10:
            seconds = "0" + str(seconds)
        s = str(minutes) + ":" + str(seconds)
        return s

    def __get_singer_and_name(self, item):
        singer = re.findall("([\w\W]*?) - ([\w\W]*?)\.mp3", item)
        try:
            return singer[0][0], singer[0][1]
        except:
            return "Get singer error", "Get song name error"
