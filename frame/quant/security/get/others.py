"""
其它非股票指数数据
"""
from quant.security.check_fun import *
from quant.classes.exception import *

get_fundbasic_market_list = ['E', 'O']  # 交易市场: E场内 O场外（默认E）
get_fundbasic_status_list = ['D', 'I', 'L']  # 存续状态 D摘牌 I发行 L上市中
get_fundbasic_range_list = ['trade_date', 'ts_code', 'name', 'close', 'p_change', 'rank', 'market_type', 'amount',
              'net_amount', 'sh_amount', 'sh_net_amount', 'sh_buy', 'sh_sell', 'sz_amount', 'sz_net_amount',
              'sz_buy', 'sz_sell']
get_futbasic_exchange_list = ['CFFEX', 'DCE', 'CZCE', 'SHFE', 'INE']  # 交易所代码 CFFEX-中金所 DCE-大商所 CZCE-郑商所 SHFE-上期所 INE-上海国际能源交易中心
get_futbasic_fut_list = ['1', '2']  # 合约类型 (1 普通合约 2 主力与连续合约 默认取全部)
get_futbasic_range_list = ['ts_code', 'symbol', 'exchange', 'name', 'fut_code', 'multiplier', 'trade_unit', 'per_unit', 'quote_unit',
              'quote_unit_desc', 'd_mode_desc', 'list_date', 'delist_date', 'd_month', 'last_ddate', 'trade_time_desc']
get_optbasic_exchange_list = ['CFFEX', 'DCE', 'CZCE', 'SHFE', 'SSE', 'SZSE'] #交易所代码表
get_optbasic_range_list = ['ts_code', 'exchange', 'name', 'per_unit', 'opt_code', 'opt_type', 'call_put', 'exercise_type', 'exercise_price',
              's_month', 'maturity_date', 'list_price', 'list_date', 'delist_date', 'last_edate', 'last_ddate', 'quote_unit', 'min_price_chg']
get_optbasic_call_put_list = ['P', 'C']  # 期权类型表
get_cbbasic_exchange_list = ['SZ','SH']
get_cbbasic_range_list = ['ts_code', 'bond_full_name', 'bond_short_name', 'cb_code', 'stk_code', 'stk_short_name', 'maturity', 'par', 'issue_price',
              'issue_size', 'remain_size', 'value_date', 'maturity_date', 'rate_type', 'coupon_rate', 'add_rate'',pay_per_year',
              'list_date', 'delist_date', 'exchange', 'conv_start_date', 'conv_end_date', 'first_conv_price', 'conv_price', 'rate_clause',
              'put_clause', 'maturity_put_price', 'call_clause', 'reset_clause', 'conv_clause', 'guarantor', 'guarantee_type', 'issue_rating',
              'newest_rating', 'rating_comp']
get_fxobasic_classify_list = ['FX','INDEX','COMMODITY','METAL','BUND','CRYPTO','FX_BASKET']
get_fxobasic_range_list = ['ts_code', 'exchange', 'name', 'classify', 'min_unit', 'max_unit', 'pip', 'pip_cost',
              'target_spread', 'min_stop_distance', 'trading_hours', 'break_time']
get_hkbasic_status_list = ['L', 'D', 'P']  # 上市状态列表 L上市 D退市 P暂停上市 不输入默认L
get_hkbasic_range_list = ['ts_code', 'name', 'fullname', 'enname', 'cn_spell', 'market', 'list_status',
              'list_date', 'delist_date', 'trade_unit', 'isin', 'curr_type']
get_usbasic_classify_list = ['ADR', 'GDR', 'EQ']  # 股票分类列表
get_usbasic_range_list = ['ts_code', 'name', 'enname', 'classify', 'list_date', 'delist_date']

