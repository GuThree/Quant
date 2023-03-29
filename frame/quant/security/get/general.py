"""
证券日行情获取函数
此文件的函数只支持股票、指数、基金
"""

from quant.security.check_fun import *
from quant.classes.exception import *
import sys

# 获得交易日或指定范围内交易日
def get_trade_days(start_date=None, end_date=None):
    if (start_date is not None and end_date is None) or (start_date is None and end_date is not None):
        Log.log("%sget_trade_day参数start_date和end_date需成对出现", context.dt)
        exceptional_handle("get_trade_day参数start_date和end_date需成对出现")

    if start_date is not None and end_date is not None:
        df = trade_cal[(trade_cal['is_open'] == 1) & (trade_cal['cal_date'] <= end_date) & (trade_cal['cal_date'] >= start_date)]
    else:
        df = trade_cal[(trade_cal['is_open'] == 1)]

    return df

# 获取今天的价格
def get_today_data(security):
    # today = context.dt.strftime('%Y%m%d')
    today = datetime.datetime.strptime(context.dt, '%Y-%m-%d').strftime('%Y%m%d')
    try:
        i = security
        stock = ''
        index = ''
        fund = ''
        if (i[0:3] == '600' or i[0:3] == '601' or i[0:3] == '603' or i[0:3] == '605' or i[0:3] == '900' or i[0:3] == '688') and i[7:9] == 'SH':
            stock = i
        elif (i[0:3] == '000' or i[0:3] == '002' or i[0:3] == '300') and i[7:9] == 'SZ':  # 深市股票
            stock = i
        elif i[0:3] == '000' and i[7:9] == 'SH':
            index = i
        elif i[0:3] == '399' and i[7:9] == 'SZ':
            index = i
        elif (i[0:3] == '150' or i[0:3] == '159' or i[0:3] == '160' or i[0:3] == '161' or i[0:3] == '162' or i[0:3] == '163' or i[0:3] == '164' or i[0:3] == '165' or
                i[0:3] == '167' or i[0:3] == '168' or i[0:3] == '184') and i[7:9] == 'SZ':
            fund = i
        elif (i[0:3] == '501' or i[0:3] == '502' or i[0:3] == '505' or i[0:3] == '510' or i[0:3] == '511' or i[0:3] == '512' or i[0:3] == '513' or i[0:3] == '518') and i[7:9] == 'SH':
            fund = i

        if stock != '':
            data = pro.daily(ts_code=stock, start_date=today, end_date=today).iloc[0, :]
        elif index != '':
            data = pro.index_daily(ts_code=index, start_date=today, end_date=today).iloc[0, :]
        elif fund != '':
            data = pro.fund_daily(ts_code=fund, start_date=today, end_date=today).iloc[0, :]
        else:
            Log.log("%sget_today_data函数无法识别此未知类型证券", context.dt)
            exceptional_handle("get_today_data函数无法识别此未知类型证券")
    except KeyError:    # 停牌
        data = pd.Series()
    return data

