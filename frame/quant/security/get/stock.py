"""
股票数据
"""
from quant.security.check_fun import *
from quant.classes.exception import *

get_sbasic_status_list = ['L','D','P']   # 上市状态列表 L上市 D退市 P暂停上市，默认是L
get_sbasic_exchange_list = ['SSE','SZSE','BSE']  #交易所列表 SSE上交所 SZSE深交所 BSE北交所
get_sbasic_is_hs_list = ['N','H','S']    # 是否沪深港通标列表 N否 H沪股通 S深股通
get_sbasic_range_list = ['ts_code', 'symbol', 'name', 'area', 'industry', 'fullname', 'enname', 'cnspell', 'market',
              'exchange', 'curr_type', 'list_status', 'list_date', 'delist_date', 'is_hs']
namechange_range_list = ['ts_code', 'name', 'start_date', 'end_date', 'ann_date', 'change_reason']
hs_const_hs_types = ['SH', 'SZ']
stock_company_exchange_list = ['SSE', 'SZSE']
stock_company_range_list = ['ts_code', 'chairman', 'manager', 'secretary', 'reg_capital', 'setup_date', 'province', 'city',
              'introduction', 'website', 'email', 'office', 'employees', 'main_business', 'business_scope']
hsgt_top10_types = ['1', '3']  # 市场类型 1：沪市 3：深市
hsgt_top10_range_list = ['trade_date', 'ts_code', 'name', 'close', 'change', 'rank', 'market_type', 'amount', 'net_amount', 'buy', 'sell']
ggt_top10_types = ['2', '4']  # 市场类型 2：港股通（沪） 4：港股通（深）
ggt_top10_range_list = ['trade_date', 'ts_code', 'name', 'close', 'p_change', 'rank', 'market_type', 'amount',
              'net_amount', 'sh_amount', 'sh_net_amount', 'sh_buy', 'sh_sell', 'sz_amount', 'sz_net_amount', 'sz_buy', 'sz_sell']
new_share_range_list = ['ts_code','sub_code','name','ipo_date','issue_date','amount','market_amount','price','pe','limit_amount','funds','ballot']
get_giant_range_list = ['trade_date','ts_code','name','close','pct_change','turnover_rate','amount','l_sell','l_buy','l_amount',
                        'net_amount','net_rate','amount_rate','float_values','reason']
get_locked_range_list = ['ts_code','ann_date','float_date','float_share','float_ratio','holder_name','share_type']
stk_limit_range_list = ['trade_date','ts_code','pre_close','up_limit','down_limit']

# 获取股票基础信息
def get_sbasic(code=None, status='L', exchange=None, is_hs=None, fields=None):
    if status not in get_sbasic_status_list:
        Log.log("%sget_sbasic函数输入的上市状态status有误\n", context.dt)
        exceptional_handle("get_sbasic函数输入的上市状态status有误")

    if exchange is not None:
        if exchange not in get_sbasic_exchange_list:
            Log.log("%sget_sbasic函数输入的交易所exchange有误\n", context.dt)
            exceptional_handle("get_sbasic函数输入的交易所exchange有误")

    if code is not None:
        if check_ts_code(code) is False:
            Log.log("%sget_sbasic函数code格式不正确\n", context.dt)
            exceptional_handle("get_sbasic函数code格式不正确")

    if is_hs is not None:
        if is_hs not in get_sbasic_is_hs_list:
            Log.log("%sget_sbasic函数输入的是否沪深港通标is_hs有误\n", context.dt)
            exceptional_handle("get_sbasic函数输入的是否沪深港通标is_hs有误")

    # 判断fields
    if fields is not None:
        if check_fields(fields, get_sbasic_range_list):
            df = pro.stock_basic(exchange=exchange, list_status=status, ts_code=code, is_hs=is_hs)
            df = df[fields]
            return df
        else:
            Log.log("%sget_sbasic函数fields不在范围或格式有误\n", context.dt)
            exceptional_handle("get_sbasic函数fields内容不在范围或格式有误")

    df = pro.stock_basic(exchange=exchange, list_status=status, ts_code=code, is_hs=is_hs)
    return df

# 获取概念股分类
def get_ccpclass():
    return pro.concept()

