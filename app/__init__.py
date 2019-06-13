"""
author songjie
"""
from app.modules.helper import Helper


def create_helper():
    helper = Helper()
    helper.config.from_object("config.secure")
    helper.config.from_object("config.settings")
    helper.init_db_config("INSOMNIA_MUSIC_DATABASE_CONFIG")
    return helper
