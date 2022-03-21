import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from dateutil.parser import parse
import tushare as ts

#用户开始设定的数值
CASH = 100000
START_DATE = '2016-01-23'
END_DATE = '2016-06-01'

ts.set_token('9e22c84922d0c39ef78ae4c9562c00dfa79775795f022c03e1432455')
pro = ts.pro_api()
trade_cal = pd.read_csv("trade_cal.csv")

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

g = G()
context = Context(CASH, START_DATE, END_DATE)

#设置基准
def set_benckmark(security):
    context.benchmark = security

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

#按股数下单(作为基础函数)
def _order(today_data, security, amount):
    p = today_data['open']

    if len(today_data) == 0:
        print("今天停牌")
        return

    if context.cash - amount * p < 0:
        amount = int(context.cash / p)
        print("现金不足,已调整为%d" % (amount))

    if amount % 100 != 0:
        if amount != -context.positions.get(security, 0):
            amount = int(amount / 100) * 100
            print("不是100的倍数,已调整为%d" % amount)

    if context.positions.get(security, 0) < -amount:
        amount = -context.positions.get(security, 0)
        print("卖出股票不能超出持仓数量,已调整为%d" % amount)
    
    context.positions[security] = context.positions.get(security, 0) + amount

    context.cash -= amount * p

    if context.positions[security] == 0:
         del context.positions[security]

#按股数下单
def order(security, amount):
    today_data = get_today_data(security)
    _order(today_data, security, amount)

#按目标股数下单
def order_target(security, amount):
    if amount < 0:
        print("数量不能为负,已调整成为0")
        amount = 0
    
    today_data = get_today_data(security)
    hold_amount = context.positions.get(security, 0)  #ToDo  T+1问题
    delta_amount = amount - hold_amount
    _order(today_data, security, delta_amount)

#按价值下单
def order_value(security, value):
    today_data = get_today_data(security)
    amount = int(value / today_data['open'])
    _order(today_data, security, amount)

#按目标价值下单
def order_target_value(security, value):
    today_data = get_today_data(security)
    if value < 0:
        print("价值不能为负,已调整为0")
        value = 0

    hold_value = context.positions.get(security, 0) * today_data['open']
    delta_value = value - hold_value
    order_value(security, delta_value)

def initialize(context):
    set_benckmark('000001.SZ')
    g.p1 = 5
    g.p2 = 60
    g.security = '000006.SZ'

def handle_data(context):
    hist = attribute_history(g.security, g.p2)
    ma5 = hist['close'][-g.p1].mean()
    ma60 = hist['close'].mean()

    if ma5 > ma60 and g.security not in context.positions:
        order_value(g.security, context.cash)
    elif ma5 < ma60 and g.security in context.positions:
        order_target(g.security, 0)

#
def run():
    plt_df = pd.DataFrame(index=pd.to_datetime(context.date_range), columns=['value'])
    init_value = context.cash
    initialize(context)
    last_price = {}
    for dt in context.date_range:
        context.dt = parse(dt)
        handle_data(context)
        value = context.cash
        for stock in context.positions:
            #考虑停牌情况
            today_data = get_today_data(stock)
            if len(today_data) == 0:
                p = last_price[stock]
            else:
                p = today_data['open']
                last_price[stock] = p
            value += p * context.positions[stock]
        plt_df.loc[dt, 'value'] = value
    plt_df['ratio'] = (plt_df['value'] - init_value) / init_value
    
    bm_df = attribute_daterange_history(context.benchmark, context.start_date, context.end_date)
    bm_init = bm_df['open'][0]
    plt_df['benckmark_ratio'] = (bm_df['open'] - bm_init) / bm_init
    
    plt_df[['ratio','benckmark_ratio']].plot()
    plt.show()

run()