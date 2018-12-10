# coding:utf-8

class BadRequestError(Exception):

    def __init__(self, msg):
        self.message = msg

class NotFoundError(Exception):

    def __init__(self, msg):
        self.message = msg


def param_error(param):
    msg = 'Parameters %s is required.' % param
    return msg