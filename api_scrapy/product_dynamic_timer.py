# coding:utf-8

import datetime
from common_methods import db_method
from common_methods import common
from api_scrapy import product_dynamic
from data_product import get_product_dynamic_data

def get_asins():
    session = db_method.DBSession()
    asins = session.query(db_method.Product.asin).all()
    session.close()
    asin_list = [asin[0] for asin in asins]
    return asin_list

def scrapy_timer():
    asin_list = get_asins()
    for asin in asin_list:
        dynamic_param = {'asin': asin}
        dynamic_today = get_product_dynamic_data(dynamic_param)
        if not dynamic_today:
            try:
                common.scrapy_data(asin, product_dynamic.get_dynamic_info)
            except:
                pass

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
                timer += datetime.timedelta(days=1)
                flag = 0


if __name__ == "__main__":
    timer = datetime.datetime(2018, 9, 4, 10, 29)
    timer = timer.strftime('%Y-%m-%d %H:%M')
    set_timer(timer)