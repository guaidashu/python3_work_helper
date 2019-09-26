"""
author songjie
"""
from psql_yy import PsqlDB

from app.modules.helper import Helper


def create_helper():
    psql = PsqlDB()
    helper = Helper()
    helper.config.from_object("config.secure")
    helper.config.from_object("config.settings")
    psql.init_helper(helper, False)
    return helper
