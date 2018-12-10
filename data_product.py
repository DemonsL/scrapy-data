# coding:utf-8
import time
from common_methods import db_method
from common_methods import common
from common_methods import except_method
from common_methods import test_common
from api_scrapy import product_info
from api_scrapy import product_dynamic


# 添加多个asin到商品信息表
def set_product_data(params):
    resp = {
        'SuccessResponse': True
    }
    try:
        db_method.add_product_data(params)
    except Exception as e:
        resp['Error'] = str(e)
        return resp
    return resp

# 通过asin返回商品信息
def get_product_data(params):
    product_data = None
    product_dict = {}
    asin = params.get('asin', None)
    platform = params.get('platform', None)
    table_name = db_method.Product
    # 返回测试数据
    test = params.get('test', None)
    if test:
        table_name = test_common.TestProduct
    try:
        product_data = db_method.execute_sql(db_method.product_select_sql, table_name, params)
    except Exception as e:
        product_dict['Error'] = str(e)
        return product_dict

    if product_data:
        product_dict = [data.data_to_dict() for data in product_data]
    # 没有测试数据返回空
    elif test:
        product_dict = {}
    else:
        # 数据库没有数据则进行爬取
        try:
            product_dict = common.scrapy_data(asin, platform, product_info.get_product_info)
        except except_method.NotFoundError as e:
            product_dict['NotFoundError'] = str(e)
            return product_dict
        except Exception as e:
            product_dict['Error'] = str(e)
            return product_dict

        # 是否有当天动态数据
        dynamic_param = {
            'asin': asin,
            'platform': platform
        }
        dynamic_today = get_product_dynamic_data(dynamic_param)
        if not dynamic_today:
            try:
                common.scrapy_data(asin, platform, product_dynamic.get_dynamic_info)
            except except_method.NotFoundError as e:
                product_dict['NotFoundError'] = str(e)
            except Exception as e:
                print('dynamic_error: %s' % e)

    return product_dict

# 通过asin返回商品动态信息
def get_product_dynamic_data(params):
    price_unit = {
        'azcm': 'USD',
        'azca': 'CAD',
        'azde': 'EUR',
        'azes': 'EUR',
        'azfr': 'EUR',
        'azit': 'EUR',
        'azin': 'INR',
        'azcn': 'CNY',
        'aznl': 'EUR',
        'azuk': 'GBP',
        'azjp': 'CNY',
        'azbr': 'BRL',
        'azau': 'USD',
        'azmx': 'USD'
    }
    dynamic_data = None
    dynamic_dict = {}
    asin = params.get('asin', None)
    platform = params.get('platform', None)
    table_name = db_method.ProductDynamic
    # 返回测试数据
    test = params.get('test', None)
    if test:
        table_name = test_common.TestProductDynamic
    try:
        dynamic_data = db_method.execute_sql(db_method.dynamic_select_sql, table_name, params)
        # 当天没数据则重新抓取
        if not dynamic_data:
            resp = common.scrapy_data(asin, platform, product_dynamic.get_dynamic_info)
            if resp:
                dynamic_data = db_method.execute_sql(db_method.dynamic_select_sql, table_name, params)
        dynamic_dict = [data.data_to_dict() for data in dynamic_data]
        # 添加货币单位
        update_price_unit(price_unit, dynamic_dict)
    except except_method.NotFoundError as e:
        dynamic_dict['NotFoundError'] = str(e)
    except Exception as e:
        dynamic_dict['Error'] = str(e)
        return dynamic_dict

    return dynamic_dict

def update_price_unit(price_unit, dynamic_dict):
    for dynamic in dynamic_dict:
        platform = dynamic.get('platform', None)
        unit = price_unit.get(platform, None)
        if unit:
            dynamic.update({'price_unit': unit})

# 通过id返回商品评论信息
def get_product_reviews_data(params):
    reviews_data = None
    reviews_dict = {}
    table_name = db_method.ProductReviews
    try:
        reviews_data = db_method.execute_sql(db_method.reviews_select_sql, table_name, params)
    except Exception as e:
        reviews_dict['Error'] = str(e)
        return reviews_dict
    if reviews_data:
        reviews_dict = [data.data_to_dict() for data in reviews_data]

    return reviews_dict

# 通过情感区间返回句子
def get_sentence_by_polarity(params):
    sentence_data = None
    sentence_dict = {}
    table_name = db_method.EmotionalSentence
    try:
        sentence_data = db_method.execute_sql(db_method.sql_sentence_polarity, table_name, params)
    except Exception as e:
        sentence_dict['Error'] = str(e)
        return sentence_dict
    if sentence_data:
        sentence_dict = [data.data_to_dict() for data in sentence_data]

    return sentence_dict

# 通过关键字返回句子
def get_sentence_by_keyword(params):
    sentence_data = None
    sentence_dict = {}
    table_name = db_method.EmotionalSentence
    try:
        sentence_data = db_method.execute_sql(db_method.sql_sentence_keyword, table_name, params)
    except Exception as e:
        sentence_dict['Error'] = str(e)
        return sentence_dict
    if sentence_data:
        sentence_dict = [data.data_to_dict() for data in sentence_data]

    return sentence_dict

# 获取评论表信息
def get_review(params):
    review_data = None
    review_dict = {}
    table_name = db_method.ProductReviews
    try:
        review_data = db_method.execute_sql(db_method.get_review_by_id, table_name, params)
    except Exception as e:
        review_dict['Error'] = str(e)
        return review_dict
    if review_data:
        review_dict = [data.data_to_dict() for data in review_data]

    return review_dict

# 获取关键字表信息
def get_keywords(params):
    keyword_data = None
    keyword_dict = {}
    table_name = db_method.Keywords
    try:
        keyword_data = db_method.execute_sql(db_method.get_keyword_by_asin, table_name, params)
    except Exception as e:
        keyword_dict['Error'] = str(e)
        return keyword_dict
    if keyword_data:
        keyword_dict = [data.data_to_dict() for data in keyword_data]

    return keyword_dict