# 获取概念类的成分股
def get_ccpstocks(id=None):
    # 判断id
    if id is not None:
        if 'TS' not in id:
            Log.log("%sget_ccpstocks函数概念分类ID输入有误\n", context.dt)
            exceptional_handle("get_ccpstocks函数概念分类ID输入有误")
    else:
        Log.log("%sget_ccpstocks函数未输入概念id\n", context.dt)
        exceptional_handle("get_ccpstocks函数未输入概念id")

    df = pro.concept_detail(id=id)
    return df

# 查询某个股票的所属概念
def get_ccpbelong(code=None):
    # 判断股票代码（查询某个股票的概念）
    if code is not None:
        if check_ts_code(code) is False:
            Log.log("%sget_ccpbelong函数code格式不正确\n", context.dt)
            exceptional_handle("get_ccpbelong函数code格式不正确")

    df = pro.concept_detail(ts_code=code)
    return df

# 获取股票曾用名
def namechange(code=None, start_date=None, end_date=None, fields=None):  # fields输入为列表形式
    # 判断stock
    if code == None:
        if len(context.universe) != 0:
            code = context.universe
    if check_ts_code(code) is False:
        Log.log("%snamechange函数code格式不正确\n", context.dt)
        exceptional_handle("namechange函数code格式不正确")

    # 判断公告的开始日期start_date
    if start_date != None:
        try:  # 判断输入的日期格式是否为'%Y-%m-%d'
            datetime.datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("开始日期输入有误,日期格式应改为‘%Y-%m-%d’")
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y%m%d')

    # 判断公告的结束日期end_date
    if end_date != None:
        try:  # 判断输入的日期格式是否为'%Y-%m-%d'
            datetime.datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("开始日期输入有误,日期格式应改为‘%Y-%m-%d’")
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y%m%d')

    if start_date != None and end_date != None:
        if start_date < end_date:
            Log.log("%snamechange公告截止日期在开始日期之前,输入有误\n", context.dt)
            exceptional_handle("namechange公告截止日期在开始日期之前,输入有误")

    # 判断fields
    if fields != None:
        if check_fields(fields,namechange_range_list):
            df = pro.namechange(ts_code=code, start_date=start_date, end_date=end_date)
            df = df[fields]
            return df
        else:
            Log.log("%snamechange函数fields不在范围或格式有误\n", context.dt)
            exceptional_handle("namechange函数fields内容不在范围或格式有误")

    df = pro.namechange(ts_code=code, start_date=start_date, end_date=end_date)
    return df

# 沪深股通成分股
def hs_const(hs_type=None):
    if hs_type == None:
        Log.log("%shs_const函数参数hs_const不能空\n", context.dt)
        exceptional_handle("hs_const函数参数hs_const不能空")

    if hs_type not in hs_const_hs_types:
        Log.log("%shs_const函数输入的查询字符串有误\n", context.dt)
        exceptional_handle("hs_const函数输入的查询字符串有误")

    df = pro.hs_const(hs_type=hs_type)
    list_ = df['ts_code'].tolist()
    return list_

# 上市公司基本信息
def stock_company(exchange=None, fields=None):  # exchange为交易所代码
    if exchange not in stock_company_exchange_list:
        Log.log("%sstock_company函数输入的交易代码有误\n", context.dt)
        exceptional_handle("stock_company函数输入的交易代码有误")

    # 判断fields 格式为列表
    if fields is not None:
        if check_fields(fields, stock_company_range_list):
            df = pro.stock_company(exchange=exchange)
            df = df[fields].sort_values(by='ts_code')  # 注:如果fields中没有ts_code则排序会出错
            return df
        else:
            Log.log("%sstock_company函数fields不在范围或格式有误\n", context.dt)
            exceptional_handle("stock_company函数fields内容不在范围或格式有误")

    df = pro.stock_company(exchange=exchange).sort_values(by='ts_code')
    return df

