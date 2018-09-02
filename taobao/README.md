
tbSpider: 淘宝爬虫源码

代码采用的是MongoDB数据库，使用pymongo模块进行操作，驱动使用的是火狐，解析模块使用的是beautifulsoup
项目下geckodriver.exe、chromedriver.exe和phantomjs.exe分别为火狐和谷歌的驱动，其中PhantomJS是一个基
于Webkit内核的无界面(headless)浏览器，所以运行起来比火狐、谷歌等完整型的浏览器更高效。

1. 安装selenium：pip install selenium
2. 下载火狐、谷歌或PhantomJS等浏览器的驱动，并将该驱动文件所在目录加入环境变量的Path中;如果不加入
   环境变量Path中，也可以在程序中指定驱动所在目录，详见代码
3. 安装MongoDB的操作模块：pip install pymongo
4. 安装beautifulsoup：pip install bs4

代码运行结果：

![image](https://github.com/wangbo-beau/spider/blob/master/taobao/console%E7%BB%93%E6%9E%9C.png)
![image](https://github.com/wangbo-beau/spider/blob/master/taobao/MongoDB%E7%BB%93%E6%9E%9C.png)
