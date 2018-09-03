# coding:utf-8
from selenium import webdriver

UrlPath = 'https://www.amazon.com/dp/%s?th=1&psc=1'

def scrapy_data(asin, scrapy_func):
    driver = webdriver.Chrome()
    urlpath = UrlPath % asin
    driver.get(urlpath)
    scrapy_func(asin, driver)
    driver.close()