# 沪深股通十大成交股
# 获取沪股通、深股通每日前十大成交详细数据 1.查询某个交易日
def hsgt_top10(date=None, count=1, market_type=None, fields=None):
    # market_type检验
    if market_type not in hsgt_top10_types and market_type != None:
        Log.log("%shsgt_top10函数输入的市场类型格式有误或不在范围内\n", context.dt)
        exceptional_handle("hsgt_top10函数输入的市场类型格式有误或不在范围内")

    # date参数校验
    if date is not None:
        try:  # 判断输入的日期格式是否为'%Y-%m-%d'
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("开始日期输入有误,日期格式应改为‘%Y-%m-%d’")
    else:
        date = context.dt
        date = str(date)

    # fields检验
    if fields is not None:
        if not check_fields(fields, hsgt_top10_range_list):
            Log.log("%shsgt_top10函数fields不在范围或格式有误\n", context.dt)
            exceptional_handle("hsgt_top10函数fields内容不在范围或格式有误")

    # 根据count推时间
    dframe = pd.DataFrame()
    date_list = []
    date_range = trade_cal[(trade_cal['cal_date'] <= date)][::-1]
    for index, row in date_range.iterrows():  # 遍历date_range这个Dateframe对象
        if count == 0:
            break
        if row['is_open'] == 1:
            date_list.append(datetime.datetime.strptime(row['cal_date'], '%Y-%m-%d').strftime('%Y%m%d'))
            count -= 1
    for i in date_list:
        df = pro.hsgt_top10(trade_date=i, market_type=market_type)
        dframe = pd.concat([dframe, df], ignore_index=True)

    if fields is not None:
        return dframe[fields]
    else:
        return dframe

# 港股通十大成交股
def ggt_top10(date=None, count=1, market_type=None, fields=None):
    # 判断market_type
    if market_type not in ggt_top10_types and market_type != None:
        Log.log("%sggt_top10函数输入的市场类型格式market_type有误或不在范围内\n", context.dt)
        exceptional_handle("ggt_top10函数输入的市场类型格式market_type有误或不在范围内")

    # date参数校验
    if date is not None:
        try:  # 判断输入的日期格式是否为'%Y-%m-%d'
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("开始日期输入有误,日期格式应改为‘%Y-%m-%d’")
    else:
        date = context.dt
        date = str(date)

    # fields检验
    if fields is not None:
        if not check_fields(fields, ggt_top10_range_list):
            Log.log("%sggt_top10函数fields不在范围或格式有误\n", context.dt)
            exceptional_handle("ggt_top10函数fields内容不在范围或格式有误")

    # 根据count推时间
    dframe = pd.DataFrame()
    date_list = []
    date_range = trade_cal[(trade_cal['cal_date'] <= date)][::-1]
    for index, row in date_range.iterrows():  # 遍历date_range这个Dateframe对象
        if count == 0:
            break
        if row['is_open'] == 1:
            date_list.append(datetime.datetime.strptime(row['cal_date'], '%Y-%m-%d').strftime('%Y%m%d'))
            count -= 1
    for i in date_list:
        df = pro.ggt_top10(trade_date=i, market_type=market_type)
        dframe = pd.concat([dframe, df], ignore_index=True)

    if fields is not None:
        return dframe[fields]
    else:
        return dframe

# IPO新股列表
# 传入一个开始日期date1和结束日期date2
def new_share(date1=None, date2=None, fields=None):  # 传入一个开始日期date1和开始日期date2
    try:  # 判断输入的日期格式是否为'%Y-%m-%d'
        datetime.datetime.strptime(date1, '%Y-%m-%d')
        datetime.datetime.strptime(date2, '%Y-%m-%d')
    except ValueError:
        raise ValueError("开始日期输入有误,日期格式应改为‘%Y-%m-%d’")
    date1 = datetime.datetime.strptime(date1, '%Y-%m-%d').strftime('%Y%m%d')
    date2 = datetime.datetime.strptime(date2, '%Y-%m-%d').strftime('%Y%m%d')

    if fields is not None:
        if check_fields(fields, new_share_range_list):
            df = pro.new_share(start_date=date1, end_date=date2)
            df = df[fields]
            return df
        else:
            Log.log("%snew_share函数fields不在范围或格式有误\n", context.dt)
            exceptional_handle("new_share函数fields内容不在范围或格式有误")

    df = pro.new_share(start_date=date1, end_date=date2)
    return df

