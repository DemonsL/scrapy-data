# coding:utf-8

from config import db
from common_methods import db_method

class Product:

    def get_product_data(params):
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
        product_data = db_method.data_to_dict(product_data, table_name)
        return product_data

    def get_product_dynamic_data(params):
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
        dynamic_data = db_method.data_to_dict(dynamic_data, table_name)
        return dynamic_data

    def get_product_reviews_data(params):
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
        reviews_data = db_method.data_to_dict(reviews_data, table_name)
        return reviews_data