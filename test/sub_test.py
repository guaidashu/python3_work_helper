"""
Create by yy on 2019/9/24
"""
import re

from tool_yy import debug

if __name__ == '__main__':
    s = "<a></a><a></a>"
    data = re.sub("<a>[\w\W]*?</a>", "this ", s)
    debug(data)
