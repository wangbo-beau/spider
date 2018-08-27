china_land：是全国地面逐小时数据  http://data.cma.cn/dataService/cdcindex/datacode/A.0012.0001/show_value/normal.html 对应mysql中的cmadata数据库

world_land： 是全球地面逐小时数据  http://data.cma.cn/dataService/cdcindex/datacode/A.0013.0001/show_value/normal.html  对应mysql中的world_landdata数据库

world_air： 是全球高空数据，只有00点和12点，且无效数据较多，网页反应慢  http://data.cma.cn/data/cdcdetail/dataCode/B.0011.0001.html  对应mysql中的world_airdata数据库

各目录下的excel文件则是对数据库中每个表的各要素的解释。

各目录下的log目录则是运行程序中的日志，可查看站点的数据获取信息。

各目录下的bat文件为windows系统下的运行脚本文件，双击即可使用。

程序运行的输入要求输入PHPSESSID值，即登录后的session值，可在网页里面按F12查看。
