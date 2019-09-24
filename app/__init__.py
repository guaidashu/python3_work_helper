"""
author songjie
"""
from psql_yy import PsqlDB

from app.modules.helper import Helper

psql = PsqlDB()


def create_helper():
    helper = Helper()
    helper.config.from_object("config.secure")
    helper.config.from_object("config.settings")
    psql.init_helper(helper, False)
    return helper