# 基金列表
# 没有传参则输出全部信息
def get_fundbasic(market=None, status=None, fields=None):
    if market is not None:
        if market not in get_fundbasic_market_list:
            Log.log("%sget_fundbasic函数输入的market值不在范围内\n", context.dt)
            exceptional_handle("get_fundbasic函数输入的market值不在范围内")

    if status is not None:
        if status not in get_fundbasic_status_list:
            Log.log("%sget_fundbasic函数输入的status值不在范围内\n", context.dt)
            exceptional_handle("get_fundbasic函数输入的status值不在范围内")

    if fields is not None:
        if check_fields(fields, get_fundbasic_range_list):
            df = pro.fund_basic(market=market, status=status)
            df = df[fields]
            return df
        else:
            Log.log("%sget_fundbasic函数fields不在范围或格式有误\n", context.dt)
            exceptional_handle("get_fundbasic函数fields内容不在范围或格式有误")

    df = pro.fund_basic(market=market, status=status)
    return df

# 期货合约信息表
def get_futbasic(exchange=None, fut_type=None, fields=None):
    if exchange not in get_futbasic_exchange_list:
        Log.log("%sget_futbasic函数输入的交易所代码exchange不在范围内\n", context.dt)
        exceptional_handle("get_futbasic函数输入的交易所代码exchange不在范围内")

    if fut_type is not None:
        if fut_type not in get_futbasic_fut_list:
            Log.log("%sget_futbasic函数输入的合约类型格式fut_type有误或不在范围内\n", context.dt)
            exceptional_handle("get_futbasic函数输入的合约类型格式fut_type有误或不在范围内")

    # 判断fields 格式为列表
    if fields is not None:
        if check_fields(fields,get_futbasic_range_list):
            df = pro.fut_basic(exchange=exchange, fut_type=fut_type)
            df = df[fields]
            return df
        else:
            Log.log("%sget_futbasic函数fields不在范围或格式有误\n", context.dt)
            exceptional_handle("get_futbasic函数fields内容不在范围或格式有误")

    df = pro.fut_basic(exchange=exchange, fut_type=fut_type)
    return df

# 期权合约信息
def get_optbasic(exchange=None, call_put=None, fields=None):
    if exchange not in get_optbasic_exchange_list:
        Log.log("%sget_optbasic函数输入的交易所代码exchange不在范围内\n", context.dt)
        exceptional_handle("get_optbasic函数输入的交易所代码exchange不在范围内")

    if call_put is not None:
        if call_put not in get_optbasic_call_put_list:
            Log.log("%sget_optbasic函数输入的期权类型call_put不在范围内\n", context.dt)
            exceptional_handle("get_optbasic函数输入的期权类型call_put不在范围内")

    # 判断fields 格式为列表
    if fields is not None:
        if check_fields(fields,get_optbasic_range_list):
            df = pro.opt_basic(exchange=exchange, call_put=call_put)
            df = df[fields]
            return df
        else:
            Log.log("%sget_optbasic函数fields不在范围或格式有误\n", context.dt)
            exceptional_handle("get_optbasic函数fields内容不在范围或格式有误")

    df = pro.opt_basic(exchange=exchange,call_put=call_put)
    return df

# 可转债基本信息
"""
 1.输入单个转债代码查询
 2.输入上市地点查询
 3.查询全部
"""
def get_cbbasic(code=None, exchange=None, fields=None):
    if exchange is not None:
        if exchange not in get_cbbasic_exchange_list:
            Log.log("%sget_cbbasic函数输入的交易地点exchange不在范围内\n", context.dt)
            exceptional_handle("get_cbbasic函数输入的交易地点exchange不在范围内")

    # 判断股票代码
    if code is not None:
        if check_ts_code(code) is False:
            Log.log("%sget_cbbasic函数code格式不正确\n", context.dt)
            exceptional_handle("get_cbbasic函数code格式不正确")

    # 判断fields 格式为列表
    if fields is not None:
        if check_fields(fields,get_cbbasic_range_list):
            df = pro.cb_basic(ts_code=code,exchange=exchange)
            df = df[fields]
            return df
        else:
            Log.log("%sget_cbbasic函数fields不在范围或格式有误\n", context.dt)
            exceptional_handle("get_cbbasic函数fields内容不在范围或格式有误")

    df = pro.cb_basic(ts_code=code,exchange=exchange)
    return df

