# -*- utf-8 -*-
import time

begin_date_str = input("请输入起始日期（yyyy-mm-dd）:")
end_date_str = input("请输入结束日期（yyyy-mm-dd）:")
begin_date = time.strptime(begin_date_str,"%Y-%m-%d")
end_date = time.strptime(end_date_str, "%Y-%m-%d")
while begin_date > end_date:
    print("起始日期要小于结束日期！")
    begin_date_str = input("请输入起始日期（yyyy-mm-dd）:")
    end_date_str = input("请输入结束日期（yyyy-mm-dd）:")
    begin_date = time.strptime(begin_date_str, "%Y-%m-%d")
    end_date = time.strptime(end_date_str, "%Y-%m-%d")

print("ok")