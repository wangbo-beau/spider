
tbSpider: 淘宝爬虫源码

代码采用的是MongoDB数据库，使用pymongo模块进行操作，驱动使用的是火狐，解析模块使用的是beautifulsoup
项目下geckodriver.exe 和 chromedriver.exe 分别为火狐和谷歌的驱动, phantomjs-2.1.1-windows.zip 是
phantomjs浏览器的压缩包，PhantomJS是一个基于Webki内核t的无界面(headless)浏览器，所以运行起来比火狐、
谷歌等完整型的浏览器更高效。

1. 安装selenium：pip install selenium
2. 下载火狐、谷歌或PhantomJS等浏览器的驱动，并将该驱动文件所在目录加入环境变量，其中PhantomJS是将解压
   后bin目录加入环境变量
3. 安装MongoDB的操作模块：pip install pymongo
4. 安装beautifulsoup：pip install bs4

代码运行结果：

![image](https://github.com/wangbo-beau/spider/blob/master/taobao/console%E7%BB%93%E6%9E%9C.png)
![image](https://github.com/wangbo-beau/spider/blob/master/taobao/MongoDB%E7%BB%93%E6%9E%9C.png)
