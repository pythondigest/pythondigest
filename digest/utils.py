# -*- encoding: utf-8 -*-

import os


def save_fixture(name, data, mode='wb'):
    with open(os.path.join(os.path.dirname(__file__), name), mode) as fio:
        fio.write(data)


def read_fixture(name, mode='rb'):
    with open(os.path.join(os.path.dirname(__file__), name), mode) as fio:
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
