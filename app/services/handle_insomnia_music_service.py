"""
author songjie
"""
from tool.lib.function import debug


class HandleInsomniaMusicService(object):
    def __init__(self, init_db=None):
        self.db = init_db("INSOMNIA_MUSIC_DATABASE_CONFIG")

    def __del__(self):
        self.db.closeDB()

    def get_music_list(self):
        return self.db.select({
            "table": "music_list",
            "limit": [0, 10]
        })

    def run(self):
        data = self.get_music_list()
        debug(data)
