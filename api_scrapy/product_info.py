# coding= utf-8

import time
from common_methods import db_method

            
def get_product_info(asin, driver):
    """
    通过asin抓取商品信息
    :param asin: 商品编号
    :param driver: 调用驱动抓取信息
    :return: 返回抓取的商品信息
    """
    runtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    product_name = driver.find_element_by_xpath('//*[@id="productTitle"]').text
    img = driver.find_element_by_id('landingImage')
    imglink = img.get_attribute('src') 
    print(imglink)  
    complete = '1'
    asin = asin.replace(" ","")
    asin = asin.replace("\n","")
    asin = asin.replace("\t","")
    params_dict = {
        'asin': asin,
        'prod_title': product_name,
        'prod_image': imglink,
        'is_complete': complete,
        'time': runtime
    }
    save_to_mysql(params_dict)
    return params_dict

# 保存商品信息到数据库
def save_to_mysql(params_dict):
    session = db_method.DBSession()
    product_info = db_method.Product(params_dict)
    session.add(product_info)
    session.commit()
    session.close()

