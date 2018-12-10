# coding= utf-8
import re
import time
from bs4 import BeautifulSoup
from common_methods import db_method

def get_dynamic_info(asin, platform, browser):
    """
    抓取商品动态信息
    :param asin: 商品编号
    :param driver: 调用驱动抓取信息
    """
    soup = BeautifulSoup(browser.page_source, 'lxml')
    if platform == 'wicm':
        price = get_price_wish(soup)
        browser.find_element_by_xpath('//div[@class="PurchaseContainer__RatingWrapper-ebrehg fkCrvt"]').click()
        time.sleep(10)
        soup = BeautifulSoup(browser.page_source, 'lxml')
        star = get_star_wish(soup)
        review_counts = get_review_counts(soup)
        ranks, cates = [], []
    else:
        price = get_price(soup)
        star = get_star(soup)
        review_counts = get_review_counts(soup)
        ranks, cates = get_rank_and_cates(soup)

    params_dict = {
        "asin": asin.strip(),
        "platform": platform.strip(),
        "price": float(price),
        "star": float(star),
        "comments": review_counts,
        "ranks": ranks,
        "cats": cates
    }
    print('dynamic_info:%s' % params_dict)
    save_to_mysql(params_dict)
    return params_dict

# 商品动态信息保存到数据库
def save_to_mysql(params_dict):
    ranks_key = ['rank_one', 'rank_two', 'rank_three', 'rank_four', 'rank_five']
    cates_key = ['category_one', 'category_two', 'category_three', 'category_four', 'category_five']
    ranks_value = params_dict.get('ranks')
    cates_value = params_dict.get('cats')
    params_dict.pop('ranks')
    params_dict.pop('cats')
    if ranks_value and cates_value:
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
def get_price(soup):
    try:
        price = soup.find(attrs={'id': 'priceblock_ourprice'})
        # 图书价格
        if not price:
            price = soup.find(attrs={'id': 'a-autoid-0-announce'}) \
                        .findall('span')[2]
    except:
        # (针对某些打折的商品或)
        try:
            price = soup.find(attrs={'id': 'priceblock_dealprice'})
        except Exception as e:
            price = ''
            print('price_error:%s' % e)
    # 不同站点价格和单位的匹配
    if price:
        regex = '^(\D*)(\d+.*)$'
        prices = re.match(regex, price.text).groups()
        price_unit = prices[0].strip()
        print('price_unit: %s' % price_unit)
        price = prices[1]
        if price.find('-') != -1:
            price = price.split('-')[0].strip()
        if price.find(',') != -1:
            price = price.replace(',', '')
    else:
        price = 0.0
    return price

# wish商品价格
def get_price_wish(soup):
    price = soup.find(attrs={'class': 'PurchaseContainer__ActualPrice-liXyad cRbBob'}).text
    if price:
        regex = '(\d+)'
        price = re.search(regex, price).groups()[0]
        if price.find(',') != -1:
            price = price.replace(',', '')
    else:
        price = 0.0
    return price


# 返回商品星级
def get_star(soup):
    try:
        star = soup.find(attrs={'id': 'acrPopover'}).get('title')
    except Exception as e:
        star = ''
        print('star_error:%s' % e)
    if star:
        regex = '(\d+.\d+)'
        star = re.search(regex, star).groups()[0]
    else:
        star = 0.0
    return star

# wish星级
def get_star_wish(soup):
    star = soup.find(attrs={'class': 'ProductReviewContainer__AverageRationgScoreSection-enkDzN hiwWxQ'}).text
    if star:
        regex = '(\d+.\d+)'
        star = re.search(regex, star).groups()[0]
    else:
        star = 0.0
    return star


# 返回商品评论数
def get_review_counts(soup):
    try:
        review_counts = soup.find(attrs={'id': 'acrCustomerReviewText'})
        # wish 评论数
        if not review_counts:
            review_counts = soup.find(attrs={'class': 'ProductReviewContainer__TotalRating-jITvxa fFhsZP'})
    except Exception as e:
        review_counts = ''
        print('comments_error:%s' % e)
    if review_counts:
        regex = '(\d+,?\d*)'
        review_counts = re.search(regex, review_counts.text).groups()[0]
        if review_counts.find(',') != -1:
            review_counts = review_counts.replace(',', '')
    else:
        review_counts = 0
    return review_counts


# 返回商品类别和排名
def get_rank_and_cates(soup):
    listinfo = ''
    listinfo_sub = ''
    try:
        # listinfo1 = driver.find_element_by_id('detailBullets_feature_div').text
        listinfo = soup.find(attrs={'id': 'SalesRank'}).text
        listinfo_sub = soup.find(attrs={'class': 'zg_hrsr'})
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

    # 不同站点类别排名的匹配
    ranks, cates = [], []
    rank_regex = re.compile('(\d+)')
    try:
        if listinfo and (listinfo.find('(') != -1) \
                    and (listinfo.find(':') != -1):
            listinfo = listinfo.split('(')[0]\
                               .split(':')[1]\
                               .replace('\xa0', ' ')

            rank = rank_regex.findall(listinfo)
            cate = re.findall('in (.*)', listinfo) or \
                   re.findall('en (.*)', listinfo) or \
                   re.findall('em (.*)', listinfo) or \
                   re.findall('dans (.*)', listinfo) or \
                   re.findall('(.*)\u91cc', listinfo) or \
                   re.findall('(.*)\u002d', listinfo)
            if rank and cate:
                ranks.append(rank[0].replace(',', '').replace('.', ''))
                cates.append(cate[0].strip())
    except Exception as e:
        print('list:%s' % e)

    try:
        if listinfo_sub:
            for list in listinfo_sub.find_all('li'):
                rank = list.find('span', attrs={'class': 'zg_hrsr_rank'}).text
                cate = list.find('span', attrs={'class': 'zg_hrsr_ladder'}).text
                rank = rank.replace(',', '').replace('.', '')

                rank = rank_regex.findall(rank)
                cate = cate.replace('\xa0', '').replace('-', '')
                cate = re.findall('^(?:in)?(?:en)?(?:em)?(?:dans)?(.*)', cate)
                if rank and cate:
                    ranks.append(rank[0])
                    cates.append(cate[0].strip())
    except Exception as e:
        print('list_sub:%s' % e)

    return ranks, cates



