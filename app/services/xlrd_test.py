"""
Created by yy on 2019/11/10
"""
import re

import xlrd
from tool_yy import debug


class XlrdTest(object):
    def __init__(self):
        """
        init
        """
        self.aim_path = "static/excel/compare.xlsx"
        self.origin_path = "static/excel/10142.xlsx"
        self.aim_excel_data = dict()

    def __del__(self):
        pass

    def run(self):
        self.get_origin_name()
        # debug(self.aim_excel_data)
        self.handle()

    def handle(self):
        """
        :return:
        """
        excel = xlrd.open_workbook(self.origin_path)
        # self.aim_excel_data = self.get_origin_name()
        sheet_list = excel.sheets()
        for sheet in sheet_list:
            self.__handle(sheet)

    def __handle(self, sheet):
        """
        :param sheet: 当前操作的sheet表
        :return:
        """
        row_count = sheet.nrows
        for i in range(row_count):

            if i == 0:
                continue
            row_data = sheet.row_values(i)

            try:
                # 获取到 名字列表
                name = row_data[2].replace(" ", "，")
                name = re.sub("\([\w\W]*?\)", "", name)
                name = name.split("，")
            except:
                name = list()

            self.match(name, sheet, i)
            break

    def match(self, name_list, sheet, row_num):
        """
        :param name_list: 姓名列表
        :param sheet: 当前操作的sheet表
        :param row_num: 行号
        :return:
        """
        tmp_case_num = ""
        for i, name in enumerate(name_list):
            if name == "":
                continue
            if name in self.aim_excel_data:
                if i == 0:
                    tmp_case_num = self.aim_excel_data[name]
                else:
                    if tmp_case_num != self.aim_excel_data[name]:
                        tmp_case_num = tmp_case_num + "，" + self.aim_excel_data[name]

        debug("{name}: {data}".format(name=name_list, data=tmp_case_num))
        sheet.put_cell(row_num, 3, 1, tmp_case_num, 0)

    def get_origin_name(self):
        """
        获取 要匹配的数据 表的所有姓名信息和案号
        :return:
        """
        excel = xlrd.open_workbook(self.aim_path)
        sheet = excel.sheets()[0]
        row_count = sheet.nrows

        tmp_name = list()
        tmp_case_num = ""

        for i in range(row_count):

            if i == 0:
                continue

            row_data = sheet.row_values(i)

            try:
                # 获取到名字
                name = row_data[0]
                # 获取案号
                case_num = row_data[1]
                if name == "":
                    name_list = tmp_name
                    tmp_case_num = tmp_case_num + "，" + case_num
                else:
                    name_list = name.split("，")
                    tmp_case_num = case_num
                    tmp_name = name_list

            except:
                name_list = list()
                tmp_case_num = ""

            for name in name_list:
                self.aim_excel_data[name] = tmp_case_num
