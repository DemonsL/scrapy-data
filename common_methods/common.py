# coding:utf-8
# import requests
import time
import random
from common_methods import except_method
from common_methods import user_agent
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

"""
    Amazon_Platform
    {
        'azcm': '美国',
        'azca': '加拿大',
        'azde': '德国',
        'azes': '西班牙',
        'azfr': '法国',
        'azit': '意大利',
        'azin': '印度',
        'azcn': '中国',
        'aznl': '荷兰',
        'azuk': '英国',
        'azjp': '日本',
        'azbr': '巴西',
        'azau': '澳大利亚',
        'azmx': '墨西哥'
    }
"""

urls = {
    # amazon scrapy
    'azcm': 'https://www.amazon.com/dp/%s?th=1&psc=1',
    'azca': 'https://www.amazon.ca/dp/%s?th=1&psc=1',
    'azde': 'https://www.amazon.de/dp/%s?th=1&psc=1',
    'azes': 'https://www.amazon.es/dp/%s?th=1&psc=1',
    'azfr': 'https://www.amazon.fr/dp/%s?th=1&psc=1',
    'azit': 'https://www.amazon.it/dp/%s?th=1&psc=1',
    'azin': 'https://www.amazon.in/dp/%s?th=1&psc=1',
    'azcn': 'https://www.amazon.cn/dp/%s?th=1&psc=1',
    'aznl': 'https://www.amazon.nl/dp/%s?th=1&psc=1',
    'azuk': 'https://www.amazon.co.uk/dp/%s?th=1&psc=1',
    'azjp': 'https://www.amazon.co.jp/dp/%s?th=1&psc=1',
    'azbr': 'https://www.amazon.com.br/dp/%s?th=1&psc=1',
    'azau': 'https://www.amazon.com.au/dp/%s?th=1&psc=1',
    'azmx': 'https://www.amazon.com.mx/dp/%s?th=1&psc=1',
    # wish scrapy
    'wicm': 'https://www.wish.com/product/%s'
}

def scrapy_data(asin, platform, scrapy_func):
    if platform == 'wicm':
        site = 'https://www.wish.com'
        user = '245576908@qq.com'
        pwd = 'test123'
        browser = site_login(site, user, pwd)
        # 登录之后等待10秒
        time.sleep(10)
    else:
        # 浏览器添加user_agent
        ua = random.choice(user_agent.UserAgentList)
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = ua
        browser = webdriver.PhantomJS(desired_capabilities=dcap)
    # 站点异常处理
    url_path = urls.get(platform, None)
    if not url_path:
        raise except_method.NotFoundError('Platform Not Found')

    browser.get(url_path % asin)
    # agent = browser.execute_script("return navigator.userAgent")
    # print('ua:%s'%agent)
    # 404异常处理
    page_length = browser.page_source.__len__()
    if page_length < 8000:
        raise except_method.NotFoundError('Page Not Found')
    # 抓取数据
    # soup = BeautifulSoup(browser.page_source, 'lxml')
    res_data = scrapy_func(asin, platform, browser)
    return res_data


def site_login(site, user, pwd):
    browser = webdriver.Chrome()
    # 用户登录
    browser.get(site)
    browser.find_element_by_xpath('//*[@id="signup-form"]/div[4]').click()
    browser.find_element_by_xpath('//*[@id="test-le"]').send_keys(user)
    browser.find_element_by_xpath('//*[@id="test-lp"]').send_keys(pwd)
    browser.find_element_by_xpath('//*[@id="test-elf"]/button').submit()
    cookies = browser.get_cookies()
    # 添加cookies
    for item in cookies:
        browser.add_cookie({
            'domain': 'www.wish.com',
            'name': item['name'],
            'value': item['value'],
            'path': '/',
            'expiry': None
        })
    return browser





