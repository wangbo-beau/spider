# -*- codiing:utf-8 -*-
import sys
import os

print(os.path.dirname(__file__))#D:/java/jdk1.8/workspace/tbSpider/cma_data_spider
curPath = os.path.abspath(os.path.dirname(__file__))
print(curPath)#D:/java/jdk1.8/workspace/tbSpider/cma_data_spider
rootPath = os.path.split(curPath)[0]
#print(sys.path)
#['D:\\java\\jdk1.8\\workspace\\tbSpider\\cma_data_spider', 'D:\\java\\jdk1.8\\workspace\\tbSpider',
# 'D:\\Program Files (x86)\\python\\python35.zip', 'D:\\Program Files (x86)\\python\\DLLs',
# 'D:\\Program Files (x86)\\python\\lib', 'D:\\Program Files (x86)\\python',
# 'D:\\Program Files (x86)\\python\\lib\\site-packages', 'D:\\Program Files (x86)\\python\\lib\\site-packages\\win32',
# 'D:\\Program Files (x86)\\python\\lib\\site-packages\\win32\\lib',
# 'D:\\Program Files (x86)\\python\\lib\\site-packages\\Pythonwin']
print(rootPath)#D:\java\jdk1.8\workspace\tbSpider
sys.path.append(rootPath)
#print(sys.path)
#['D:\\java\\jdk1.8\\workspace\\tbSpider\\cma_data_spider', 'D:\\java\\jdk1.8\\workspace\\tbSpider',
# 'D:\\Program Files (x86)\\python\\python35.zip', 'D:\\Program Files (x86)\\python\\DLLs',
# 'D:\\Program Files (x86)\\python\\lib', 'D:\\Program Files (x86)\\python',
# 'D:\\Program Files (x86)\\python\\lib\\site-packages', 'D:\\Program Files (x86)\\python\\lib\\site-packages\\win32',
# 'D:\\Program Files (x86)\\python\\lib\\site-packages\\win32\\lib',
# 'D:\\Program Files (x86)\\python\\lib\\site-packages\\Pythonwin','D:\\java\\jdk1.8\\workspace\\tbSpider']

import Download,Parser,Output
from datetime import datetime,timedelta
import time
import random
import logging

class SpiderMainMain(object):
    def __init__(self):
        self.download = Download.Download(logger)
        self.parser = Parser.Parser()
        self.output = Output.Output()
    def start(self):
        PHPSESSID = input("请输入PHPSESSID:")
        while PHPSESSID =="":
            PHPSESSID = input("请输入PHPSESSID:")
        self.download.PHPSESSID = PHPSESSID
        now = datetime.now()
        print(now)

        dayAccount = int(input("请输入要爬取的天数(1~6):"))
        while dayAccount < 1 and dayAccount > 6:
            dayAccount = int(input("请重新输入要爬取的天数(1~6):"))

        # 由于是6天的数据，所以1截止到昨天就行了
        for i in range(-6, dayAccount-6):
        # for i in range(-5,0):
            # 得到本次循环的日期
            begintime = now + timedelta(days=i)
            # 把日期转化成字符串的形式
            beginstr = begintime.strftime("%Y-%m-%d")
            # 根据本次查询的日期建表，因为mysql不支持数据表名字全为数字，所以加data前缀
            self.output.table_name="data_"+begintime.strftime("%Y_%m_%d")
            self.output.create()
            # 对31个省市进行循环找出每个省市对应的站点信息
            for pro in province:
                # 得到点击不同省市的链接返回的ajax返回值，然后进行解析
                station_response = self.download.station_download(pro)
                # 解析返回的json数据，来得到每个省份对应的站点list，然后迭代循环查找实时数据
                if(station_response!=None):
                    station_list = self.parser.station_parser(station_response)
                    # 输出测试代码
                    # print("station_list:")
                    # print(station_list)
                    # 对列表里面的各个站点进行循环查找实时数据
                    if(station_list!=None):
                        for station in station_list:
                            # print(station['StationID'])
                            data_result_list = []
                            # 先查找本次循环日期的00-11点的数据
                            data_response = self.download.data_download(station['StationID'],beginstr+" 00",beginstr+" 11")
                            # 对00-11点得到的实时数据进行解析
                            if(data_response!=None):
                                data_result_list = self.parser.data_parser(data_response,station['CNAME'])
                            # 再查找本次循环日期的12-23点的数据
                            data_response = self.download.data_download(station['StationID'],beginstr+" 12",beginstr+" 23")
                            # 再对12-23点得到的实时数据进行解析，然后把结果拼接到第一次的后面
                            if (data_response!=None):
                                data_result_list.extend(self.parser.data_parser(data_response,station['CNAME']))
                            # 批量插入本站点本天的所有结果
                            # 如果出现前面数据获取失败
                            if(data_result_list!=[]):
                                self.output.insert(data_result_list)
                                # print("succeed:"+station["StationID"]+"站点的"+beginstr+"日期的数据插入完成！")
                                logger.info("succeed:"+station["StationID"]+"站点的"+beginstr+"日期的数据插入完成！")
                            else:
                                # print("failure:" + station["StationID"] + "站点的" + beginstr + "日期的数据获取失败！")
                                logger.info("failure:" + station["StationID"] + "站点的" + beginstr + "日期的数据为空！")
                            time.sleep(random.randint(1,3))
            print("succeed:"+beginstr+" 日期的数据插入完成！")
            logger.info("succeed:"+beginstr+" 日期的数据插入完成！")
        self.output.close()
        print("congratulate:"+str(dayAccount)+"天的所有站点的数据插入完成！")
        logger.info("congratulate:"+str(dayAccount)+"天的所有站点的数据插入完成！")

if __name__=="__main__":
    province = [110,120,130,140,150,210,220,230,310,320,330,340,350,360,370,410,420,430,440,450,460,
               500,510,520,530,540,610,620,630,640,650]
    # 暂未用到
    # province_dict={"110":"北京市","120":"天津市","130":"河北省","140":"山西省","150":"内蒙古自治区",
    #                "210":"辽宁省","220":"吉林省","230":"黑龙江省",
    #                "310":"上海市","320":"江苏省","330":"浙江省","340":"安徽省","350":"福建省","360":"江西省","370":"山东省",
    #                "410":"河南省","420":"湖北省","430":"湖南省","440":"广东省","450":"广西壮族自治区","460":"海南省",
    #                "500":"重庆市","510":"四川省","520":"贵州省","530":"云南省","540":"西藏自治区",
    #                "610":"陕西省","620":"甘肃省","630":"青海省","640":"宁夏回族自治区","650":"新疆维吾尔自治区",}
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=r'china_land_log/' + datetime.now().strftime("%Y%m%d%H%M%S") + '.log',
                        filemode='w')
    logger = logging.getLogger()
    spider_main = SpiderMainMain()
    spider_main.start()

