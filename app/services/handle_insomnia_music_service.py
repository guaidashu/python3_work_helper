"""
author songjie
"""
from tool.lib.db import DBConfig
from tool.lib.function import debug


class HandleInsomniaMusicService(object):
    def __init__(self, db=DBConfig()):
        self.db = db

    def __del__(self):
        self.db.closeDB()

    def get_music_list(self):
        return self.db.select()

    def run(self):
        debug("run")
