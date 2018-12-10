import time
import random
import pymysql
from config import db
from common_methods import db_method
from sqlalchemy import Column, String, Integer, Float, DateTime, Date, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DBConnection = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=%s&autocommit=true' % (db.User, db.Passwd, db.Host, db.Port, db.DB, db.CharSet)
engine = create_engine(DBConnection)
DBSession = sessionmaker(bind=engine)

Base = declarative_base()
class TestProduct(Base):
    '''
    商品表
    '''
    __tablename__ = 'test_product'

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


class TestProductDynamic(Base):
    '''
    商品动态数据表
    '''
    __tablename__ = 'test_product_dynamic'

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

# 查询
def select_sql(sql):
    db = pymysql.connect(host='192.168.55.6', user='root', password='123456', port=3306, db='smart_dolphin',
                         charset="utf8")
    cursor = db.cursor()
    cursor.execute(sql)
    resp = cursor.fetchall()
    db.commit()
    return resp

# 获取测试商品asin
def get_test_asin_and_platform():
    session = db_method.DBSession()
    asin_platforms = session.query(TestProduct.asin, TestProduct.platform).all()
    session.close()
    return asin_platforms

# 获取测试动态数据
def get_test_dynamic(asin, platform):
    sql = 'SELECT  * FROM test_product_dynamic where asin="%s" and platform="%s" order by date(time) desc limit 1' % \
          (asin, platform)
    dynamic = select_sql(sql)
    return dynamic

# 添加测试动态数据
def add_test_dynamic(dynamic_dict):
    asin = dynamic_dict.get('asin')
    price = dynamic_dict.get('price')
    star = dynamic_dict.get('star')
    comments = dynamic_dict.get('comments')
    rank_1 = dynamic_dict.get('rank_1')
    rank_2 = dynamic_dict.get('rank_2')
    rank_3 = dynamic_dict.get('rank_3')
    rank_4 = dynamic_dict.get('rank_4')
    rank_5 = dynamic_dict.get('rank_5')
    cate_1 = dynamic_dict.get('cate_1')
    cate_2 = dynamic_dict.get('cate_2')
    cate_3 = dynamic_dict.get('cate_3')
    cate_4 = dynamic_dict.get('cate_4')
    cate_5 = dynamic_dict.get('cate_5')
    platform = dynamic_dict.get('platform')
    time = dynamic_dict.get('time')

    db = pymysql.connect(host='192.168.55.6', user='root', password='123456', port=3306, db='smart_dolphin',
                         charset="utf8")
    cursor = db.cursor()
    sql = 'INSERT INTO test_product_dynamic (asin, price, star, comments, rank_one, category_one, rank_two, ' \
          'category_two, rank_three, category_three, rank_four, category_four, rank_five, category_five, ' \
          'platform, time) ' \
          'VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % \
          (asin, price, star, comments, rank_1, cate_1, rank_2, cate_2, rank_3, cate_3, rank_4, cate_4, rank_5, cate_5,
           platform, time)
    cursor.execute(sql)
    db.commit()


# 更新排名
def update_rank(rank):
    rank = int(rank)
    if rank >11:
        rank_s = rank - 10
        rank_e = rank + 10
        rank = random.randint(rank_s, rank_e)
    return rank

# 更新星级
def update_star(star):
    star = float(star)
    if star > 0 and star <5:
        star += random.choice([0, 0.1])
    return star

# 更新测试动态数据
def get_test_dynamic_dict(dynamic_data):
    asin = dynamic_data[1]
    cate_1 = dynamic_data[6]
    cate_2 = dynamic_data[8]
    cate_3 = dynamic_data[10]
    cate_4 = dynamic_data[12]
    cate_5 = dynamic_data[14]
    platform = dynamic_data[14]
    date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    price = dynamic_data[2]
    star = dynamic_data[3]
    comments = dynamic_data[4]
    rank_1 = dynamic_data[5]
    rank_2 = dynamic_data[7]
    rank_3 = dynamic_data[9]
    rank_4 = dynamic_data[11]
    rank_5 = dynamic_data[13]

    dynamic_dict = {
        'asin': asin,
        'price': price,
        'star': update_star(star),
        'comments': int(comments) + random.randint(1, 3),
        'rank_1': update_rank(rank_1),
        'rank_2': update_rank(rank_2),
        'rank_3': update_rank(rank_3),
        'rank_4': update_rank(rank_4),
        'rank_5': update_rank(rank_5),
        'cate_1': cate_1,
        'cate_2': cate_2,
        'cate_3': cate_3,
        'cate_4': cate_4,
        'cate_5': cate_5,
        'platform': platform,
        'time': date_time
    }
    return dynamic_dict


if __name__ == '__main__':
    asin_plats = get_test_asin_and_platform()
    for asin_plat in asin_plats:
        asin = asin_plat[0]
        platform = asin_plat[1]
        dynamic = get_test_dynamic(asin, platform)
        dynamic_dict = get_test_dynamic_dict(dynamic[0])
        add_test_dynamic(dynamic_dict)
