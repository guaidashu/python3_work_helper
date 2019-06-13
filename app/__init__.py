"""
author songjie
"""
from app.modules.helper import Helper


def create_helper():
    helper = Helper()
    helper.config.from_object("config.secure")
    helper.config.from_object("config.settings")
    return helper
