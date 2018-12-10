# coding= utf-8
from bs4 import BeautifulSoup
from common_methods import db_method


def get_product_info(asin, platform, browser):
    """
    通过asin抓取商品信息
    :param asin: 商品编号
    :param driver: 调用驱动抓取信息
    :return: 返回抓取的商品信息
    """
    soup = BeautifulSoup(browser.page_source, 'lxml')
    product_name = get_prod_title(soup)
    img_link = get_image_link(soup)
    params_dict = {
        'asin': asin.strip(),
        'platform': platform.strip(),
        'prod_title': product_name.strip(),
        'prod_image': img_link
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


def get_prod_title(soup):
    prod_title = soup.find(attrs={'id': 'productTitle'})
    # wish 产品名称
    if not prod_title:
        prod_title = soup.find(attrs={'class': 'PurchaseContainer__Name-ghgluL crzchL'})
    prod_title = prod_title.text
    return prod_title


def get_image_link(soup):
    img = soup.find('img', attrs={'id': 'landingImage'})
    if not img:
        # 书籍图片
        img = soup.find('img', attrs={'id': 'imgBlkFront'})
    # wish 商品图片
    if not img:
        img = soup.find('img', attrs={'class': 'ProductImageContainer__StripImage-jMdYib fjlNJj'})
    img_link = img.get('src')
    return img_link


