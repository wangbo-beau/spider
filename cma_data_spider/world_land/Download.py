# -*- coding:utf-8 -*-

import socket
import urllib
import logging
from urllib import request
from http import cookiejar

class Download(object):
    def __init__(self,logger):
        self.logger = logger
        self.PHPSESSID = ""
        self.country_url = "http://data.cma.cn/dataService/ajax.html"
        self.station_url = "http://data.cma.cn/dataService/ajax.html"
        self.data_url = "http://data.cma.cn/data/search.html?dataCode=A.0012.0001"
        # 用来存储cookie
        self.cookie = cookiejar.CookieJar()
        # 用来管理cookie
        self.handle = request.HTTPCookieProcessor(self.cookie)
        self.opener = request.build_opener(self.handle)

        #下载动态的ajax页面，服务器响应值为json类型的数据，里面存放国家信息
    def country_download(self, land):
        print(land)
        req_header={
                'Accept':'application/json, text/javascript, */*; q=0.01',
                # Accept-Encoding:gzip, deflate
                'Accept-Language':'zh-CN,zh;q=0.8',
                'Connection':'keep-alive',
                # 'Content-Length':'63',
                'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                'Cookie':'PHPSESSID='+self.PHPSESSID+'; '
                         'trueName=%E7%8E%8B%E8%8E%89%E8%8E%89;userName=3C60FE2E2B89467EA092407E92C3ADEF; ',
                'Host':'data.cma.cn',
                'Origin':'http://data.cma.cn',
                'Referer':'http://data.cma.cn/dataService/index/datacode/A.0012.0001.html',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/49.0.2623.75 Safari/537.36',
                'X-Requested-With':'XMLHttpRequest'}
        values={
                'act':'getCountrysByContinentCode',
                'continentCode':land,
                'dataCode':'A.0013.0001'}
        return self._download(self.station_url,values,req_header,land)

    # 下载动态的ajax页面，服务器响应值为json类型的数据，里面存放站点信息
    def station_download(self, country):
        # print(country)
        req_header = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            # Accept-Encoding:gzip, deflate
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            # 'Content-Length': '63',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'PHPSESSID=' + self.PHPSESSID + '; '
                                                      'trueName=%E7%8E%8B%E8%8E%89%E8%8E%89;userName=3C60FE2E2B89467EA092407E92C3ADEF; ',
            'Host': 'data.cma.cn',
            'Origin': 'http://data.cma.cn',
            'Referer': 'http://data.cma.cn/dataService/index/datacode/A.0012.0001.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/49.0.2623.75 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'}
        values = {
            'act': 'getStationsByCountryCode',
            'countryCode': country,
            'dataCode': 'A.0013.0001'}
        return self._download(self.country_url, values, req_header, country)

    # 下载实时数据页面，服务器响应值为整个页面
    def data_download(self, stationId, begintime, endtime,landId,countryId):
        req_header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            # 'Accept-Encoding':'gzip, deflate',
            'Connection': 'keep-alive',
            # 'Content-Length': '595',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie':'PHPSESSID='+self.PHPSESSID+';userLoginKey=c56b937b9b882af22b5d66e53200f78a; '
                'trueName=%E7%8E%8B%E8%8E%89%E8%8E%89;userName=3C60FE2E2B89467EA092407E92C3ADEF; ',
            'Host': 'data.cma.cn',
            'Origin': 'http://data.cma.cn',
            'Referer': 'http://data.cma.cn/dataService/index/datacode/A.0012.0001.html',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/49.0.2623.75 Safari/537.36'
        }
        values = [('dateS', begintime), ('dateE', endtime), ('hidden_limit_timeRange', '1,10;90,15,1'),
                ('hidden_limit_timeRangeUnit', 'Station;Day'), ('isRequiredHidden[]', 'dateS'), ('isRequiredHidden[]', 'dateE'),
                ('chooseType','Station'),('isRequiredHidden[]', 'station_ids[]'), ('continentCode',landId),('countryCode',countryId),
                ('station_ids[]', stationId), ('station_maps',''),('select','on'),('elements[]', 'PRS'),
                ('elements[]', 'PRS_Sea'), ('elements[]', 'WIN_D'), ('elements[]', 'WIN_S'),
                ('elements[]', 'TEM'), ('elements[]', 'RHU'),('elements[]', 'PRE_1h'),
                ('isRequiredHidden[]', 'elements[]'), ('dataCode', 'A.0013.0001'),('dataCodeInit', 'A.0013.0001'),
                  ('show_value','normal')]
        return self._download(self.data_url,values,req_header,stationId)

    def _download(self,req_url,values,req_header,exceptInfo):
        maxTryNum = 10
        for tries in range(maxTryNum):
            try:
                req_data = urllib.parse.urlencode(values).encode('utf-8')
                req = request.Request(req_url.split("\n")[0],req_data,req_header)
                response = self.opener.open(req,timeout=10)
                # for item in self.cookie:
                #     print(item.name+":"+item.value)
                # abc = response.read()
                # with open(str(exceptInfo)+".html","w",encoding='utf8') as f:
                #     f.write(abc.decode('utf8'))
                return response.read()
            except request.URLError as e:
                if tries < (maxTryNum - 1):
                    continue
                if hasattr(e, "code"):
                    print("获取 "+str(exceptInfo)+" 时发生request.HTTPError异常," + "错误code: " + str(e.code()))
                    self.logger.error("获取 "+str(exceptInfo)+" 时发生request.HTTPError异常," + "错误code: " + str(e.code()))
                if hasattr(e, "reason"):
                    print("获取 "+str(exceptInfo)+" 时发生request.URLError异常")
                    self.logger.error("获取 "+str(exceptInfo)+" 时发生request.URLError异常")
            except socket.timeout as e:
                if tries < (maxTryNum - 1):
                    continue
                print("获取 "+str(exceptInfo) + " 时发生socket.timeout异常")
                self.logger.error("获取 "+str(exceptInfo) + " 发生socket.timeout异常")
            except Exception as e:
                if tries < (maxTryNum - 1):
                    continue
                print("获取 " + str(exceptInfo) + " 时发生其他异常" + e)
                self.logger.error("获取 " + str(exceptInfo) + " 时发生其他异常")
        return None
