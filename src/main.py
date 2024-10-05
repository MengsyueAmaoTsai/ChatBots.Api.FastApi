import sys

from builder import WebApplication


class IMyService:
    """"""


class MyService(IMyService):
    pass


class IOtherService:
    """"""


class OtherService(IOtherService):
    pass


builder = WebApplication.create_builder(sys.argv)
