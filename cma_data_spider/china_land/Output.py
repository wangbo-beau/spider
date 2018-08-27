# -*- coding:utf-8 -*-

from mysql import connector

class Output(object):
    def __init__(self):
        self.table_name = ""
        self.sqlc = " (id int(11) NOT NULL AUTO_INCREMENT,station_id int(10) DEFAULT NULL," \
                    "station_name varchar(255) DEFAULT NULL,year int(4) DEFAULT NULL," \
                    "mon int(4) DEFAULT NULL,day int(4) DEFAULT NULL,hour int(4) DEFAULT NULL," \
                    "prs float DEFAULT NULL,prs_sea float DEFAULT NULL,win_s_max float DEFAULT NULL," \
                    "win_s_inst_max float DEFAULT NULL,win_d_inst_max float DEFAULT NULL," \
                    "win_d_avg_2mi float DEFAULT NULL,win_s_avg_2mi float DEFAULT NULL," \
                    "win_d_s_max float DEFAULT NULL,tem float DEFAULT NULL," \
                    "rhu float DEFAULT NULL,vap float DEFAULT NULL,pre_1h float DEFAULT NULL," \
                    "vis float DEFAULT NULL,wea_now float DEFAULT NULL,tcc float DEFAULT NULL," \
                    "tcc_m_l float DEFAULT NULL,tcc_low float DEFAULT NULL," \
                    "w_level float DEFAULT NULL,sen_tem float DEFAULT NULL," \
                    "PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
        self.conn = connector.connect(host="localhost",user="root",password="",database="cmadata",charset="utf8")
        # 目前没用该段
        # self.sqli_attr = "(station_id,station_name,year,mon,day,hour," \
        #                  "prs,prs_sea,win_s_max,win_s_inst_max,win_d_inst_max,win_d_avg_10mi," \
        #                  "win_s_avg_10mi,win_d_s_max,tem,rhu,vap,pre_1h)"
        self.sqli = " values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    def create(self):
        cursor = self.conn.cursor()
        drop_sql = "drop table if exists " + self.table_name
        cursor.execute(drop_sql)
        create_sql = "CREATE TABLE " + self.table_name + "" + self.sqlc
        # 输出测试代码
        # print(create_sql)
        cursor.execute(create_sql)
        cursor.close()
        self.conn.commit()
    def insert(self,data_result_list):
        insert_sql = "insert into "+self.table_name+self.sqli
        cursor = self.conn.cursor()
        # 输出测试代码
        # print(data_result_list)

        cursor.executemany(insert_sql,data_result_list)
        cursor.close()
        self.conn.commit()

    def close(self):
        self.conn.close()
