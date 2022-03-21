import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from dateutil.parser import parse
import tushare as ts

ts.set_token('9e22c84922d0c39ef78ae4c9562c00dfa79775795f022c03e1432455')
pro = ts.pro_api()
trade_cal = pd.read_csv("..\\files\\trade_cal.csv")

#获取前n日的历史数据
def attribute_history(security, count, fields=('open', 'close', 'high', 'low', 'vol')):
    end_date = (context.dt - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    start_date = trade_cal[(trade_cal['is_open'] == 1) &
                            (trade_cal['cal_date'] <= end_date )][-count:].iloc[0, :]['cal_date']
    return attribute_daterange_history(security, start_date, end_date, fields)

#获取指定日期范围内的历史数据
def attribute_daterange_history(security, start_date, end_date, fields=('open', 'close', 'high', 'low', 'vol')):
    start_date = parse(start_date).strftime('%Y%m%d')
    end_date = parse(end_date).strftime('%Y%m%d')
    df = pro.daily(ts_code=security, start_date=start_date, end_date=end_date)
    df.index = df['trade_date'].values
    return df[list(fields)]

#获取今天的价格
def get_today_data(security):
    today = context.dt.strftime('%Y%m%d')
    try:
        f = open(security+'.csv','r')
        data = pd.read_csv(f, index_col='date', parse_dates=['date']).loc[today,:]
    except FileNotFoundError:
        data = pro.daily(ts_code=security, start_date=today, end_date=today).iloc[0,:]
    except KeyError:
        data = pd.Series()
    return data
