# coding:utf-8

import pymysql
import datetime
from config import db

# 连接数据库
def database_connection():
    conn = pymysql.connect(host=db.Host, port=db.Port, user=db.User, passwd=db.Passwd, db=db.DB, charset=db.CharSet)
    cursor = conn.cursor()
    return cursor, conn

# 执行数据库操作并返回数据
def get_db_data(execute_sql):
    cursor, conn = database_connection()
    cursor.execute(execute_sql)
    db_data = cursor.fetchall()
    conn.close()
    return db_data

# 返回数据库操作语句
def execute_sql(table_name, params_name, params_value, other_case=None, sign='='):
    where_case = ''
    params_dict = {}
    if sign == '>':
        where_case = 'and ' + params_name[0] + sign + params_value[0]
        if len(params_name) > 1:
            params_dict = dict(zip(params_name[1:],params_value[1:]))
    else:
        params_dict = dict(zip(params_name, params_value))

    if params_dict:
        for key, value in params_dict.items():
            where_case += 'and ' + key + '="' + value + '"'
    where_case = ' WHERE ' + where_case[3:]

    select_sql = 'SELECT * FROM %s' % table_name
    if where_case:
        select_sql = select_sql + where_case
    if other_case:
        select_sql = select_sql + other_case
    return select_sql


# 数据库中的数据转成字典
def data_to_dict(data, table_name):
    data_dict = {}
    column = db.Columns.get(table_name)
    count = 0
    for value in data:
        val = []
        for v in value:
            if isinstance(v, datetime.datetime):
                v = str(v)
            if isinstance(v, datetime.date):
                v = str(v)
            val.append(v)
        value_dict = dict(zip(column, val))
        data_dict[count] = value_dict
        count += 1
    return data_dict