# 获取历史数据，可查询多个标的单个数据字段
def history(count, unit='1d', fields='close', security_list=None,
            isdf=True):  # 这里的fields只能取一个值！且为元组类型，最后面要加一个逗号；输入的股票代码为列表类型，例如['000001.SZ','600000.SH']
    # count参数检验
    if type(count) != int or count == None or count <= 0:
        Log.log("%shistory函数输入返回的目标行数参数不正确\n", context.dt)
        exceptional_handle("history函数输入返回的目标行数参数不正确")

    # fields参数检验
    if not (
            fields != 'open' or fields != 'high' or fields != 'low' or fields != 'close' or fields != 'pre_close' or fields != 'change' or fields != 'pct_chg' or fields != 'vol' or fields != 'amount'):
        Log.log("%shistory函数输入的证券属性参数有误\n", context.dt)
        exceptional_handle("history函数输入的证券属性参数有误")

    # security_list参数检验
    if security_list == None:
        if len(context.universe) != 0:
            security_list = context.universe
        else:
            Log.log("%shistory函数没有输入证券参数且证券池为空\n", context.dt)
            exceptional_handle("history函数没有输入证券参数且证券池为空")
    elif type(security_list) == type(''):
        if len(security_list) != 9:
            Log.log("%shistory函数输入字符串单只证券长度字符不正确\n", context.dt)
            exceptional_handle("history函数输入字符串单只证券长度字符不正确")
        t = security_list
        security_list = []
        security_list.append(t)

    # 计算日期
    # end_date = (context.dt).strftime('%Y-%m-%d')  # end_date为今天,这里的日期格式与trade_cal的格式对应
    end_date = datetime.datetime.strptime(context.dt, '%Y-%m-%d').strftime('%Y-%m-%d')
    if unit[1] == 'd':  # 回溯时以天数为单位
        date_list = []
        date_range = trade_cal[(trade_cal['cal_date'] <= end_date)]
        for index, row in date_range.iterrows():  # 遍历date_range这个Dateframe对象
            if count == 0:
                break
            if row['is_open'] == 1:
                date_list.append(datetime.datetime.strptime(row['cal_date'], '%Y-%m-%d').strftime('%Y%m%d'))
                count -= 1
    elif unit[1] == 'w':  # 回溯时以周为单位，将索引到的时间数据放入一个列表中
        date_list = []
        for i in range(count):
            judge_date = trade_cal[(trade_cal['cal_date'] <= end_date)][((i * 7) + 1):].iloc[0, :][
                'is_open']  # 获取到时间，而后判断是否为交易日；若不是，则返回前面最近一日的交易日的数据
            if judge_date == 1:
                date_list.append(datetime.datetime.strptime(
                    trade_cal[(trade_cal['cal_date'] <= end_date)][((i * 7) + 1):].iloc[0, :]['cal_date'],
                    '%Y-%m-%d').strftime('%Y%m%d'))
            else:  # 回溯
                date_range = trade_cal[(trade_cal['cal_date'] <= end_date)][((i * 7) + 1)::1]
                for index, row in date_range.iterrows():  # 遍历date_range这个Dateframe对象
                    if row['is_open'] == 1:
                        date_list.append(datetime.datetime.strptime(row['cal_date'], '%Y-%m-%d').strftime('%Y%m%d'))
                        break
    elif unit[1] == 'm':  # 回溯时以月为单位
        date_list = []
        for i in range(count):
            judge_date = trade_cal[(trade_cal['cal_date'] <= end_date)][((i * 30) + 1):].iloc[0, :][
                'is_open']  # 获取到时间，而后判断是否为交易日；若不是，则返回前面最近一日的交易日的数据
            if judge_date == 1:
                date_list.append(datetime.datetime.strptime(
                    trade_cal[(trade_cal['cal_date'] <= end_date)][((i * 30) + 1):].iloc[0, :]['cal_date'],
                    '%Y-%m-%d').strftime('%Y%m%d'))
            else:  # 往前回溯，找到离该日期最近一天的交易日
                date_range = trade_cal[(trade_cal['cal_date'] <= end_date)][((i * 30) + 1)::1]
                for index, row in date_range.iterrows():  # 遍历date_range这个Dateframe对象
                    if row['is_open'] == 1:
                        date_list.append(datetime.datetime.strptime(row['cal_date'], '%Y-%m-%d').strftime('%Y%m%d'))
                        break
    else:
        Log.log("%shistory函数单位时间长度设置有误\n", context.dt)
        exceptional_handle("history函数单位时间长度设置有误")

    # 返回的为DateFrame类型
    if isdf == True:
        dframe = pd.DataFrame()  # 添加得到的每个交易日数据信息  columns='ts_code','trade_date','open','high','low  close','pre_close','change','pct_chg','vol','amount'
        #遍历security_list，将股票代码、指数代码、基金代码分别放入不同的列表中
        dframe1 = pd.DataFrame()
        dframe2 = pd.DataFrame()
        dframe3 = pd.DataFrame()
        stock_list = []
        index_list = []
        fund_list = []
        for i in security_list:
            if (i[0:3] == '600' or i[0:3] == '601' or i[0:3] == '603' or i[0:3] == '605' or i[0:3] == '900' or i[0:3] == '688') and i[7:9]=='SH':
                stock_list.append(i)
            elif (i[0:3] == '000' or i[0:3] == '002' or i[0:3] == '300') and i[7:9] == 'SZ':   # 深市股票
                stock_list.append(i)
            elif i[0:3] == '000' and i[7:9] == 'SH':
                index_list.append(i)
            elif i[0:3] == '399' and i[7:9] == 'SZ':
                index_list.append(i)
            elif (i[0:3] == '150' or i[0:3] == '159' or i[0:3] == '160' or i[0:3] == '161' or i[0:3] == '162' or i[0:3] == '163' or i[0:3] == '164' or i[0:3] == '165' or i[0:3] == '166' or i[0:3] == '167' or i[0:3] == '168' or i[0:3] == '169' or i[0:3] == '184') and i[7:9]=='SZ':
                fund_list.append(i)
            elif (i[0:3] == '501' or i[0:3] == '502' or i[0:3] == '505' or i[0:3] == '510' or i[0:3] == '511' or i[0:3] == '512' or i[0:3] == '513' or i[0:3] == '518') and i[7:9] == 'SH':
                fund_list.append(i)
        stock_list = ','.join(stock_list)   # 转化为字符串，应用到接口
        index_list = ','.join(index_list)
        fund_list = ','.join(fund_list)
        terminal = []   # 暂存3个dframe
        terminal1 = []  # 存放不为空的dframe
        if stock_list != '':
            for i in date_list:
                DF1 = pro.daily(ts_code=stock_list, start_date=i, end_date=i)
                dframe1 = pd.concat([dframe1,DF1], ignore_index=True)
            terminal.append(dframe1)
        if index_list != '':
            for i in date_list:
                DF2 = pro.index_daily(ts_code=index_list, start_date=i, end_date=i)
                dframe2 = pd.concat([dframe2, DF2], ignore_index=True)
            terminal.append(dframe2)
        if fund_list != '':
            for i in date_list:
                DF3 = pro.fund_daily(ts_code=fund_list, start_date=i, end_date=i)
                dframe3 = pd.concat([dframe3, DF3], ignore_index=True)
            terminal.append(dframe3)

        for i in terminal:
            if not i.empty:
                terminal1.append(i)
        if len(terminal1) == 1:
            dframe = terminal1[0]
        elif len(terminal1) == 2:
            dframe = pd.merge(terminal1[0], terminal1[1], how='outer')
        elif len(terminal1) == 3:
            dframe = pd.merge(terminal1[0], terminal1[1], how='outer')
            dframe = pd.merge(dframe, terminal1[2], how='outer')
        #判断dframe是否为空
        if dframe.empty:
            Log.log("%shistory函数获得空数据\n", context.dt)
            exceptional_handle("history函数获得空数据")

        dframe['trade_date'] = dframe['trade_date'].astype('datetime64[ns]')  # 格式化时间
        dframe.index = dframe['trade_date'].values  # 以时间为索引
        dframe = dframe.sort_values('trade_date')  # 时间从久到近排序
        dframe = dframe[[fields, 'ts_code']]
        # security_list = security_list.split(',')    # 股票代码保存在列表中
        new_dframe = pd.DataFrame(columns=security_list)
        for index, row in dframe.iterrows():
            new_dframe.loc[index, row['ts_code']] = row[fields]
        return new_dframe

    # 返回的为dict类型
    elif isdf == False:
        dframe = pd.DataFrame()  # 添加得到的每个交易日数据信息  columns='ts_code','trade_date','open','high','low  close','pre_close','change','pct_chg','vol','amount'
        # 遍历security_list，将股票代码、指数代码、基金代码分别放入不同的列表中
        dframe1 = pd.DataFrame()
        dframe2 = pd.DataFrame()
        dframe3 = pd.DataFrame()
        stock_list = []
        index_list = []
        fund_list = []
        for i in security_list:
            if (i[0:3] == '600' or i[0:3] == '601' or i[0:3] == '603' or i[0:3] == '605' or i[0:3] == '900' or i[0:3] == '688') and i[7:9]=='SH':
                stock_list.append(i)
            elif (i[0:3] == '000' or i[0:3] == '002' or i[0:3] == '300') and i[7:9] == 'SZ':  # 深市股票
                stock_list.append(i)
            elif i[0:3] == '000' and i[7:9] == 'SH':
                index_list.append(i)
            elif i[0:3] == '399' and i[7:9] == 'SZ':
                index_list.append(i)
            elif (i[0:3] == '150' or i[0:3] == '159' or i[0:3] == '160' or i[0:3] == '161' or i[0:3] == '162' or i[0:3] == '163' or i[0:3] == '164' or
                    i[0:3] == '165' or i[0:3] == '166' or i[0:3] == '167' or i[0:3] == '168' or i[0:3] == '169' or i[0:3] == '184') and i[7:9] == 'SZ':
                fund_list.append(i)
            elif (i[0:3] == '501' or i[0:3] == '502' or i[0:3] == '505' or i[0:3] == '510' or i[0:3] == '511' or i[0:3] == '512' or i[0:3] == '513' or i[0:3] == '518') and i[7:9] == 'SH':
                fund_list.append(i)
        stock_list = ','.join(stock_list)   # 转化为字符串，应用到接口
        index_list = ','.join(index_list)
        fund_list = ','.join(fund_list)
        terminal = []   # 暂存3个dframe
        terminal1 = []  # 存放不为空的dframe
        if stock_list != '':
            for i in date_list:
                DF1 = pro.daily(ts_code=stock_list, start_date=i, end_date=i)
                dframe1 = pd.concat([dframe1,DF1], ignore_index=True)
            terminal.append(dframe1)
        if index_list != '':
            for i in date_list:
                DF2 = pro.index_daily(ts_code=index_list, start_date=i, end_date=i)
                dframe2 = pd.concat([dframe2, DF2], ignore_index=True)
            terminal.append(dframe2)
        if fund_list != '':
            for i in date_list:
                DF3 = pro.fund_daily(ts_code=fund_list, start_date=i, end_date=i)
                dframe3 = pd.concat([dframe3, DF3], ignore_index=True)
            terminal.append(dframe3)
        for i in terminal:
            if not i.empty:
                terminal1.append(i)
        if len(terminal1) == 1:
            dframe = terminal1[0]
        elif len(terminal1) == 2:
            dframe = pd.merge(terminal1[0], terminal1[1], how='outer')
        elif len(terminal1) == 3:
            dframe = pd.merge(terminal1[0], terminal1[1], how='outer')
            dframe = pd.merge(dframe, terminal1[2], how='outer')
        # 判断dframe是否为空
        if dframe.empty:
            Log.log("%shistory函数获得空数据\n", context.dt)
            exceptional_handle("history函数获得空数据")

        dframe['trade_date'] = dframe['trade_date'].astype('datetime64[ns]')  # 格式化时间
        dframe.index = dframe['ts_code'].values    # 以时间为索引
        dframe = dframe.sort_values('trade_date')  # 时间从久到近排序
        dframe = dframe[fields]  # 此时dframe是一个series对象
        dict = {}
        for index, values in dframe.items():
            if index not in dict:
                dict.setdefault(index, []).append(values)
            else:
                dict[index].append(values)
        return dict

    else:
        Log.log("%shistory函数isdf参数输入不正确\n", context.dt)
        exceptional_handle("history函数isdf参数输入不正确")

