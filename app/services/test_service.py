"""
Create by yy on 2019-09-05
"""


class TestService:
    def __set__(self, instance, value):
        print("set")

    def __get__(self, instance, owner):
        print("get")


class A:
    # a = TestService()
    a = 2

    def __init__(self):
        self.b = 3


if __name__ == '__main__':
    a = A()
    a.a = 1

    print(dir(a))
