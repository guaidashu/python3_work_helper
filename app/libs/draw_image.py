"""
Create by yy on 2019-09-05
"""
from PIL import ImageFont, Image, ImageDraw
from tool_yy.lib.helper_context import HelperContext


class DrawImage(HelperContext):
    """
    If you want to use this tool,
    you can create an instance by DrawImage.instance or new a DrawImage.
    Then you must:
        draw_image.set_font(style_file_path, fontsize=10)
        for example:
            draw_image.set_font("static/font/simsun.ttc", fontsize=50)
    """

    def __init__(self, image, **kwargs):
        """
        :param image:
        :param kwargs:
        """
        super().__init__()
        self._image = image
        self.draw_image = ImageDraw.Draw(self._image)
        self.width = self._image.width
        self.height = self._image.height
        self.font = None

    def __del__(self):
        pass

    @classmethod
    def instance(cls, new_mode=1, mode='RGB', size=(100, 100), color=0, **kwargs):
        """
        直接新建一个DrawImage实例
        :param new_mode: 实例的模式，是open一个图片还是直接自己创建一个图片
        :param mode:
        :param size:
        :param color:
        :return:
        """
        if new_mode == 2:
            fp = kwargs.setdefault("path", "")
            if fp == "":
                return
            open_mode = kwargs.setdefault("open_mode", "")
            if open_mode == "":
                open_mode = "r"
            image = Image.open(fp, open_mode)
        else:
            image = Image.new(mode, size, color)
        return DrawImage(image, **kwargs)

    @property
    def image(self):
        """
        返回Image类对象，用以用户进行任意操作，更灵活和自由
        :return:
        """
        return self.image

    def draw(self, path):
        """
        绘制图片
        :return:
        """
        self._image.save(path)

    def set_font(self, style_file_path="", fontsize=10, **kwargs):
        """
        设置字体样式(传入文件名，自动读取)，字体大小
        :param style_file_path:
        :param fontsize:
        :return:
        """
        index = kwargs.setdefault("index", 0)
        encoding = kwargs.setdefault("encoding", "")
        layout_engine = kwargs.setdefault("layout_engine", None)
        self.font = ImageFont.truetype(style_file_path, size=fontsize, index=index, encoding=encoding,
                                       layout_engine=layout_engine)

    def get_font_size(self, content):
        """
        获取 要写入的文字的尺寸(根据当前的文字大小计算得出)
        :param content:
        :return: (宽，高) (width, height)
        """
        font_size = self.font.getsize(content)
        font_offset = self.font.getoffset(content)
        return font_size[0] - font_offset[0], font_size[1]

    def draw_text_single_row(self, content, position):
        """
        绘制单行文字
        :param position:
        :param content:
        :return:
        """
        # 判断文字绘制位置
        if isinstance(position, tuple):
            if isinstance(position[0], str):
                pos = self.__get_draw_position(content, position)
            else:
                pos = position
        else:
            pos = (0, 0)
        self.draw_image.text(pos, content, font=self.font)

    def __get_draw_position(self, content, position):
        """
        根据传入的字符串判断绘制的位置
        :param content:
        :param position:
        :return:
        """
        if position[0] == 'center':
            return self.width / 2 - self.get_font_size(content)[0] / 2, position[1]
        if position[0] == 'left':
            return 0, position[1]
        if position[0] == 'right':
            return self.width - self.get_font_size(content)[0], position[1]

    def draw_text(self, content, position, width=None, **kwargs):
        """
        绘制多行文字
        :param position:
        :param width:
        :param content:
        :param kwargs: line_height=given_height(给定行高)
        :return:
        """
        if width is None:
            width = self.width
        length = len(content)
        if length == 0:
            return
        content_size = self.get_font_size(content)
        content_width = content_size[0]
        single_width = int(content_width / length)
        if content_width < width:
            self.draw_text_single_row(content, position)
            return
        # 如果超过了给定的最大宽度 width， 则进行分行绘制，
        # 默认行高间隔可设置 line_height
        line_height = kwargs.setdefault("line_height", content_size[1])
        draw_data = self.__get_draw_data(content, position, int(width / single_width), line_height)
        for data in draw_data:
            self.draw_text_single_row(data['content'], data['position'])

    @classmethod
    def __get_draw_data(cls, content, position, length, line_height):
        """
        多文本写入的时候，进行切分
        :param content:
        :param position:
        :param length:
        :param line_height:
        :return: list({"content": ..., "position": (width, height)}...)
        """
        num = 1
        s = content[0:length]
        draw_data = list()
        while s != '':
            draw_data_dict = dict()
            draw_data_dict['position'] = (position[0], position[1] + line_height * num)
            draw_data_dict['content'] = s
            draw_data.append(draw_data_dict)
            s = content[num * length:length * (num + 1)]
            num = num + 1
        return draw_data
