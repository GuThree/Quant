"""
数据获取函数
"""

from quant.classes.object import *


ts.set_token('9e22c84922d0c39ef78ae4c9562c00dfa79775795f022c03e1432455')
pro = ts.pro_api()

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

#获取历史数据，可查询多个标的单个数据字段
def history(count,unit='1d',fields='close',security_list=None, isdf=True):  #这里的fields只能取一个值！且为元组类型，最后面要加一个逗号；输入的股票代码为字符串类型，例如'000001.SZ,600000.SH'
    #count参数检验
    if type(count)!=int or count==None or count<=0:
        print('未输入返回的目标行数')
        return
    #fields参数检验
    if not(fields!='open' or fields!='high' or fields!='low' or fields!='close' or fields!='pre_close' or fields!='change' or fields!='pct_chg' or fields!='vol' or fields!='amount'):
        print('输入的股票属性参数有误')
        return
    #security_list参数检验
    if type(security_list) == type([]):
        security_list=','.join(security_list)        #这里需要把股票代码转化为字符串形式，因为接口需要的是字符串输入

    elif type(security_list) == type(''):
        if len(security_list) != 9:
            print('股票长度字符不正确')
            return

    elif security_list==None:
        if context.universe!=None:
            security_list=context.universe

        else:
            print('没有设定股票代码')
            return

    end_date = (context.dt).strftime('%Y-%m-%d')  # end_date为今天,这里的日期格式与trade_cal的格式对应
    if unit[1]=='d':  #回溯时以天数为单位
        date_list = []
        date_range = trade_cal[(trade_cal['cal_date'] <= end_date)][::-1]
        for index, row in date_range.iterrows():  # 遍历date_range这个Dateframe对象
            if count==0:
                break
            if row['is_open'] == 1:
                date_list.append(datetime.datetime.strptime(row['cal_date'], '%Y-%m-%d').strftime('%Y%m%d'))
                count-=1
        # return date_list
    elif unit[1]=='w':  #回溯时以周为单位，将索引到的时间数据放入一个列表中
        date_list=[]
        for i in range(count):
            judge_date = trade_cal[(trade_cal['cal_date'] <= end_date)][-((i * 7) + 1):].iloc[0, :]['is_open']   #获取到时间，而后判断是否为交易日；若不是，则返回前面最近一日的交易日的数据
            if judge_date==1:
                date_list.append(datetime.datetime.strptime(trade_cal[(trade_cal['cal_date'] <= end_date)][-((i * 7) + 1):].iloc[0, :]['cal_date'],'%Y-%m-%d').strftime('%Y%m%d'))
            else:  #回溯
                date_range = trade_cal[(trade_cal['cal_date'] <= end_date)][-((i * 7) + 1)::-1]
                for index, row in date_range.iterrows():  # 遍历date_range这个Dateframe对象
                    if row['is_open'] == 1:
                        date_list.append(datetime.datetime.strptime(row['cal_date'], '%Y-%m-%d').strftime('%Y%m%d'))
                        break
        #return date_list
    elif unit[1]=='m':  #回溯时以月为单位
        date_list = []
        for i in range(count):
            judge_date = trade_cal[(trade_cal['cal_date'] <= end_date)][-((i * 30) + 1):].iloc[0, :]['is_open']  # 获取到时间，而后判断是否为交易日；若不是，则返回前面最近一日的交易日的数据
            if judge_date == 1:
                date_list.append(datetime.datetime.strptime(trade_cal[(trade_cal['cal_date'] <= end_date)][-((i * 30) + 1):].iloc[0, :]['cal_date'],'%Y-%m-%d').strftime('%Y%m%d'))
            else:  #往前回溯，找到离该日期最近一天的交易日
                date_range=trade_cal[(trade_cal['cal_date'] <= end_date)][-((i * 30) + 1)::-1]
                for index,row in date_range.iterrows():  #遍历date_range这个Dateframe对象
                    if row['is_open']==1:
                        date_list.append(datetime.datetime.strptime(row['cal_date'],'%Y-%m-%d').strftime('%Y%m%d'))
                        break
        #return date_list
    else:
        print('单位时间长度设置有误')
        return

    if isdf==True:  #返回的为DateFrame类型
        dframe = pd.DataFrame()   #添加得到的每个交易日数据信息  columns='ts_code','trade_date','open','high','low  close','pre_close','change','pct_chg','vol','amount'
        for i in date_list:
            DF = pro.daily(ts_code=security_list, start_date=i, end_date=i)
            dframe=dframe.append(DF, ignore_index = True)
        dframe.index = dframe['trade_date'].values  #以时间为索引
        dframe=dframe[fields]  #此时dframe是一个series对象
        security_list=security_list.split(',')    #股票代码保存在列表中
        new_dframe=pd.DataFrame(columns=security_list)
        for index,value in dframe.items():
            security_code=security_list.pop(0)
            security_list.append(security_code)
            new_dframe.loc[index,security_code]=value
        return new_dframe

    elif isdf==False:  #返回的为dict类型
        dframe = pd.DataFrame()   #添加得到的每个交易日数据信息  columns='ts_code','trade_date','open','high','low  close','pre_close','change','pct_chg','vol','amount'
        for i in date_list:
            DF = pro.daily(ts_code=security_list, start_date=i, end_date=i)
            dframe=dframe.append(DF, ignore_index = True)
        dframe.index = dframe['ts_code'].values  #以时间为索引
        dframe=dframe[fields]  #此时dframe是一个series对象
        dict = {}
        for index, values in dframe.items():
            if index not in dict:
                dict.setdefault(index, []).append(values)
            else:
                dict[index].append(values)
        return dict

    else:
        print('“df”输入有误')

