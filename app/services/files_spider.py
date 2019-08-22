"""
Create by yy on 2019-08-21
"""
from tool_yy import debug, Thread, curl_data


class FilesSpider(Thread):
    def __init__(self, init_db=None):
        super().__init__()
        self.db = init_db("GAME_DATABASE_CONFIG")

    def __del__(self):
        pass

    def run(self):
        self.handle()

    def handle(self):
        url = "https://waznygry.pl/fonts/icons.woff2?79622105"
        data = curl_data(url, referer="https://waznygry.pl/styles/main.mobile.min.css?v=2182019515", header={
            "origin": "https://waznygry.pl"
        })
        with open("static/spider/icons.woff2", "wb") as f:
            f.write(data)
            f.close()
        # self.start_thread()
