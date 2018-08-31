# coding:utf-8

import tornado.ioloop
import tornado.web
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from common_methods import http_method

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('hello, this is scrapy-data.')

class DataProduct(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(40)
    @run_on_executor
    def post(self):
        product = http_method.action(self, 'Product')
        print(product)
        self.write(product)
        self.finish()


def main():
    method_list = [
        ('/', MainHandler),
        ('/scrapy_data/product', DataProduct)
    ]
    app = tornado.web.Application(method_list, autoreload=True)
    print('run...')
    app.listen(6666)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()