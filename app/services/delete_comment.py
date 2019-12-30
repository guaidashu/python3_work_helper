"""
Create by yy on 2019/12/30
"""
from tool_yy import Thread, debug


class DeleteComment(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        debug("ok")