"""
结束日期end_date若未指定，默认当天时间
count默认为1
security参数只接受一个股票代码，若未指定，则去股票池寻找，若股票池股票代码数量不为1，则报错
"""
# 获取龙虎榜数据
def get_giant(code=None, date=None, count=1, fields=None):
    # count参数校验
    if type(count) != int or count <= 0:
        Log.log("%sget_giant函数输入的返回的目标行数数据格式有误\n", context.dt)
        exceptional_handle("get_giant函数输入的返回的目标行数数据格式有误")

    # stock参数校验
    if type(code) == type([]):
        if len(code) != 1:
            Log.log("%sget_giant函数输入的股票代码个数只能为一\n", context.dt)
            exceptional_handle("get_giant函数输入的股票代码个数只能为一")
        code = ''.join(code)
    elif type(code) == type(''):
        if len(code) != 9:
            Log.log("%sget_giant函数股票长度字符不正确\n", context.dt)
            exceptional_handle("get_giant函数股票长度字符不正确")
    elif code == None:
        pass
    else:
        Log.log("%sget_giant函数股票代码输入类型有误\n", context.dt)
        exceptional_handle("get_giant函数股票代码输入类型有误")

    # date参数校验
    if date is not None:
        try:  # 判断输入的日期格式是否为'%Y-%m-%d'
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("开始日期输入有误,日期格式应改为‘%Y-%m-%d’")
    else:
        date = context.dt
        date = str(date)

    # fields参数检验
    if fields is not None:
        if not check_fields(fields, get_giant_range_list):
            Log.log("%sget_giant函数fields不在范围或格式有误\n", context.dt)
            exceptional_handle("get_giant函数fields内容不在范围或格式有误")

    dframe = pd.DataFrame()
    date_list = []
    date_range = trade_cal[(trade_cal['cal_date'] <= date)][::-1]
    for index, row in date_range.iterrows():  # 遍历date_range这个Dateframe对象
        if count == 0:
            break
        if row['is_open'] == 1:
            date_list.append(datetime.datetime.strptime(row['cal_date'], '%Y-%m-%d').strftime('%Y%m%d'))
            count -= 1
    for i in date_list:
        df = pro.top_list(trade_date=i, ts_code=code)
        dframe = pd.concat([dframe,df], ignore_index=True)

    if fields is not None:
        return dframe[fields]
    else:
        return dframe

