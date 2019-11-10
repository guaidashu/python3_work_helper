"""
Created by yy on 2019/11/10
"""
import xlrd
from tool_yy import debug


class XlrdTest(object):
    def __init__(self):
        pass

    def __del__(self):
        pass

    def run(self):
        self.handle()

    def handle(self):
        excel = xlrd.open_workbook("static/excel/1014.xlsx")
        sheet = excel.sheet_by_index(1)
        debug(sheet.cell(0, 0).value)
