# coding:utf-8

import time
from config import db
from common_methods import except_method
from sqlalchemy import Column, String, Integer, Float, DateTime, Date, create_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DBConnection = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=%s&autocommit=true' % (db.User, db.Passwd, db.Host, db.Port, db.DB, db.CharSet)
engine = create_engine(DBConnection)
DBSession = sessionmaker(bind=engine)

Base = declarative_base()
class Product(Base):
    '''
    商品表
    '''
    __tablename__ = 'product'

    id = Column(Integer(), primary_key=True)
    asin = Column(String(45))
    prod_title = Column(String(500))
    prod_image = Column(String(500))
    is_complete = Column(Integer())
    platform = Column(String(45))
    time = Column(DateTime)
    status = Column(Integer())

    def __init__(self, params_dict):
        self.asin = params_dict.get('asin')
        self.prod_title = params_dict.get('prod_title')
        self.prod_image = params_dict.get('prod_image')
        self.is_complete = params_dict.get('is_complete', 1)
        self.platform = params_dict.get('platform', None)
        self.time = params_dict.get('time',
                                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        self.status = params_dict.get('status', 0)

    def data_to_dict(self):
        data_dict = {
            'asin': self.asin,
            'prod_title': self.prod_title,
            'prod_image': self.prod_image,
            'is_complete': self.is_complete,
            'platform': self.platform,
            'time': str(self.time)
        }
        return data_dict


class ProductDynamic(Base):
    '''
    商品动态数据表
    '''
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
    platform = Column(String(45))
    time = Column(DateTime)

    def __init__(self, params_dict):
        self.asin = params_dict.get('asin')
        self.price = params_dict.get('price')
        self.star = params_dict.get('star')
        self.comments = params_dict.get('comments')
        self.rank_one = params_dict.get('rank_one', 0)
        self.category_one = params_dict.get('category_one', None)
        self.rank_two = params_dict.get('rank_two', 0)
        self.category_two = params_dict.get('category_two', None)
        self.rank_three = params_dict.get('rank_three', 0)
        self.category_three = params_dict.get('category_three', None)
        self.rank_four = params_dict.get('rank_four', 0)
        self.category_four = params_dict.get('category_four', None)
        self.rank_five = params_dict.get('rank_five', 0)
        self.category_five = params_dict.get('category_five', None)
        self.platform = params_dict.get('platform', None)
        self.time = params_dict.get('time',
                                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def data_to_dict(self):
        data_dict = {
            'asin': self.asin,
            'price': self.price,
            'star': self.star,
            'comments': self.comments,
            'rank_one': self.rank_one,
            'category_one': self.category_one,
            'rank_two': self.rank_two,
            'category_two': self.category_two,
            'rank_three': self.rank_three,
            'category_three': self.category_three,
            'rank_four': self.rank_four,
            'category_four': self.category_four,
            'rank_five': self.rank_five,
            'category_five': self.category_five,
            'platform': self.platform,
            'time': str(self.time)
        }
        return data_dict

class ProductReviews(Base):
    '''
    商品评论表
    '''
    __tablename__ = 'product_reviews'

    id = Column(Integer(), primary_key=True)
    asin = Column(String(45))
    review_title = Column(String(500))
    review_content = Column(String())
    attribute_one = Column(String(100))
    attribute_two = Column(String(100))
    votes = Column(Integer())
    review_time = Column(String(20))
    convert_time = Column(Date)
    review_author = Column(String(100))
    review_star = Column(Float())
    time = Column(DateTime)

    def data_to_dict(self):
        data_dict = {
            'id': self.id,
            'asin': self.asin,
            'review_title': self.review_title,
            'review_content': self.review_content,
            'attribute_one': self.attribute_one,
            'attribute_two': self.attribute_two,
            'votes': self.votes,
            'review_time': self.review_time,
            'convert_time': str(self.convert_time),
            'review_author': self.review_author,
            'review_star': self.review_star,
            'time': str(self.time)
        }
        return data_dict

class EmotionalSentence(Base):
    '''
    句子的情感分析表
    '''
    __tablename__ = 'emotional_sentence'

    id = Column(Integer(), primary_key=True)
    reviews_id = Column(Integer())
    asin = Column(String(45))
    prod_star = Column(Float())
    sentence = Column(String())
    polarity = Column(Float())
    time = Column(DateTime)

    def data_to_dict(self):
        data_dict = {
            'id': self.id,
            'reviews_id': self.reviews_id,
            'asin': self.asin,
            'prod_star': self.prod_star,
            'sentence': self.sentence,
            'polarity': self.polarity,
            'time': str(self.time)
        }
        return data_dict

class Keywords(Base):
    '''
    关键字表
    '''
    __tablename__ = 'keywords'

    id = Column(Integer(), primary_key=True)
    asin = Column(String(45))
    keyword = Column(String())
    keyword_tag = Column(String())
    frequency = Column(Integer())
    time = Column(DateTime)

    def data_to_dict(self):
        data_dict = {
            'id': self.id,
            'asin': self.asin,
            'keyword': self.keyword,
            'keyword_tag': self.keyword_tag,
            'frequency': self.frequency,
            'time': str(self.time)
        }
        return data_dict


# 执行数据库操作
def execute_sql(sql_case, table_name, params):
    session = DBSession()
    select_sql = sql_case(params)
    try:
        resp_data = session.query(table_name).filter(text(select_sql)).all()
    except:
        resp_data = session.query(table_name).filter(text(select_sql)).all()
    session.close()
    return resp_data

def add_product(asin, platform):
    product_dict = {
        'asin': asin,
        'prod_title': '',
        'prod_image': '',
        'is_complete': 0,
        'platform': platform,
        'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    }
    return product_dict

# 添加多个商品号到商品信息表
def add_product_data(params):
    session = DBSession()
    asin_platforms = session.query(Product.asin, Product.platform).all()
    product_list = []
    asins = params.get('asins', None)
    platform = params.get('platform', None)
    if asins and platform:
        if asins.find(',') != -1:
            for asin in asins.split(','):
                # 去重
                asin_p = (asin, platform)
                if asin_p not in asin_platforms:
                    product_dict = add_product(asin, platform)
                    product = Product(product_dict)
                    product_list.append(product)
        else:
            asin_p = (asins, platform)
            if asin_p not in asin_platforms:
                product_dict = add_product(asins, platform)
                product = Product(product_dict)
                product_list.append(product)
    else:
        msg = except_method.param_error('asins and platform')
        raise except_method.BadRequestError(msg)
    session.add_all(product_list)
    session.commit()
    return True


# 商品查询语句
def product_select_sql(params):
    asin = params.get('asin', None)
    is_complete = params.get('is_complete', None)
    platform = params.get('platform', None)

    if asin and platform:
        select_sql = 'asin="%s" and platform="%s"' % (asin, platform)
    else:
        msg = except_method.param_error('asin and platform')
        raise except_method.BadRequestError(msg)
    if is_complete:
        select_sql = 'asin="%s" and is_complete="%s" and platform="%s"' % (asin, is_complete, platform)

    # resp_data = session.query(table_name).filter(text(select_sql)).all()
    return select_sql

# 商品动态数据查询
def dynamic_select_sql(params):
    asin = params.get('asin', None)
    platform = params.get('platform', None)
    start_date = params.get('start_date', None)
    end_date = params.get('end_date', None)

    if asin and platform:
        select_sql = 'asin="%s" and platform="%s" and date(time)=curdate()' % (asin, platform)
        if start_date:
            select_sql = 'asin="%s" and platform="%s" and date(time)>="%s"' % (asin, platform, start_date)
        if start_date and end_date:
            select_sql = 'asin="%s" and platform="%s" and date(time) between "%s" and "%s"' % (asin, platform,
                                                                                               start_date, end_date)
    else:
        msg = except_method.param_error('asin and platform')
        raise except_method.BadRequestError(msg)

    # resp_data = session.query(table_name).filter(text(select_sql)).all()
    return select_sql

# 商品评论查询
def reviews_select_sql(params):
    id = params.get('id', None)
    asin = params.get('asin', None)
    review_star = params.get('review_star', None)

    if id:
        select_sql = 'id>%s' % id
    else:
        msg = except_method.param_error('id')
        raise except_method.BadRequestError(msg)

    if asin and review_star:
        select_sql = 'id>%s and asin="%s" and review_star="%s"' % (id, asin, review_star)
    elif asin:
        select_sql = 'id>%s and asin="%s"' % (id, asin)
    elif review_star:
        select_sql = 'id>%s and review_star="%s"' % (id, review_star)

    # resp_data = session.query(table_name).filter(text(select_sql)).all()
    return select_sql

# 通过情感区间查句子
def sql_sentence_polarity(params):
    asin = params.get('asin', None)
    polarity = params.get('polarity', None)
    if not asin:
        msg = except_method.param_error('asin')
        raise except_method.BadRequestError(msg)
    if not polarity:
        msg = except_method.param_error('polarity')
        raise except_method.BadRequestError(msg)
    polarity = polarity.split(',')
    select_sql = 'asin="%s" and polarity>%s and polarity<%s' %(asin, polarity[0], polarity[1])
    # resp_data = session.query(table_name).filter(text(select_sql)).all()
    return select_sql

# 通过关键字查句子
def sql_sentence_keyword(params):
    asin = params.get('asin', None)
    keyword = params.get('keyword', None)
    if not asin:
        msg = except_method.param_error('asin')
        raise except_method.BadRequestError(msg)
    if not keyword:
        msg = except_method.param_error('keyword')
        raise except_method.BadRequestError(msg)
    select_sql = 'asin="%s" and sentence like "%s%s%s"' % (asin, '%', keyword, '%')
    # resp_data = session.query(table_name).filter(text(select_sql)).all()
    return select_sql

# 评论内容查询
def get_review_by_id(params):
    id = params.get('id', None)
    if not id:
        msg = except_method.param_error('id')
        raise except_method.BadRequestError(msg)
    select_sql = 'id="%s"' % id
    # resp_data = session.query(table_name).filter(table_name.id == id).all()
    return select_sql

# 关键字表查询
def get_keyword_by_asin(params):
    asin = params.get('asin', None)
    if not asin:
        msg = except_method.param_error('asin')
        raise except_method.BadRequestError(msg)
    select_sql = 'asin="%s"' % asin
    # resp_data = session.query(table_name).filter(table_name.asin == asin).all()
    return select_sql