# 获取指定日期区间内的限售解禁数据
def get_locked(code=None, float_date=None, start_date=None, end_date=None, count=None, fields=None):  # stock为股票list
    # stock参数校验
    if type(code) == type([]):
        if len(code) != 1:
            Log.log("%sget_locked函数输入的股票代码个数只能为一\n", context.dt)
            exceptional_handle("get_locked函数输入的股票代码个数只能为一")
        code = ''.join(code)
    elif type(code) == type(''):
        if len(code) != 9:
            Log.log("%sget_locked函数股票长度字符不正确\n", context.dt)
            exceptional_handle("get_locked函数股票长度字符不正确")
    elif code == None:
        pass
    else:
        Log.log("%sget_locked函数股票代码输入类型有误\n", context.dt)
        exceptional_handle("get_locked函数股票代码输入类型有误")

    # float_date检验
    if float_date is not None:
        try:  # 判断输入的日期格式是否为'%Y-%m-%d'
            datetime.datetime.strptime(float_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("公告日期输入错误,日期格式应改为‘%Y-%m-%d’")
        float_date = datetime.datetime.strptime(float_date, '%Y-%m-%d').strftime('%Y%m%d')

    # start_date判断
    if start_date is not None:
        try:  # 判断输入的日期格式是否为'%Y-%m-%d'
            datetime.datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("开始日期输入有误,日期格式应改为‘%Y-%m-%d’")

        # 四种情况
        if end_date is not None and count == None:
            try:  # 判断输入的日期格式是否为'%Y-%m-%d'
                datetime.datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                raise ValueError("错误的输入,日期格式应改为‘%Y-%m-%d’")
            if end_date < start_date:
                Log.log("%sget_locked函数截至日期在开始日期之前，输入有误\n", context.dt)
                exceptional_handle("get_locked函数截至日期在开始日期之前，输入有误")
        elif end_date is not None and count is not None:
            date_range = trade_cal[(trade_cal['cal_date'] <= end_date)][::-1]
            for index, row in date_range.iterrows():  # 遍历date_range这个Dateframe对象
                if count == 0:
                    break
                if row['is_open'] == 1:
                    count -= 1
                    start_date = row['cal_date']
        elif end_date == None and count is not None:
            end_date = start_date
            date_range = trade_cal[(trade_cal['cal_date'] >= end_date)]
            for index, row in date_range.iterrows():  # 遍历date_range这个Dateframe对象
                if count == 0:
                    break
                if row['is_open'] == 1:
                    count -= 1
                    end_date = row['cal_date']

        elif end_date == None and count == None:
            end_date = context.dt
            end_date = end_date.strftime('%Y%m%d')
            if end_date < start_date:
                Log.log("%sget_locked函数截至日期在开始日期之前，输入有误\n", context.dt)
                exceptional_handle("get_locked函数截至日期在开始日期之前，输入有误")
    else:
        if end_date is not None and count is not None:
            date_range = trade_cal[(trade_cal['cal_date'] <= end_date)][::-1]
            for index, row in date_range.iterrows():  # 遍历date_range这个Dateframe对象
                if count == 0:
                    break
                if row['is_open'] == 1:
                    count -= 1
                    start_date = row['cal_date']
        elif end_date is not None and count == None:
            start_date = end_date

    if start_date is not None:
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y%m%d')
    if end_date is not None:
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y%m%d')

    # 判断fields
    if fields is not None:
        if check_fields(fields, get_locked_range_list):
            df = pro.share_float(ts_code=code, float_date=float_date, start_date=start_date, end_date=end_date)
            df = df[fields]
            return df
        else:
            Log.log("%sget_locked函数fields不在范围或格式有误\n", context.dt)
            exceptional_handle("get_locked函数fields内容不在范围或格式有误")

    df = pro.share_float(ts_code=code, float_date=float_date, start_date=start_date, end_date=end_date)
    return df

# 每日涨跌停价格
"""
 1.获取单日涨跌停价格 - 输入交易日 或加count获取前几日的价格
 2.获取范围涨跌停价格 起始日期和截止日期可选
 两种查询不能同时进行
"""
def stk_limit(code=None, trade_date=None, count=1, start_date=None, end_date=None, fields=None):

    if code is not None and not check_ts_code(code):
        Log.log("%sstk_limit函数参数code格式不正确\n", context.dt)
        exceptional_handle("stk_limit函数参数code格式不正确")

    # fields参数检验
    if fields is not None:
        if not check_fields(fields, stk_limit_range_list):
            Log.log("%sstk_limit函数fields不在范围或格式有误\n", context.dt)
            exceptional_handle("stk_limit函数fields内容不在范围或格式有误")

    # trade_date和(start_date&end_date)两种时间参数至少输入一种组合
    if trade_date is not None:
        if start_date or end_date is not None:
            Log.log("%sstk_limit函数输入了trade_date参数就不要输入start_date和end_date参数\n", context.dt)
            exceptional_handle("stk_limit函数输入了trade_date参数就不要输入start_date和end_date参数")

        try:  # 判断输入的日期格式是否为'%Y-%m-%d'
            datetime.datetime.strptime(trade_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("开始日期输入有误,日期格式应改为‘%Y-%m-%d’")

        dframe = pd.DataFrame()
        date_list = []
        date_range = trade_cal[(trade_cal['cal_date'] <= trade_date)][::-1]
        for index, row in date_range.iterrows():  # 遍历date_range这个Dateframe对象
            if count == 0:
                break
            if row['is_open'] == 1:
                date_list.append(datetime.datetime.strptime(row['cal_date'], '%Y-%m-%d').strftime('%Y%m%d'))
                count -= 1
        for i in date_list:
            df = pro.stk_limit(trade_date=i, ts_code=code)
            dframe = pd.concat([dframe, df], ignore_index=True)

        if fields is not None:
            return dframe[fields]
        else:
            return dframe
    else:
        if start_date is None or end_date is None:
            Log.log("%sstk_limit函数必须输入时间参数\n", context.dt)
            exceptional_handle("stk_limit函数必须输入时间参数")

        try:  # 判断输入的日期格式是否为'%Y-%m-%d'
            datetime.datetime.strptime(start_date, '%Y-%m-%d')
            datetime.datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("开始日期输入有误,日期格式应改为‘%Y-%m-%d’")
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y%m%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y%m%d')

    df = pro.stk_limit(ts_code=code, start_date=start_date, end_date=end_date)

    if fields is not None:
        return df[fields]
    else:
        return df


# 每日涨跌停统计
"""
 1.获取某日统计数据（涨跌停）-输入交易日
 2.获取某日涨或跌停股票-输入交易日和涨跌停类型：U涨停D跌停
 3.获取某时间段统计信息-输入起始时间和截止时间(可选：涨跌停类型)
 4.获取某支股票在某时间段的统计信息-输入股票或股票列表、起始时间、截止时间(可选：涨跌停类型)
 补充说明：第4点尝试传入列表（多支股票）无法获取
"""
"""
def limit_list(trade_date=None,ts_code=None,limit_type=None,start_date=None,end_date=None,fields=None):
    limit_types = ['U', 'D']
    range_ = ['trade_date', 'ts_code', 'name', 'close',
             'pct_chg', 'amp', 'fc_ratio', 'fl_ratio',
             'fd_amount', 'first_time', 'last_time',
             'open_times', 'strth', 'limit']
    # 1.
    if trade_date is not None:  # 传入交易日进行查询 不能输入股票代码 开始和截止日期
        try:  # 判断输入的日期格式是否为'%Y-%m-%d'
            datetime.datetime.strptime(trade_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("开始日期输入有误,日期格式应改为‘%Y-%m-%d’")
        trade_date = datetime.datetime.strptime(trade_date, '%Y-%m-%d').strftime('%Y%m%d')
        if check_date(trade_date) is False:
            return
        if ts_code or start_date or end_date is not None:
            print('输入了其他无关变量')
            return
        else:
            # 判断fields 格式为列表
            if fields is not None:
                if check_fields(fields,range_):
                    # 2.
                    if limit_type is not None:
                        if limit_type in limit_types:
                            df = pro.limit_list(trade_date=trade_date,limit_type=limit_type)
                            df = df[fields]
                            return df
                        else:
                            print('输入的limit_type有误')
                            return
                    else:
                        df = pro.limit_list(trade_date=trade_date)
                        return df
                else:
                    return
            else:
                if limit_type is not None:
                    if limit_type in limit_types:
                        df = pro.limit_list(trade_date=trade_date, limit_type=limit_type)
                        return df
                    else:
                        print('输入的limit_type有误')
                        return
                else:
                    df = pro.limit_list(trade_date=trade_date)
                    return df
    # 3.
    if start_date and end_date is not None:
        try:  # 判断输入的日期格式是否为'%Y-%m-%d'
            datetime.datetime.strptime(start_date, '%Y-%m-%d')
            datetime.datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("开始日期输入有误,日期格式应改为‘%Y-%m-%d’")
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y%m%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y%m%d')
        if check_date(start_date) and check_date(end_date):
            if limit_type is not None:
                if limit_type not in limit_types:
                    print('输入的limit_type有误')
                    return
            # 4.
            if ts_code is not None:
                if fields is not None:
                    if check_fields(fields,range_):
                        df = pro.limit_list(ts_code=ts_code, start_date=start_date, end_date=end_date, limit_type=limit_type)
                        df = df[fields]
                        return df
                    else:
                        return
                df = pro.limit_list(ts_code=ts_code,start_date=start_date,end_date=end_date,limit_type=limit_type)
                return df
            else:
                if fields is not None:
                    if check_fields(fields,range_):
                        df = pro.limit_list(start_date=start_date,end_date=end_date,limit_type=limit_type)
                        df = df[fields]
                        return df
                    else:
                        print('fields参数的格式输入有误')
                        return
                df = pro.limit_list(start_date=start_date,end_date=end_date,limit_type=limit_type)
                return df

    print('未传入参数或传入的参数不完整')
    return
"""