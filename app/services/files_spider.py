"""
Create by yy on 2019-08-21
"""
from tool_yy import debug, Thread, curl_data, md5


class FilesSpider(Thread):
    def __init__(self, init_db=None):
        super().__init__()
        self.db = init_db("GAME_DATABASE_CONFIG")

    def __del__(self):
        pass

    def run(self):
        # debug(md5(1567785699))
        self.handle()

    def handle(self):
        # url = "https://i.ytimg.com/vi/9OHkwJpS6u4/hqdefault.jpg?sqp=-oaymwEZCPYBEIoBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLDEO8flAyYWStTIWI3aLoirwz73yg"
        # url = "https://i.ytimg.com/vi/9OHkwJpS6u4/hqdefault.jpg"
        # url = "https://www.google.com/"
        url = "http://192.168.50.177:8083/download"
        # url = "https://www386.hlsmp4.com/token=b2LDM4PEjOWh5XvREsjfdw/1567685699/0.0.0.0/67/f/9b/11b5f88fd13540ae36950a5a0daa19bf-480p.mp4"
        header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
            # "upgrade-insecure-requests": "1"
        }
        data = curl_data(url, value={"name": "ok"}, header=header, open_virtual_ip=True)
        debug(data)
        # with open("static/files/test.mp4", "wb") as f:
        #     f.write(data)
        #     f.close()
