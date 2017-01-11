# -*- coding: utf-8 *-*
import sys
sys.path.append('/Users/lish/PycharmProjects/pyweb/hive')
from tornado.options import options as opts
from app import DB
import tornado,time
import vote
from hive import hiveDB






class AutoTask(object):
    def __init__(self):
        self.r_db = DB(opts.db_r_host,opts.db_r_port,opts.db_r_name,opts.db_r_user,opts.db_r_password)
        self.w_db = DB(opts.db_w_host,opts.db_w_port,opts.db_w_name,opts.db_w_user,opts.db_w_password)
        self.r_hivedb=hiveDB('182.92.183.76',9084)

    def test(self,para):
        print 'tesyt'
        print para

    # 自动执行的计划任务
    def auto_check_task(self):
        #从mysql数据库中取出数据
        # sql = "SELECT * from prd_bid_c limit 5"
        # self.r_db.query(sql,None,self.test)

        #从hive数据库中取出数据
        # vars_hql='desc dmn.us_am_uid_tag'
        # hql = 'select * from dmn.us_am_uid_tag limit 5'
        # self.r_hivedb.query(vars_hql,hql,self.test)
        # print "hi~"
        vote.vote(1967)


