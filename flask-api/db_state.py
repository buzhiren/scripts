#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import random
import time


db_user = "xxx"
db_password = "xxxx"
db_database = "xxxxx"
update_host = ["xxxx",]
select_host = ["xxxx",]
localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

base = declarative_base()

class MysqlStatus(base):
    __tablename__ = "t_mysql_status"
    status_id = Column(Integer,primary_key=True)
    status_tag = Column(String(32))
    status_time = Column(Date)


def Update():
    global db_host
    db_host = random.sample(update_host, 1)
    link_address = "mysql+pymysql://%s:%s@%s/%s" %(db_user, db_password, db_host[0], db_database)
    engine = create_engine(link_address, encoding='utf-8')
    Session_class = sessionmaker(bind=engine)
    Session = Session_class()
    res = Session.query(MysqlStatus).filter(MysqlStatus.status_id=="666").filter( \
        MysqlStatus.status_tag=="mysql_status").one()
    res.status_time = localtime
    Session.commit()
    Session.close()
    return True


def Select():
    tag = 0
    file = open('/home/ops/script/monitor_mysql/info', 'w')
    file.write("[update host: %s]  [update time: %s]\n" %(db_host[0], localtime))
    for host in select_host:
        link_address = "mysql+pymysql://%s:%s@%s/%s" %(db_user, db_password, host, db_database)
        engine = create_engine(link_address, encoding='utf-8')
        Session_class = sessionmaker(bind=engine)
        Session = Session_class()
        res_time = Session.query(MysqlStatus).filter(MysqlStatus.status_id=="666").filter( \
        MysqlStatus.status_tag=="mysql_status").one().status_time
        Session.close()
        select_time = str(res_time)
        if select_time != localtime:
            tag = 4
            content = "%s: Synchronization error !!!" %host
            file.write(content + "\n")
    file.close()
    print(tag)
    return True



if __name__ == "__main__":
    Update()
    time.sleep(1)
    Select()