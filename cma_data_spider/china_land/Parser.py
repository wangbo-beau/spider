# -*- coding:utf-8 -*-

import json
from bs4 import BeautifulSoup
import bs4
import re

class Parser(object):
    def __init__(self):
        pass

    # 解析站点json字符串
    def station_parser(self, station_response):
        # 输出测试代码
        # print("station_response:")
        # print(station_response.decode('utf-8'))

        # 对传过来的站点响应值解码得到json字符串
        station_json = json.loads(station_response.decode('utf-8'))

        # 输出测试代码
        # print(station_json)
        # print("staion_json[stations]的值:")
        # print(station_json['stations'])
        # print("station_json的类型:")
        # print(type(station_json['stations']))

        # 把json字符串里面的stations的值取出来返回一个list
        return station_json['stations']

    # 解析实时数据
    def data_parser(self,data_response,station_name):
        # 输出测试代码
        # print(data_response)
        data_list=[]
        bs = BeautifulSoup(data_response,'html.parser',from_encoding='utf-8')
        # 第一种思路失败告终
        # # <table class="table data-list-table" id="data-list-table">
        # table_node = bs.find("table",class_="table data-list-table")
        # print(table_node.contents[1])
        # # tr是从2到13
        # for i in range(2,14):
        #     tr_node = table_node.contents[i]
        #     td_nodes = tr_node.find_all("td")
        #     print(td_nodes)
        # # data-list-table > tbody > tr:nth-child(2)

        # 第二种思路失败告终
        # tr_node = bs.select("#data-list-table > tr:nth-of-type(2)")
        # print(type(tr_node))
        # for tr in tr_node:
        #     print(tr)

        # 因为第一行是表头，所以先得到第一个tr，然后获取他的兄弟节点
        first_tr_node = bs.find("tr")
        # 输出测试
        # print(type(first_tr_node))

        # 对第一个tr的兄弟节点进行迭代
        for tr_node in first_tr_node.next_siblings:

            #  迭代的会出现string类型，过滤掉不合法的node
            # 按照顺序收集数据，然后等待插入数据库
            if isinstance(tr_node,bs4.element.Tag):
                # 测试用
                # print(type(tr_node))
                # print(tr_node.name)
                # 得到tr里面的所有text，然后进行解析成list
                text = tr_node.get_text().split()
                # 删除第一个没用的列
                text.pop(0)
                # 把station_name放到数据里面
                text.insert(1,station_name)
                # 转化成tuple
                data = tuple(text)
                # 输出测试
                data_list.append(data)
        #         返回结果集
        return data_list