#获取历史数据，可查询单个标的多个数据字段
def attribute_history(count,security=None, unit='1d',fields=['open','high','low','close','pre_close','change','pct_chg','vol','amount'],isdf=True):
    # count参数检验
    if type(count) != int or count == None or count <= 0:
        print('未输入返回的目标行数')
        return
    # security参数检验
    if type(security) == type([]):
        if len(security) != 1:
            print('输入的股票代码个数只能为一')
            return
        security=''.join(security)   #将股票列表转换为字符串

    elif type(security) == type(''):
        if len(security) != 9:
            print('股票长度字符不正确')
            return

    elif security==None:
        if context.universe!=None:
            if len(context.universe) != 1:
                print('未指定股票代码，故在股票池寻找股票代码，但股票池代码数量不为1，函数要求单个标')
                return
            security=''.join(context.universe)
        else:
            print('没有设定股票代码')
            return

    # fields参数检验
    if not (
            fields != 'open' or fields != 'high' or fields != 'low' or fields != 'close' or fields != 'pre_close' or fields != 'change' or fields != 'pct_chg' or fields != 'vol' or fields != 'vol'):
        print('输入的股票属性参数有误')
        return

    end_date = (context.dt).strftime('%Y-%m-%d')  # end_date为今天,这里的日期格式与trade_cal的格式对应
    if unit[1] == 'd':  # 回溯时以天数为单位
        date_list = []
        date_range = trade_cal[(trade_cal['cal_date'] <= end_date)][::-1]
        for index, row in date_range.iterrows():  # 遍历date_range这个Dateframe对象
            if count == 0:
                break
            if row['is_open'] == 1:
                date_list.append(datetime.datetime.strptime(row['cal_date'], '%Y-%m-%d').strftime('%Y%m%d'))
                count -= 1
    elif unit[1] == 'w':  # 回溯时以周为单位，将索引到的时间数据放入一个列表中
        date_list = []
        for i in range(count):
            judge_date = trade_cal[(trade_cal['cal_date'] <= end_date)][-((i * 7) + 1):].iloc[0, :]['is_open']  # 获取到时间，而后判断是否为交易日；若不是，则返回前面最近一日的交易日的数据
            if judge_date == 1:
                date_list.append(datetime.datetime.strptime(
                    trade_cal[(trade_cal['cal_date'] <= end_date)][-((i * 7) + 1):].iloc[0, :]['cal_date'],'%Y-%m-%d').strftime('%Y%m%d'))
            else:  # 回溯
                date_range = trade_cal[(trade_cal['cal_date'] <= end_date)][-((i * 7) + 1)::-1]
                for index, row in date_range.iterrows():  # 遍历date_range这个Dateframe对象
                    if row['is_open'] == 1:
                        date_list.append(datetime.datetime.strptime(row['cal_date'], '%Y-%m-%d').strftime('%Y%m%d'))
                        break
    elif unit[1] == 'm':  # 回溯时以月为单位
        date_list = []
        for i in range(count):
            judge_date = trade_cal[(trade_cal['cal_date'] <= end_date)][-((i * 30) + 1):].iloc[0, :]['is_open']  # 获取到时间，而后判断是否为交易日；若不是，则返回前面最近一日的交易日的数据
            if judge_date == 1:
                date_list.append(datetime.datetime.strptime(
                    trade_cal[(trade_cal['cal_date'] <= end_date)][-((i * 30) + 1):].iloc[0, :]['cal_date'],'%Y-%m-%d').strftime('%Y%m%d'))
            else:  # 回溯,找到离该日期最近一天的交易日
                date_range = trade_cal[(trade_cal['cal_date'] <= end_date)][-((i * 30) + 1)::-1]
                for index, row in date_range.iterrows():  # 遍历date_range这个Dateframe对象
                    if row['is_open'] == 1:
                        date_list.append(datetime.datetime.strptime(row['cal_date'], '%Y-%m-%d').strftime('%Y%m%d'))
                        break
    else:
        print('单位时间长度设置有误')
        return

    if isdf == True:  # 返回的为DateFrame类型
        dframe = pd.DataFrame()  # 添加得到的每个交易日数据信息  columns='ts_code','trade_date','open','high','low  close','pre_close','change','pct_chg','vol','amount'
        for i in date_list:
            DF = pro.daily(ts_code=security, start_date=i, end_date=i)
            dframe = dframe.append(DF, ignore_index=True)
        dframe.index = dframe['trade_date'].values  # 以时间为索引
        dframe = dframe[fields]
        return dframe

    elif isdf == False:  # 返回的为dict类型
        dframe = pd.DataFrame()  # 添加得到的每个交易日数据信息  columns='ts_code','trade_date','open','high','low  close','pre_close','change','pct_chg','vol','amount'
        for i in date_list:
            DF = pro.daily(ts_code=security, start_date=i, end_date=i)
            dframe = dframe.append(DF, ignore_index=True)
        dframe.index = dframe['trade_date'].values  # 以时间为索引
        dframe = dframe[fields]  #Dateframe对象
        dict = dframe.to_dict('list')

        # for index, rows in dframe.iterrows():
        #     if index not in dict:
        #         dict.setdefault(index, []).append(values)
        #     else:
        #         dict[index].append(values)
        return dict

    else:
        print('“df”输入有误')

