# coding= utf-8

import time
import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import pymysql


asin_list = ["B07F9J9SLJ","B07GRDFVY3","B01M5K7F36","B07F9M8CG3","B078SS4DS7","B078RRYSK5",
            "B075MJ4N14","B07D3SKNNG","B07BC6SHXF","B079V7YHQ8"]



def get_reviews(asin):
    driverPath = "D:\\test\\chromedriver"
    driver = webdriver.Chrome(executable_path=driverPath)
    url = "https://www.amazon.com/product-reviews/" + asin
    driver.get(url)
    #time.sleep(10)
    #获取网页源代码
    pageSource = driver.page_source  
    #利用bs4解析网页源代码
    soup = BeautifulSoup(pageSource,'lxml')   
    # 获取评论数counts
    # Rcounts = driver.find_element_by_xpath('//*[@id="cm_cr-product_info"]/div/div[1]/div[2]/div/div/div[2]/div/span').text
    counts = soup.find('span',class_='a-size-medium totalReviewCount').text
    #计算最大页码数maxIndex
    counts = int(counts.replace(",",""))
    if (counts %10) == 0:
        max_page = counts//10
    else:
        max_page = counts//10
        max_page = max_page + 1
    print('当前商品评论共[{0}]页，请稍等...'.format(max_page))

    #设置计数器页码计数器 i，评论计数器 m
    i = 1
    while True:
        #查找所有评论信息
        comments = soup.find_all('div',class_='a-section celwidget')       
        #遍历取出单条评论信息
        for comment in comments:
            #买家
            name = comment.find('a',class_ = 'a-size-base a-link-normal author').text
            print("买家名称：{0}".format(name))
            #星级
            star = comment.find('span',class_ = 'a-icon-alt').text
            print("评论星级：{0}".format(star))
            #评论标题
            title = comment.find('a',class_ = 'a-size-base a-link-normal review-title a-color-base a-text-bold').text
            print("评论主题: {0}".format(title))
            #评论时间
            time0 = comment.find('span',class_ = 'a-size-base a-color-secondary review-date').text
            print("评论时间：{0}".format(time0))
            #获取评论内容
            text = comment.find('span',class_ = 'a-size-base review-text').text
            print("评论内容：{0}".format(text))
            #色号、尺寸
            color = comment.find('a',class_ = 'a-size-mini a-link-normal a-color-secondary')
            #由于有的买家评论没有色号及尺码，加个判断
            if color:
                color = str(color)
                color_xpath = color.split(">")
                attribute1 = color_xpath[1].split('<')[0]
                attribute2 = color_xpath[3].split('<')[0]
                print(f"大小：{attribute1}\n色号:{attribute2}")
            else:
                attribute1 = ""
                attribute2 = ""
                print('当前买家没有提供色号及尺寸信息')
            #点赞数
            review_votes = comment.find('span',class_ = 'a-size-base a-color-tertiary cr-vote-text')
            if review_votes:
                review_votes = review_votes.text
                if review_votes == 'One person found this helpful':
                    review_votes = "1"
                else:
                    review_votes = review_votes.replace("people found this helpful","")
                
                print("点赞数: {0}".format(review_votes))
            else:
                review_votes = "0"
                print("当前评论没有被点赞")
            

            #写入数据库
            asin = asin.replace(" ","")
            asin = asin.replace("\n","")
            asin = asin.replace("\t","")
            time0 = time0.replace("on ","")
            #英文时间转为中文时间
            tranfo_time = datetime.datetime.strptime(time0,'%B %d, %Y')            
            star = star.replace(" out of 5 stars","")
            #当前时间
            runtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            db = pymysql.connect(host='localhost',user='root',password='qaz15690873009',port=3306,db='smart_dolphin',use_unicode=True,charset="utf8mb4")
            cursor= db.cursor()

            sql = 'INSERT INTO product_reviews(asin,review_title,votes,review_time,convert_time,review_author,review_star,time,review_content,attribute_one,attribute_two)\
                                                values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(sql,(asin,title,review_votes,time0,tranfo_time,name,star,runtime,text,attribute1,attribute2))
            db.commit()
            print('写入数据库完毕...')
            print('~'*30)
        #当达到最大页码，终止循环
        if i == max_page:
            break
        print("==================  第{0}页评论,正在获取下一页，请稍等...  ===================".format(i))

        if max_page == 2:
            #//*[@id="cm_cr-pagination_bar"]/ul/li[4]/a
            #//*[@id="cm_cr-pagination_bar"]/ul/li[4]/a
            driver.find_element_by_xpath('//*[@id="cm_cr-pagination_bar"]/ul/li[4]/a').click()
            time.sleep(6)
            i = i + 1
            pageSource = driver.page_source
            #利用bs4解析网页源代码
            soup = BeautifulSoup(pageSource,'lxml')
        if max_page == 3:
            driver.find_element_by_xpath('//*[@id="cm_cr-pagination_bar"]/ul/li[5]/a').click()
            time.sleep(6)
            i = i + 1
            pageSource = driver.page_source
            #利用bs4解析网页源代码
            soup = BeautifulSoup(pageSource,'lxml')
        if max_page == 4:
            driver.find_element_by_xpath('//*[@id="cm_cr-pagination_bar"]/ul/li[6]/a').click()
            time.sleep(6)
            i = i + 1
            pageSource = driver.page_source
            #利用bs4解析网页源代码
            soup = BeautifulSoup(pageSource,'lxml')
        if max_page == 5:
            driver.find_element_by_xpath('//*[@id="cm_cr-pagination_bar"]/ul/li[7]/a').click()
            time.sleep(6)
            i = i + 1
            pageSource = driver.page_source
            #利用bs4解析网页源代码
            soup = BeautifulSoup(pageSource,'lxml')
        if max_page >= 6:
            try:
                if (i<4 or i>(max_page-3)):
                    driver.find_element_by_xpath('//*[@id="cm_cr-pagination_bar"]/ul/li[8]/a').click()
                    time.sleep(6)
                else:
                    driver.find_element_by_xpath('//*[@id="cm_cr-pagination_bar"]/ul/li[9]/a').click()
                    time.sleep(6)
                    # //*[@id="cm_cr-pagination_bar"]/ul/li[8]/a 42 -43 
                    # //*[@id="cm_cr-pagination_bar"]/ul/li[9]/a 41 -42 i = 41
            except:
                pass
            finally:
                i = i + 1
                pageSource = driver.page_source
                #利用bs4解析网页源代码
                soup = BeautifulSoup(pageSource,'lxml')
        print("================== 已进入第{0}页，正在解析，请稍等...  ===================".format(i))
    driver.close()    
for asin in asin_list:
    get_reviews(asin)
