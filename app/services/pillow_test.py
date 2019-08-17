"""
Create by yy on 2019-07-29
"""
from PIL import Image


class PillowTest:
    def __init__(self, init_db):
        self.db = init_db("INSOMNIA_MUSIC_DATABASE_CONFIG")

    def run(self):
        img = Image.open("app/test.jpeg")
        img.save("test.jpg", quality=10)
