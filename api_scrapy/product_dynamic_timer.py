# coding:utf-8
import sys
sys.path.append('../')
import logging
import datetime
from common_methods import db_method
from common_methods import common
from common_methods import except_method
from api_scrapy import product_dynamic
from data_product import get_product_dynamic_data

logging.basicConfig(level=logging.DEBUG,
                    filename='dynamic_info.log',
                    format='%(asctime)s-%(levelname)s/%(module)s(%(lineno)d): %(message)s')

def get_asin_and_platform():
    session = db_method.DBSession()
    asin_platforms = session.query(db_method.Product.asin, db_method.Product.platform).all()
    session.close()
    return asin_platforms

def scrapy_timer():
    asin_platforms = get_asin_and_platform()
    print('asins:%s' % asin_platforms)
    for asin_platform in asin_platforms:
        dynamic_param = {
            'asin': asin_platform[0],
            'platform': asin_platform[1]
        }
        dynamic_today = get_product_dynamic_data(dynamic_param)
        # logging.info('dynamic_today:%s' % dynamic_today)
        if not dynamic_today:
            try:
                common.scrapy_data(dynamic_param.get('asin'),
                                   dynamic_param.get('platform'),
                                   product_dynamic.get_dynamic_info)
            except except_method.NotFoundError as e:
                logging.info('NotFoundError: %s' % e)
            except Exception as e:
                logging.info('Error: %s' % e)

# 定时执行抓取页面信息
def set_timer(timer):
    flag = 0
    while True:
        now = datetime.datetime.now()
        now = now.strftime('%Y-%m-%d %H:%M')
        if now == timer:
            scrapy_timer()
            flag = 1
        else:
            if flag == 1:
                timer = datetime.datetime.fromisoformat(timer)
                timer += datetime.timedelta(hours=8)
                flag = 0


if  __name__ == "__main__":
    print('run...')
    timer = datetime.datetime(2018, 12, 10, 9, 56)
    timer = timer.strftime('%Y-%m-%d %H:%M')
    set_timer(timer)