#获取龙虎榜数据
def get_giant_list(count = 1, security=None, end_date=None):
    """
    结束日期end_date若未指定，默认当天时间
    count默认为1
    security参数只接受一个股票代码，若未指定，则去股票池寻找，若股票池股票代码数量不为1，则报错
    """
    # count参数校验
    if type(count) != int or count == None or count <= 0:
        print('未输入返回的目标行数')
        return
    # security参数校验
    if type(security) == type([]):
        if len(security) != 1:
            print('输入的股票代码个数只能为一')
            return
        security = ''.join(security)
    elif type(security) == type(''):
        if len(security) != 9:
            print('股票长度字符不正确')
            return
    elif security == None:
        if context.universe!=None:
            if len(context.universe) != 1:
                print('未指定股票代码，故在股票池寻找股票代码，但股票池代码数量不为1，函数要求单个标')
                return
            security=''.join(context.universe)
        else:
            print('没有设定股票代码')
            return
    else:
        print('股票代码输入类型有误')
        return
    # end_date参数校验
    if end_date == None:
        end_date = context.dt
    else:
        end_date = parse(end_date)

    dframe = pd.DataFrame()
    date_list = []
    end_date = (context.dt).strftime('%Y-%m-%d')
    date_range = trade_cal[(trade_cal['cal_date'] <= end_date)][::-1]
    for index, row in date_range.iterrows():  # 遍历date_range这个Dateframe对象
        if count == 0:
            break
        if row['is_open'] == 1:
            date_list.append(datetime.datetime.strptime(row['cal_date'], '%Y-%m-%d').strftime('%Y%m%d'))
            count -= 1
    for i in date_list:
        df = pro.top_list(trade_date=i, ts_code=security)
        if len(df.index) == 0:
            print(i,'这天表中没有数据，要么不存在这个传入的股票代码，要么这个时间点龙虎榜没这支股票')
        dframe = dframe.append(df, ignore_index=True)
    return dframe





