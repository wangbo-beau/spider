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

        begin_date_str = input("请输入起始日期（yyyy-mm-dd）:")
        end_date_str = input("请输入结束日期（yyyy-mm-dd）:")
        begin_date = datetime.strptime(begin_date_str,"%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        while begin_date > end_date:
            print("起始日期要小于结束日期！")
            begin_date_str = input("请输入起始日期（yyyy-mm-dd）:")
            end_date_str = input("请输入结束日期（yyyy-mm-dd）:")
            begin_date = datetime.strptime(begin_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        print("ok,spider start")

        # 由于是6天的数据，所以1截止到昨天就行了
        while begin_date <= end_date:

            # 对6个洲进行循环找出每个洲里面的国家信息
            for land in lands:
                # 根据本次查询的日期建表，因为mysql不支持数据表名字全为数字，所以加data前缀
                self.output.table_name="world_airdata_" + begin_date.strftime("%Y_%m_%d")
                self.output.create()
                country_response = self.download.country_download(land)
                if (country_response != None):
                    country_dic = self.parser.country_parser(country_response)
                    # 输出测试代码
                    # 对列表里面的各个站点进行循环查找实时数据
                    if (country_response != None):
                        #循环每个国家找出每个国家里面的站点信息
                        for country in country_dic:
                            # 得到点击不同省市的链接返回的ajax返回值，然后进行解析
                            station_response = self.download.station_download(country)
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
                                        data_response = self.download.data_download(station['StationID'],begin_date_str,begin_date_str,land,country,comConfig1="0",comConfig2=comConfig2_11)
                                        # 对00-11点得到的实时数据进行解析
                                        if(data_response!=None):
                                            data_result_list = self.parser.data_parser(data_response,station['CNAME'])
                                        # 再查找本次循环日期的12-23点的数据
                                        data_response = self.download.data_download(station['StationID'],begin_date_str,begin_date_str,land,country,comConfig1="0",comConfig2=comConfig2_22)
                                        # 再对12-23点得到的实时数据进行解析，然后把结果拼接到第一次的后面
                                        if (data_response!=None):
                                            data_result_list.extend(self.parser.data_parser(data_response,station['CNAME']))
                                        data_response = self.download.data_download(station['StationID'],begin_date_str,begin_date_str, land, country,comConfig1="12",comConfig2=comConfig2_11)
                                        # 再对12-23点得到的实时数据进行解析，然后把结果拼接到第一次的后面
                                        if (data_response != None):
                                            data_result_list.extend(self.parser.data_parser(data_response, station['CNAME']))
                                        data_response = self.download.data_download(station['StationID'],begin_date_str,begin_date_str, land, country,comConfig1="12",comConfig2=comConfig2_22)
                                        # 再对12-23点得到的实时数据进行解析，然后把结果拼接到第一次的后面
                                        if (data_response != None):
                                            data_result_list.extend(self.parser.data_parser(data_response, station['CNAME']))
                                        # 批量插入本站点本天的所有结果
                                        # 如果出现前面数据获取失败
                                        if(data_result_list!=[]):
                                            self.output.insert(data_result_list)
                                            # print("succeed:"+station["StationID"]+"站点的"+beginstr+"日期的数据插入完成！")
                                            logger.info("succeed:"+station["StationID"]+"站点的"+begin_date_str+"日期的数据插入完成！")
                                        else:
                                            # print("failure:" + station["StationID"] + "站点的" + beginstr + "日期的数据获取失败！")
                                            logger.info("failure:" + station["StationID"] + "站点的" + begin_date_str + "日期的数据为空！")
                                        time.sleep(random.randint(1,3))
            print("succeed:"+begin_date_str+" 日期的数据插入完成！")
            logger.info("succeed:"+begin_date_str+" 日期的数据插入完成！")
            begin_date = begin_date + timedelta(days=1)
            begin_date_str = begin_date.strftime("%Y-%m-%d")
        self.output.close()
        print("congratulate:所有站点的数据插入完成！")
        logger.info("congratulate:所有站点的数据插入完成！")

if __name__=="__main__":
    lands = [1,2,3,4,5,7]
    # 暂未用到
    # land_dict={"1":"非洲","2":"亚洲","3":"南美洲","4":"北美洲","5":"欧洲","7":"大洋洲",}
    comConfig2_11 = ['131072','65536-1000','65536-925','65536-850','65536-700','65536-500','65536-400','65536-300','65536-250','65536-200','65536-150']
    comConfig2_22 = ['65536-100','65536-70','65536-50','65536-30','65536-20','65536-10','65536-7','65536-5','65536-3','65536-1','8192']
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=r'world_air_log/' + datetime.now().strftime("%Y%m%d%H%M%S") + '.log',
                        filemode='w')
    logger = logging.getLogger()
    spider_main = SpiderMainMain()
    spider_main.start()

