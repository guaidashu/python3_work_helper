"""
Create by yy on 2019/9/27
"""
from redis_yy import RedisDB
from tool_yy import debug


class TestRedis(object):
    def __init__(self, init_db):
        self.redis = init_db('REDIS_CONF')

    def run(self):
        self.redis.set("yy", "怪大叔")
        data = self.redis.get("yy")
        debug(data)
