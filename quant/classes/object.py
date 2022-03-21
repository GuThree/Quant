import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from dateutil.parser import parse
import os
import tushare as ts
from sqlalchemy import create_engine

engine_ts = create_engine('mysql+pymysql://root:gsr3316806@127.0.0.1:3306/TushareDB?charset=utf8&use_unicode=1')
sql = """SELECT * FROM trade_cal LIMIT 20"""
trade_cal = pd.read_sql_query(sql, engine_ts)

trade_cal = trade_cal[['cal_date','is_open']]
for i in range(len(trade_cal)):
    trade_cal['cal_date'][i] = parse(trade_cal['cal_date'][i]).strftime('%Y-%m-%d')
print(trade_cal)

print(trade_cal)
class Context:
    def __init__(self, cash, start_date, end_date):
        self.cash = cash
        self.start_date = start_date
        self.end_date = end_date
        self.positions = {}
        self.benchmark = None
        self.date_range = trade_cal[(trade_cal['is_open'] == 1) & \
                                    (trade_cal['cal_date'] >= start_date) & \
                                    (trade_cal['cal_date'] <= end_date) ]['cal_date'].values
        self.dt = None



class G:
    pass