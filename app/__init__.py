"""
author songjie
"""
from psql_yy import PsqlDB
from redis_yy import RedisDB

from app.modules.helper import Helper


def create_helper():
    psql = PsqlDB()
    redis = RedisDB()
    helper = Helper()
    helper.config.from_object("config.secure")
    helper.config.from_object("config.settings")
    psql.init_helper(helper, False)
    redis.init_helper(helper, False)
    return helper
