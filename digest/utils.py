# -*- encoding: utf-8 -*-

import os

from typing import Any


def write_fixture(name: str, data: Any, mode='wb') -> None:
    with open(os.path.join(os.path.dirname(__file__), 'tests', name), mode) as fio:
        fio.write(data)


def read_fixture(name: str, mode='rb'):
    with open(os.path.join(os.path.dirname(__file__), 'tests', name), mode) as fio:
        return fio.read()


class MockResponse(object):
    def __init__(self, resp_data, code=200, msg='OK'):
        self.resp_data = resp_data
        self.code = code
        self.msg = msg
        self.headers = {'content-type': 'text/plain; charset=utf-8'}

    def read(self):
        return self.resp_data

    def getcode(self):
        return self.code

    def close(self):
        pass
