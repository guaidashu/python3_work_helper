"""
Create by yy on 2019/9/16
"""
import os
import shutil
import threading
import zipfile

from bs4 import BeautifulSoup
from tool_yy import Thread, debug
from tool_yy.lib.helper_context import HelperContext

from app.libs.draw_image import DrawImage

lock = threading.RLock()


class GetCoverImage(Thread, HelperContext):
    def __init__(self, ebook_spider):
        super().__init__()
        self.dir = "static/spider/epub/"
        self.img_path = "static/spider/epub/cover/"
        self.tmp_path = "static/spider/epub/tmp/"
        self.ebook_spider = ebook_spider

    def run(self):
        self.handle()

    def handle(self):
        data = self.get_data()
        self.start_thread(data, self.__handle, is_test=False)

    def __handle(self, item):
        # 设置自动处理错误
        with self.auto_handle_exception(throw_exception_flag=True):
            tmp_dir = self.tmp_path + "{dirname}/".format(dirname=item['id'])
            if not os.path.exists(tmp_dir):
                os.mkdir(tmp_dir)
            filename = self.dir + "{filename}.epub".format(filename=item['id'])
            try:
                self.__unzip(filename, tmp_dir)
                self.__get_cover(tmp_dir, item)
            except Exception as e:
                debug("此电子书 ============================>  无cover图片，删除")
                # self.draw_cover(item)
                self.__delete(item)
                os.remove(self.dir + str(item['id']) + ".epub")
            shutil.rmtree(tmp_dir)

    def __get_cover(self, tmp_dir, item):
        """
        获取封面
        :param tmp_dir:
        :param item:
        :return:
        """
        with open(tmp_dir + "OEBPS/content.opf", "rb") as f:
            data = f.read().decode("utf-8")
            f.close()
        data = BeautifulSoup(data, "html.parser")
        meta = data.find(name="meta", attrs={"name": "cover"})
        if meta is None:
            debug("此电子书 ============================>  无cover图片，删除")
            # self.draw_cover(item)
            self.__delete(item)
            os.remove(self.dir + str(item['id']) + ".epub")
            return
        find = data.find(name="item", attrs={"media-type": "image/jpeg"})
        cover_name = find.attrs['href']
        shutil.move(tmp_dir + "OEBPS/{img_path}".format(img_path=cover_name),
                    self.img_path + "{filename}{ext}".format(filename=item['id'], ext=os.path.splitext(cover_name)[1]))
        debug("id为 {filename} 的电子书封面图 =========>  获取完成".format(filename=item['id']))

    def __delete(self, item):
        lock.acquire()
        result = self.ebook_spider.db.delete({
            "table": "book",
            "condition": ["id={epub_id}".format(epub_id=item['id'])]
        }, is_close_db=False)
        lock.release()
        return result

    def draw_cover(self, item):
        """
        绘制 封面图
        :param item:
        :return:
        """
        img_height = 680
        img_width = 510
        draw_image = DrawImage.instance(mode='RGB', size=(img_width, img_height), color=(139, 37, 0))
        draw_image.set_font(style_file_path="static/font/simsun.ttc", fontsize=50, index=1)
        # 绘制标题 (文字都居中显示)
        draw_image.draw_text(item['title'], ('center', 70), 380, line_height=70)
        # 绘制作者
        draw_image.set_font("static/font/simsun.ttc", fontsize=30)
        draw_image.draw_text(item['author'], ('center', 400), 320, line_height=60)
        draw_image.draw(self.img_path + "{filename}.jpg".format(filename=item['id']))

    def __unzip(self, src, aim_dir):
        """
        解压文件
        :param src:
        :param aim_dir:
        :return:
        """
        file = zipfile.ZipFile(src)
        with self.auto_handle_exception():
            file.extractall(aim_dir)
            file.close()

    def get_data(self):
        data = self.ebook_spider.db.select({
            "table": self.ebook_spider.table,
            "columns": ["id", "title", "author"],
            # "limit": [0, 10]
        }, is_close_db=False)
        return data
