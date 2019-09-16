"""
Create by yy on 2019/9/16
"""
from tool_yy import Thread, debug


class ChangeContent(Thread):
    def __init__(self, ebook_spider):
        super().__init__()
        self.ebook_spider = ebook_spider

    def run(self):
        self.handle()

    def handle(self):
        debug("ok")
