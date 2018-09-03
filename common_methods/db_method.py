# coding:utf-8

import pymysql
import datetime
from config import db

from sqlalchemy import Column, String, Integer, Float, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DBConnection = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=%s' % (db.User, db.Passwd, db.Host, db.Port, db.DB, db.CharSet)
engine = create_engine(DBConnection)
DBSession = sessionmaker(bind=engine)

Base = declarative_base()
class Product(Base):

    __tablename__ = 'product'

    id = Column(Integer(), primary_key=True)
    asin = Column(String(45))
    prod_title = Column(String(500))
    prod_image = Column(String(500))
    is_complete = Column(Integer())
    platform = Column(String(45))
    time = Column(DateTime)

    def __init__(self, params_dict):
        self.asin = params_dict.get('asin')
        self.prod_title = params_dict.get('prod_title')
        self.prod_image = params_dict.get('prod_image')
        self.is_complete = params_dict.get('is_complete')
        self.paltform = params_dict.get('platform', None)
        self.time = params_dict.get('time')


class ProductDynamic(Base):

    __tablename__ = 'product_dynamic'

    id = Column(Integer(), primary_key=True)
    asin = Column(String(255))
    price = Column(Float)
    star = Column(Float)
    comments = Column(Integer())
    rank_one = Column(Integer())
    category_one = Column(String(300))
    rank_two = Column(Integer())
    category_two = Column(String(300))
    rank_three = Column(Integer())
    category_three = Column(String(300))
    rank_four = Column(Integer())
    category_four = Column(String(300))
    rank_five = Column(Integer())
    category_five = Column(String(300))
    time = Column(DateTime)

    def __init__(self, params_dict):
        self.asin = params_dict.get('asin')
        self.price = params_dict.get('price')
        self.star = params_dict.get('star')
        self.comments = params_dict.get('comments')
        self.rank_one = params_dict.get('rank_one', None)
        self.category_one = params_dict.get('category_one', None)
        self.rank_two = params_dict.get('rank_two', None)
        self.category_two = params_dict.get('category_two', None)
        self.rank_three = params_dict.get('rank_three', None)
        self.category_three = params_dict.get('category_three', None)
        self.rank_four = params_dict.get('rank_four', None)
        self.category_four = params_dict.get('category_four', None)
        self.rank_five = params_dict.get('rank_five', None)
        self.category_five = params_dict.get('category_five', None)
        self.time = params_dict.get('time')


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


