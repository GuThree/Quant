"""
指数数据
"""
from quant.security.check_fun import *
from quant.classes.exception import *

get_ibasic_market_list = ['MSCI', 'CSI', 'SSE', 'SZSE', 'CICC', 'SW', 'OTH']
get_SWindus_level_list = ['L1', 'L2', 'L3']

# 获取指数基础信息
def get_ibasic(market=None):
    if market != None and (market not in get_ibasic_market_list):
        Log.log("%sget_ibasic函数market参数输入值不在范围\n", context.dt)
        exceptional_handle("get_ibasic函数market参数输入值不在范围")
    return pro.index_basic(market=market)

# 获取指数成分股
def get_istocks(index_code=None):
    if index_code == None:
        Log.log("%sget_istocks函数获取指数成分股指数代码index_code参数不能为空\n", context.dt)
        exceptional_handle("get_istocks函数获取指数成分股指数代码index_code参数不能为空")

    df = pro.index_weight(index_code=index_code)
    list_ = df["con_code"].tolist()
    return list_

# 获取指数成份股权重:获取给定日期和指数的指数成分股权重数据
def get_iweights(index_code=None, trade_date=None, start_date=None, end_date=None):
    # index_code和trade_date必须二选一
    if not index_code and not trade_date:
        Log.log("%sget_iweights函数的index_code和trade_date参数必须二选一非空\n", context.dt)
        exceptional_handle("get_iweights函数的index_code和trade_date参数必须二选一非空")

    # 判断trade_date，必须为交易日
    if trade_date != None:
        try:  # 判断输入的日期格式是否为'%Y-%m-%d'
            datetime.datetime.strptime(trade_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("交易日期输入有误,日期格式应改为‘%Y-%m-%d’")

        for index, row in trade_cal.iterrows():
            if row['cal_date'] == trade_date and row['is_open'] == 0:
                Log.log("%sget_iweights函数输入的交易日trade_date为非交易日\n", context.dt)
                exceptional_handle("get_iweights函数输入的交易日trade_date为非交易日")
        trade_date = datetime.datetime.strptime(trade_date, '%Y-%m-%d').strftime('%Y%m%d')

    # 判断start_date
    if start_date != None:
        try:  # 判断输入的日期格式是否为'%Y-%m-%d'
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("开始日期输入有误,日期格式应改为‘%Y-%m-%d’")
        start_date = start_date.strftime('%Y%m%d')

    # 判断end_date
    if end_date == None:
        end_date = context.dt
        end_date = end_date.strftime('%Y%m%d')
    else:
        try:  # 判断输入的日期格式是否为'%Y-%m-%d'
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("截止日期输入有误,日期格式应改为‘%Y-%m-%d’")
        end_date = end_date.strftime('%Y%m%d')

    df = pro.index_weight(index_code=index_code, trade_date=trade_date, start_date=start_date,
                          end_date=end_date)  # 输入时，指数代码和交易日期二选一输入;输出为：指数代码，成分代码，交易日期，权重
    return df

# 获取申万行业列表
def get_SWindus(level=None, name='SW2021'):  # 传入等级进行查询
    if level != None and (level not in get_SWindus_level_list):
        Log.log("%sget_SWindus函数输入等级level有误, 不在范围\n", context.dt)
        exceptional_handle("get_SWindus函数输入等级level有误, 不在范围")

    df = pro.index_classify(level=level, src=name)
    return df[['index_code', 'industry_name', 'level']]

# 获取申万行业成份股
def get_SWindus_stocks(industry_code=None):  # 传入行业代码
    if industry_code is not None:
        if check_industry_code(industry_code) is False:
            Log.log("%sget_SWindus_stocks函数行业代码输入有误\n", context.dt)
            exceptional_handle("get_SWindus_stocks函数行业代码输入有误")
    else:
        Log.log("%sget_SWindus_stocks函数未输入行业代码\n", context.dt)
        exceptional_handle("get_SWindus_stocks函数未输入行业代码")

    df = pro.index_member(index_code=industry_code)
    list_ = df['con_code'].tolist()
    return list_

# 查询股票所属申万行业
def get_SWindus_belong(code=None):  # 传入股票代码
    # 判断股票代码
    if code is not None:
        if check_ts_code(code) is False:
            Log.log("%sget_SWindus_belong函数code格式不正确\n", context.dt)
            exceptional_handle("get_SWindus_belong函数code格式不正确")
    else:
        Log.log("%sget_SWindus_belong函数未输入code行业代码\n", context.dt)
        exceptional_handle("get_SWindus_belong函数未输入code行业代码")
    df = pro.index_member(ts_code=code)
    list_ = df['index_code'].drop_duplicates().tolist()
    return list_
