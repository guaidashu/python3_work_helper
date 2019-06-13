"""
author songjie
"""
from tool.lib.db import DBConfig


class HandleInsomniaMusic(object):
    def __init__(self):
        self.db = DBConfig()

    def __del__(self):
        self.db.closeDB()
