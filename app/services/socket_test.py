"""
Create by yy on 2019-07-26
"""

__all__ = ['SocketTest']


class SocketTest(object):
    def __init__(self, init_db):
        self.db = init_db("INSOMNIA_MUSIC_DATABASE_CONFIG")

    def __del__(self):
        self.db.closeDB()

    def run(self):
        pass
