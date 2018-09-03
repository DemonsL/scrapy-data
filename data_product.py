# coding:utf-8

from config import db
from common_methods import db_method
from common_methods import common
from api_scrapy import product_info
from api_scrapy import product_dynamic


def get_product_data(params):
    """
    通过asin返回商品信息
    :param params: 请求参数（asin, is_complete, platform)
    :return: 返回asin相关的商品信息
    """
    asin = params.get('asin')
    is_complete = params.get('is_complete')
    platform = params.get('platform')

    table_name = db.Tables.get('product')
    if asin:
        params_name = ['asin']
        params_value = [asin]
        select_sql = db_method.execute_sql(table_name, params_name, params_value)
    else:
        return {'Error': 'Parameters asin is required.'}

    if is_complete and platform:
        params_name = ['asin', 'is_complete', 'platform']
        params_value = [asin, is_complete, platform]
        select_sql = db_method.execute_sql(table_name, params_name, params_value)
    elif is_complete:
        params_name = ['asin', 'is_complete']
        params_value = [asin, is_complete]
        select_sql = db_method.execute_sql(table_name, params_name, params_value)
    elif platform:
        params_name = ['asin', 'platform']
        params_value = [asin, platform]
        select_sql = db_method.execute_sql(table_name, params_name, params_value)

    product_data = db_method.get_db_data(select_sql)
    if product_data:
        product_dict = db_method.data_to_dict(product_data, table_name)
    else:
        product_dict = common.scrapy_data(asin, product_info.get_product_info)

        dynamic_param = {'asin': asin}
        dynamic_today = get_product_dynamic_data(dynamic_param)
        if not dynamic_today:
            common.scrapy_data(asin, product_dynamic.get_dynamic_info)
    return product_dict


def get_product_dynamic_data(params):
    """
    通过asin返回商品动态信息
    :param params: 请求参数（asin）
    :return: 返回商品动态信息
    """
    asin = params.get('asin')

    table_name = db.Tables.get('product_dynamic')
    if asin:
        params_name = ['asin']
        params_value = [asin]

        other_case = ' and date(time)=curdate()'
        select_sql = db_method.execute_sql(table_name, params_name, params_value, other_case)
    else:
        return {'Error': 'Parameters asin is required.'}

    dynamic_data = db_method.get_db_data(select_sql)
    dynamic_dict = db_method.data_to_dict(dynamic_data, table_name)
    return dynamic_dict


def get_product_reviews_data(params):
    """
    通过id返回商品评论信息
    :param params: 请求参数（id, asin, review_star）
    :return: 返回商品评论信息
    """
    id = params.get('id')
    asin = params.get('asin')
    review_star = params.get('review_star')

    sign = '>'
    table_name = db.Tables.get('product_reviews')
    if id:
        params_name = ['id']
        params_value = [id]
        select_sql = db_method.execute_sql(table_name, params_name, params_value, sign=sign)
    else:
        return {'Error': 'Parameters id is required.'}

    if asin and review_star:
        params_name = ['id', 'asin', 'review_star']
        params_value = [id, asin, review_star]
        select_sql = db_method.execute_sql(table_name, params_name, params_value, sign=sign)
    elif asin:
        params_name = ['id', 'asin']
        params_value = [id, asin]
        select_sql = db_method.execute_sql(table_name, params_name, params_value, sign=sign)
    elif review_star:
        params_name = ['id', 'review_star']
        params_value = [id, review_star]
        select_sql = db_method.execute_sql(table_name, params_name, params_value, sign=sign)

    reviews_data = db_method.get_db_data(select_sql)
    reviews_dict = db_method.data_to_dict(reviews_data, table_name)
    return reviews_dict





