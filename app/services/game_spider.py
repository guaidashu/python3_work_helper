"""
Create by yy on 2019-08-17
"""


class GameSpider:
    def __init__(self, init_db):
        self.db = init_db("INSOMNIA_MUSIC_DATABASE_CONFIG")

    def __del__(self):
        self.db.close()

    def run(self):
        pass
