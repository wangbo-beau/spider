# -*- coding:utf-8 -*-
import copy
import re
import pymongo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from bs4 import BeautifulSoup

# 启动安装的获取浏览器驱动
browser = webdriver.Firefox()
# 设置等待时间
wait = WebDriverWait(browser, 10)
# 设置要存储到数据库的url，数据库名称，集合名称（对应mysql中的数据表名称）
MONGO_URL = "mongodb://localhost:27017/"
MONGO_DB = 'pythonSpider'
MONGO_COLLECTION = 'products'
# 连接到数据库
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
# 设置爬取最大页数和关键词
MAX_PAGE = 100
KEYWORD = '写手'

def get_page(page):
    print('正在爬取第', page, '页')
    try:
        # 使用quote函数编码
        url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
        browser.get(url)
        if page > 1:
            # 得到下一页的input文本框
            input = wait.until(EC.presence_of_element_located((By.XPATH,'//div[@id="mainsrp-pager"]//input[@aria-label="页码输入框"]')))
            # 跳转到下一页的确定按钮
            submit = wait.until(EC.element_to_be_clickable((By.XPATH,'//div[@id="mainsrp-pager"]//span[@class="btn J_Submit"]')))
            # 清空当前文本框内容，设置跳转页码并跳转
            input.clear()
            input.send_keys(page)
            submit.click()
        # 等待直到要爬取的页码的数字高亮显示
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'div#mainsrp-pager li.item.active > span'),str(page)))
        # 等待直到商品列表出现
        wait.until(EC.presence_of_element_located((By.XPATH,'//div[@id="mainsrp-itemlist"]//div[@class="items"]/div[contains(@class,"item")]')))
        get_product()
    except TimeoutException:
        get_page(page)

def get_product():
    """
    提取商品数据
    item_img_url 商品图片url
    item_price 商品价格
    item_title 商品标题
    item_url 商品url
    shop_name 店铺名称
    shop_url 店铺url
    shop_add 店铺地址
    """
    html_cont = browser.page_source
    # with open("tb.html","w",encoding="utf-8") as f:
    #     f.write(html_cont)
    # 使用beautifulsoup解析
    soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
    items = soup.find_all('div',class_=re.compile('item J_MouserOnverReq'))
    product = {}
    for item in items:
        item_img_node = item.find('img', id=re.compile(r'^J_Itemlist_Pic_.*$'))
        try:
            product['item_img_url'] = item_img_node['src'].strip()
        except:
            product['item_img_url'] = item_img_node['data-src'].strip()
        product['item_price'] = item.find('div',class_='price g_price g_price-highlight').find('strong').get_text()
        a_title = item.find('a',id=re.compile(r'^J_Itemlist_TLink_.*$'))
        product['item_title'] = a_title.get_text().strip()
        product['item_url'] = a_title['href'].strip()
        a_shop = item.find('a', class_=re.compile(r'shopname J_MouseEneterLeave J_ShopInfo'))
        product['shop_url'] = a_shop['href'].strip()
        product['shop_name'] = a_shop.get_text().strip()
        product['shop_add'] = item.find('div',class_="location").get_text()
        print(product)
        save_product(product)

# 保存到MongoDB数据库
def save_product(result):
    try:
        # 如果不深拷贝result对象，会造成每次数据库生成的 _id 字段值一样
        item = copy.deepcopy(result)

        # 去掉 _id 字段后比较其他字段值是否存在，若存在则不插入
        for x in db[MONGO_COLLECTION].find(item):
            x.pop("_id")
            if item == x:
                print("this item exist in the db!")
                return

        if db[MONGO_COLLECTION].insert_one(item):
            print('save success!')
    except Exception as e:
        print('save fail!')
        print(e) 

if __name__=="__main__":
    for i in range(1, MAX_PAGE + 1):
        get_page(i)

