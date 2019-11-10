"""
Create by yy on 2019/9/24
"""
from tool_yy import debug


class TestPsql(object):
    def __init__(self, init_db):
        self.db = init_db('POSTGRESQL_TEST_CONFIG')

    def run(self):
        self.db.insert({
            "table": "p_user",
            "username": "guaidashu"
        }, is_close_db=False)
        debug("ok")
