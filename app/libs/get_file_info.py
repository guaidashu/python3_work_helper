"""
author songjie
"""
import os


class GetFileInfo(object):
    def __init__(self, path, name="", aim_pos=None, level=1):
        """
        :param path: 要读取的文件(夹)位置 The path which will be read
        :param name: 要读取的文件(夹)民 The file name which will be read
        :param aim_pos: 目标存放位置 The position that aim will store
        :param level: 要读取的层级，默认为第一层
        """
        self.path = path
        self.name = name
        self.file_list = {
            "path": path,
            "dir_name": name,
            "file_list": [],
            "dir_list": []
        }
        self.level = level
        if not aim_pos:
            self.aim_pos = path

    def __del__(self):
        pass

    def get_file_list(self):
        """
        获取文件夹内的文件列表，并存入一个数组
        :return:
        """
        # 如果刚开始传入的就是文件, 而不是一个文件夹，则直接加入结果列表返回
        if os.path.isfile(self.path + "/" + self.name):
            self.file_list["file_list"].append(self.name)
            return self.file_list
        self.file_list = self.handle_file_info(self.path, self.name, 1)
        return self.file_list

    def handle_file_info(self, path, name, current_level):
        """
        具体处理函数
        :param name: 文件名
        :param path: 文件(夹)路径
        :param current_level: 文件要遍历的层级
        :return:
        """
        if current_level > self.level:
            return False
        file_list = {
            "path": path,
            "dir_name": name,
            "file_list": [],
            "dir_list": []
        }

        files_path = path + "/" + name
        files = os.listdir(files_path)
        for item in files:
            file_name = files_path + "/" + item
            if os.path.isfile(file_name):
                file_list["file_list"].append(item)
            if os.path.isdir(file_name):
                result = self.handle_file_info(files_path, item, self.get_current_level(current_level))
                if result:
                    file_list["dir_list"].append(result)
        return file_list

    def get_current_level(self, current_level):
        return current_level + 1
