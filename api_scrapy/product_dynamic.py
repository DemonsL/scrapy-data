# coding= utf-8

import time
from bs4 import BeautifulSoup
from common_methods import db_method

def get_dynamic_info(asin, driver):
    """
    抓取商品动态信息
    :param asin: 商品编号
    :param driver: 调用驱动抓取信息
    """
    pageSource = driver.page_source
    soup = BeautifulSoup(pageSource, 'lxml')
    print("=" * 30)
    asin = asin.replace(" ", "")
    asin = asin.replace("\n", "")
    asin = asin.replace("\t", "")
    dollar = get_price(driver)
    star = get_star(driver, soup)
    review_counts = get_review_counts(driver)
    runtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    ranks, cates = get_rank_and_cates(driver)
    params_dict = {
        'asin': asin,
        "price": dollar,
        "star": star,
        "comments": review_counts,
        "time": runtime,
        "ranks": ranks,
        "cats": cates
    }
    save_to_mysql(params_dict)

# 商品动态信息保存到数据库
def save_to_mysql(params_dict):
    ranks_key = ['rank_one', 'rank_two', 'rank_three', 'rank_four', 'rank_five']
    cates_key = ['category_one', 'category_two', 'category_three', 'category_four', 'category_five']
    ranks_value = params_dict.get('ranks')
    cates_value = params_dict.get('cats')
    params_dict.pop('ranks')
    params_dict.pop('cats')
    ranks = dict(zip(ranks_key, ranks_value))
    cates = dict(zip(cates_key, cates_value))
    params_dict.update(ranks)
    params_dict.update(cates)

    session = db_method.DBSession()
    product_dynamic = db_method.ProductDynamic(params_dict)
    session.add(product_dynamic)
    session.commit()
    session.close()

# 返回商品价格
def get_price(driver):
    try:
        dollar = driver.find_element_by_xpath('//*[@id="priceblock_ourprice"]')
        dollar = dollar.text.replace("$", "")
    except:
        # (针对某些打折的商品或)
        try:
            dollar = driver.find_element_by_id('priceblock_dealprice')
            dollar = dollar.text.replace("$", "")
        except:
            # 针对某些没有标价的商品
            dollar = '0'
    finally:
        print("Price: {0}".format(dollar))

    return dollar

# 返回商品星级
def get_star(driver, soup):
    try:
        star = soup.find('span', class_='a-icon-alt').text.replace(" out of 5 stars", "")
        print("Product star: {0}".format(star))
    except:
        star = ""
        print('Product star:  此商品尚未有星级信息')
    return star

# 返回商品评论数
def get_review_counts(driver):
    try:
        review_counts = driver.find_element_by_id('acrCustomerReviewLink').text.replace(" customer reviews", "")
        review_counts = review_counts.replace(",", "")
    except:
        review_counts = "0"

    return review_counts

# 返回商品描述
def get_product_desc(driver):
    try:
        ProductDsc = driver.find_element_by_xpath('//*[@id="productDescription_feature_div"]').text
        print(ProductDsc)
    except:
        ProductDsc = ""
    return ProductDsc

# 返回商品类别和排名
def get_rank_and_cates(driver):
    try:
        # listinfo1 = driver.find_element_by_id('detailBullets_feature_div').text
        listinfo2 = driver.find_element_by_id('SalesRank').text
    except:
        pass
        # try:
        #     tableinfo_1 = driver.find_element_by_xpath('//*[@id="productDetails_detailBullets_sections1"]/tbody').text
        #     tableinfo_2 = driver.find_element_by_xpath('//*[@id="productDetails_techSpec_section_1"]').text
        #     tableinfo_3 = driver.find_element_by_xpath('//*[@id="productDetails_techSpec_section_2"]').text
        # except:
        #     pass
        #     # 其他表现形式
        #     # otherclass = driver.find_element_by_xpath('//*[@id="detail-bullets"]/table/tbody').text
        #     # print(otherclass)
    ls1 = listinfo2.split('\n')
    ranks = []
    cates = []
    for ls in ls1:
        lls = ls.split('#')[1]
        ranks.append(lls.split(' in ')[0].replace(',', ''))
        cates.append(lls.split(' in ')[1].split('(See Top 100')[0])

    return ranks, cates