# 获取历史数据，可查询单个标的多个数据字段 *
def attribute_history(count, security=None, unit='1d',fields=['open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg', 'vol', 'amount'],isdf=True):
    # count参数检验
    if type(count) != int or count == None or count <= 0:
        Log.log("%sattribute_history函数输入返回的目标行数参数不正确\n", context.dt)
        exceptional_handle("attribute_history函数输入返回的目标行数参数不正确")

    # security参数检验
    if security == None:
        if len(context.universe) != 1:
            Log.log("%sattribute_history函数未指定证券代码，故在证券池寻找，但证券池数量不为1，函数要求单个标\n", context.dt)
            exceptional_handle("attribute_history函数未指定证券代码，故在证券池寻找，但证券池数量不为1，函数要求单个标")
        security = ''.join(context.universe)
    elif type(security) == type([]):
        if len(security) != 1:
            Log.log("%sattribute_history函数输入的证券代码个数只能为一\n", context.dt)
            exceptional_handle("attribute_history函数输入的证券代码个数只能为一")
        security = ''.join(security)  # 将股票列表转换为字符串
    elif type(security) == type(''):
        if len(security) != 9:
            Log.log("%sattribute_history函数证券长度字符不正确\n", context.dt)
            exceptional_handle("attribute_history函数证券长度字符不正确")

    # fields参数检验
    if not (
            fields != 'open' or fields != 'high' or fields != 'low' or fields != 'close' or fields != 'pre_close' or fields != 'change' or fields != 'pct_chg' or fields != 'vol' or fields != 'vol'):
        Log.log("%sattribute_history函数输入的证券属性参数有误\n", context.dt)
        exceptional_handle("attribute_history函数输入的证券属性参数有误")

    # 计算日期
    # end_date = (context.dt).strftime('%Y-%m-%d')  # end_date为今天,这里的日期格式与trade_cal的格式对应
    end_date = datetime.datetime.strptime(context.dt, '%Y-%m-%d').strftime('%Y-%m-%d')
    if unit[1] == 'd':  # 回溯时以天数为单位
        date_list = []
        date_range = trade_cal[(trade_cal['cal_date'] <= end_date)]
        for index, row in date_range.iterrows():  # 遍历date_range这个Dateframe对象
            if count == 0:
                break
            if row['is_open'] == 1:
                date_list.append(datetime.datetime.strptime(row['cal_date'], '%Y-%m-%d').strftime('%Y%m%d'))
                count -= 1
    elif unit[1] == 'w':  # 回溯时以周为单位，将索引到的时间数据放入一个列表中
        date_list = []
        for i in range(count):
            judge_date = trade_cal[(trade_cal['cal_date'] <= end_date)][((i * 7) + 1):].iloc[0, :][
                'is_open']  # 获取到时间，而后判断是否为交易日；若不是，则返回前面最近一日的交易日的数据
            if judge_date == 1:
                date_list.append(datetime.datetime.strptime(
                    trade_cal[(trade_cal['cal_date'] <= end_date)][((i * 7) + 1):].iloc[0, :]['cal_date'],
                    '%Y-%m-%d').strftime('%Y%m%d'))
            else:  # 回溯
                date_range = trade_cal[(trade_cal['cal_date'] <= end_date)][((i * 7) + 1)::1]
                for index, row in date_range.iterrows():  # 遍历date_range这个Dateframe对象
                    if row['is_open'] == 1:
                        date_list.append(datetime.datetime.strptime(row['cal_date'], '%Y-%m-%d').strftime('%Y%m%d'))
                        break
    elif unit[1] == 'm':  # 回溯时以月为单位
        date_list = []
        for i in range(count):
            judge_date = trade_cal[(trade_cal['cal_date'] <= end_date)][((i * 30) + 1):].iloc[0, :][
                'is_open']  # 获取到时间，而后判断是否为交易日；若不是，则返回前面最近一日的交易日的数据
            if judge_date == 1:
                date_list.append(datetime.datetime.strptime(
                    trade_cal[(trade_cal['cal_date'] <= end_date)][((i * 30) + 1):].iloc[0, :]['cal_date'],
                    '%Y-%m-%d').strftime('%Y%m%d'))
            else:  # 回溯,找到离该日期最近一天的交易日
                date_range = trade_cal[(trade_cal['cal_date'] <= end_date)][((i * 30) + 1)::1]
                for index, row in date_range.iterrows():  # 遍历date_range这个Dateframe对象
                    if row['is_open'] == 1:
                        date_list.append(datetime.datetime.strptime(row['cal_date'], '%Y-%m-%d').strftime('%Y%m%d'))
                        break
    else:
        Log.log("%sattribute_history函数单位时间长度设置有误\n", context.dt)
        exceptional_handle("attribute_history函数单位时间长度设置有误")

    # 返回的为DateFrame类型
    if isdf == True:
        dframe = pd.DataFrame()  # 添加得到的每个交易日数据信息  columns='ts_code','trade_date','open','high','low  close','pre_close','change','pct_chg','vol','amount'
        i = security
        stock = ''
        index = ''
        fund = ''
        if (i[0:3] == '600' or i[0:3] == '601' or i[0:3] == '603' or i[0:3] == '605' or i[0:3] == '900' or i[0:3] == '688') and i[7:9]=='SH':
            stock=i
        elif (i[0:3] == '000' or i[0:3] == '002' or i[0:3] == '300') and i[7:9] == 'SZ':  # 深市股票
            stock=i
        elif i[0:3] == '000' and i[7:9] == 'SH':
            index=i
        elif i[0:3] == '399' and i[7:9] == 'SZ':
            index=i
        elif (i[0:3] == '150' or i[0:3] == '159' or i[0:3] == '160' or i[0:3] == '161' or i[0:3] == '162' or i[0:3] == '163' or i[0:3] == '164' or i[0:3] == '165' or i[0:3] == '167' or i[0:3] == '168' or i[ 0:3] == '184') and i[7:9] == 'SZ':
            fund=i
        elif (i[0:3] == '501' or i[0:3] == '502' or i[0:3] == '505' or i[0:3] == '510' or i[0:3] == '511' or i[0:3] == '512' or i[0:3] == '513' or i[0:3] == '518') and i[7:9] == 'SH':
            fund=i
        if stock != '':
            for i in date_list:
                DF = pro.daily(ts_code=stock, start_date=i, end_date=i)
                dframe = pd.concat([dframe, DF], ignore_index=True)
        elif index != '':
            for i in date_list:
                DF =  pro.index_daily(ts_code=index, start_date=i, end_date=i)
                dframe = pd.concat([dframe, DF], ignore_index=True)
        elif fund != '':
            for i in date_list:
                DF = pro.fund_daily(ts_code=fund, start_date=i, end_date=i)
                dframe = pd.concat([dframe, DF], ignore_index=True)
        # 判断dframe是否为空
        if dframe.empty:
            Log.log("%sattribute_history函数获得空数据\n", context.dt)
            exceptional_handle("attribute_history函数获得空数据")

        dframe['trade_date'] = dframe['trade_date'].astype('datetime64[ns]')    # 格式化时间
        dframe.index = dframe['trade_date'].values  # 以时间为索引
        dframe = dframe.sort_values('trade_date')   # 时间从久到近排序
        dframe = dframe[fields]
        return dframe

    # 返回的为dict类型
    elif isdf == False:
        dframe = pd.DataFrame()  # 添加得到的每个交易日数据信息  columns='ts_code','trade_date','open','high','low  close','pre_close','change','pct_chg','vol','amount'
        i = security
        stock = ''
        index = ''
        fund = ''
        if (i[0:3] == '600' or i[0:3] == '601' or i[0:3] == '603' or i[0:3] == '605' or i[0:3] == '900' or i[0:3] == '688') and i[7:9] == 'SH':
            stock = i
        elif (i[0:3] == '000' or i[0:3] == '002' or i[0:3] == '300') and i[7:9] == 'SZ':  # 深市股票
            stock = i
        elif i[0:3] == '000' and i[7:9] == 'SH':
            index = i
        elif i[0:3] == '399' and i[7:9] == 'SZ':
            index = i
        elif (i[0:3] == '150' or i[0:3] == '159' or i[0:3] == '160' or i[0:3] == '161' or i[0:3] == '162' or i[0:3] == '163' or i[0:3] == '164'
              or i[0:3] == '165' or i[0:3] == '167' or i[0:3] == '168' or i[0:3] == '184') and i[7:9] == 'SZ':
            fund = i
        elif (i[0:3] == '501' or i[0:3] == '502' or i[0:3] == '505' or i[0:3] == '510' or i[0:3] == '511' or i[0:3] == '512' or i[0:3] == '513'
              or i[0:3] == '518') and i[7:9] == 'SH':
            fund = i
        if stock!='':
            for i in date_list:
                DF = pro.daily(ts_code=stock, start_date=i, end_date=i)
                dframe = pd.concat([dframe, DF], ignore_index=True)
        elif index!='':
            for i in date_list:
                DF =  pro.index_daily(ts_code=index, start_date=i, end_date=i)
                dframe = pd.concat([dframe, DF], ignore_index=True)
        elif fund!='':
            for i in date_list:
                DF = pro.fund_daily(ts_code=fund, start_date=i, end_date=i)
                dframe = pd.concat([dframe, DF], ignore_index=True)
        # 判断dframe是否为空
        if dframe.empty:
            Log.log("%sattribute_history函数获得空数据\n", context.dt)
            exceptional_handle("attribute_history函数获得空数据")

        dframe['trade_date'] = dframe['trade_date'].astype('datetime64[ns]')    # 格式化时间
        dframe.index = dframe['trade_date'].values  # 以时间为索引
        dframe = dframe.sort_values('trade_date')  # 时间从久到近排序
        dframe = dframe[fields]  # Dateframe对象
        dict = dframe.to_dict('list')

        return dict

    else:
        Log.log("%sattribute_history函数isdf参数输入不正确\n", context.dt)
        exceptional_handle("attribute_history函数isdf参数输入不正确")

# 每日子指标
def daily_info(date = str(context.dt), field = None, sort = None):
    try:  # 判断输入的日期格式是否为'%Y-%m-%d'
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("开始日期输入有误,日期格式应改为‘%Y-%m-%d’")
    date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')

    if field is not None and type(field) != type(""):
        Log.log("%sdaily_info函数参数field必须是单个字段的字符串形式\n", context.dt)
        exceptional_handle("daily_info函数参数field必须是单个字段的字符串形式")

    if sort is not None and sort != "descend" and sort != "ascend":
        Log.log("%sdaily_info函数参数sort必须是ascend或descend两者之一\n", context.dt)
        exceptional_handle("daily_info函数参数sort必须是ascend或descend两者之一")

    df = pro.daily_basic(trade_date=date)
    df.index = df['ts_code'].values

    if (field is None and sort is not None) or (field is not None and sort is None):
        Log.log("%sdaily_info函数参数sort和field必须都有传参或都不传\n", context.dt)
        exceptional_handle("daily_info函数参数sort和field必须都有传参或都不传")

    if field is not None and sort is not None:
        flag = None
        if sort == "ascend":
            flag = True
        else:
            flag = False
        df.sort_values(by=field, inplace=True, ascending=flag)

    return df