# 外汇基础信息（海外）
"""
 目前只有FXCM交易商的数据 所以exchange为空默认是FXCM
 此外提供输入单个代码查询基础信息
"""
def get_fxobasic(code=None, exchange=None, classify=None, fields=None):
    if classify is not None:
        if classify not in get_fxobasic_classify_list:
            Log.log("%sget_fxobasic函数输入的分类类型classify不在范围内\n", context.dt)
            exceptional_handle("get_fxobasic函数输入的分类类型classify不在范围内")

    if code is not None:
        if isinstance(code, str):
            if '.FXCM' not in code:
                Log.log("%sget_fxobasic函数输入的code代码有误\n", context.dt)  # 是否需要设置重新输入
                exceptional_handle("get_fxobasic函数输入的code代码有误")
        else:
            Log.log("%sget_fxobasic函数输入的代码需为字符的形式\n", context.dt)
            exceptional_handle("get_fxobasic函数输入的代码需为字符的形式")

    # 判断fields 格式为列表
    if fields is not None:
        if check_fields(fields,get_fxobasic_range_list):
            df = pro.fx_obasic(exchange=exchange,classify=classify,ts_code=code)
            df = df[fields]
            return df
        else:
            Log.log("%sget_fxobasic函数fields不在范围或格式有误\n", context.dt)
            exceptional_handle("get_fxobasic函数fields内容不在范围或格式有误")

    df = pro.fx_obasic(exchange=exchange,ts_code=code,classify=classify)
    return df

# 港股列表
def get_hkbasic(code=None, status=None, fields=None):
    if status is not None:
        if status not in get_hkbasic_status_list:
            Log.log("%sget_hkbasic函数输入的状态值status有误\n", context.dt)
            exceptional_handle("get_hkbasic函数输入的状态值status有误")

    if code is not None:
        if type(code) != type('') or len(code) != 8:
            Log.log("%sget_hkbasic函数输入的股票代码code格式或长度有误\n", context.dt)
            exceptional_handle("get_hkbasic函数输入的股票代码code格式或长度有误")

    if fields is not None:
        if check_fields(fields,get_hkbasic_range_list):
            df = pro.hk_basic(ts_code=code,list_status=status)
            df = df[fields]
            return df
        else:
            Log.log("%sget_hkbasic函数fields不在范围或格式有误\n", context.dt)
            exceptional_handle("get_hkbasic函数fields内容不在范围或格式有误")

    df = pro.hk_basic(ts_code=code,list_status=status)  # 获取全部可交易股票基础信息
    return df


# 美股列表
"""
 1.获取相关状态股票基础信息
 2.获取具体股票的信息
"""
def get_usbasic(code=None, classify=None, fields=None):
    if classify is not None:
        if classify not in get_usbasic_classify_list:
            Log.log("%sget_usbasic函数输入的分类值classify有误\n", context.dt)
            exceptional_handle("get_usbasic函数输入的分类值classify有误")

    if code is not None:
        if type(code) != type(''):
            Log.log("%sget_usbasic函数输入的股票代码code格式有误\n", context.dt)
            exceptional_handle("get_usbasic函数输入的股票代码code格式有误")

    if fields is not None:
        if check_fields(fields,get_usbasic_range_list):
            df = pro.us_basic(ts_code=code,classify=classify)
            df = df[fields]
            return df
        else:
            Log.log("%sget_usbasic函数fields不在范围或格式有误\n", context.dt)
            exceptional_handle("get_usbasic函数fields内容不在范围或格式有误")

    df = pro.us_basic(ts_code=code,classify=classify)  # 获取全部可交易股票基础信息
    return df

# 黄金现货基础信息
# 获取上海黄金交易所现货合约基础信息
'''def get_sgebasic(code=None, fields=None):    # 不输入为获取全部
    range_ = ['ts_code', 'ts_name', 'trade_type', 't_unit',
              'p_unit', 'min_change', 'price_limit', 'min_vol',
              'max_vol', 'trade_mode', 'margin_rate', 'liq_rate',
              'trade_time', 'list_date']
    if code is not None:
        if isinstance(code,str) is False:
            Log.log("%sget_sgebasic函数输入的代码格式有误\n", context.dt)
            return

    if fields is not None:
        if check_fields(fields,range_):
            df = pro.sge_basic(ts_code=code)
            df = df[fields]
            return df
        else:
            return

    df = pro.sge_basic(ts_code=code)
    return df'''
