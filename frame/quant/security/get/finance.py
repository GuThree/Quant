"""
财务数据获取函数
"""

from quant.classes.exception import *

financial_table_list = ['income', 'balancesheet', 'cashflow', 'forecast', 'express', 'dividend',
                            'fina_indicator', 'fina_audit', 'fina_mainbz', 'disclosure_date']

def income(condition, fields):
    _ts_code = None
    _ann_date = None
    _f_ann_date = None
    _start_date = None
    _end_date = None
    _period = None
    _report_type = None
    _comp_type = None
    _end_type = None

    for key in condition:
        if key == 'ts_code':
            _ts_code = condition[key]
        elif key == 'ann_date':
            _ann_date = condition[key]
        elif key == 'f_ann_date':
            _f_ann_date = condition[key]
        elif key == 'start_date':
            _start_date = condition[key]
        elif key == 'end_date':
            _end_date = condition[key]
        elif key == 'period':
            _period = condition[key]
        elif key == 'report_type':
            _report_type = condition[key]
        elif key == 'comp_type':
            _comp_type = condition[key]
        elif key == 'end_type':
            _end_type = condition[key]
        else:
            continue

    if not _ts_code:
        Log.log("%sget_fundamentals函数当要获取income利润表数据时,ts_code是必须参数,必须指定股票代码\n", context.dt)
        exceptional_handle("get_fundamentals函数当要获取income利润表数据时,ts_code是必须参数,必须指定股票代码")

    df = pro.income(ts_code=_ts_code, ann_date=_ann_date, f_ann_date=_f_ann_date, start_date=_start_date, end_date=_end_date,
                        period=_period, report_type=_report_type, comp_type=_comp_type, end_type=_end_type,
                            fields=fields)

    return df

def balancesheet(condition, fields):
    _ts_code = None
    _ann_date = None
    _start_date = None
    _end_date = None
    _period = None
    _report_type = None
    _comp_type = None
    _end_type = None

    for key in condition:
        if key == 'ts_code':
            _ts_code = condition[key]
        elif key == 'ann_date':
            _ann_date = condition[key]
        elif key == 'start_date':
            _start_date = condition[key]
        elif key == 'end_date':
            _end_date = condition[key]
        elif key == 'period':
            _period = condition[key]
        elif key == 'report_type':
            _report_type = condition[key]
        elif key == 'comp_type':
            _comp_type = condition[key]
        elif key == 'end_type':
            _end_type = condition[key]
        else:
            continue

    if not _ts_code:
        Log.log("%sget_fundamentals函数当要获取balancesheet资产负债表数据时,ts_code是必须参数,必须指定股票代码\n", context.dt)
        exceptional_handle("get_fundamentals函数当要获取balancesheet资产负债表数据时,ts_code是必须参数,必须指定股票代码")

    df = pro.balancesheet(ts_code=_ts_code, ann_date=_ann_date, start_date=_start_date, end_date=_end_date,
                                period=_period, report_type=_report_type, comp_type=_comp_type, end_type=_end_type,
                                    fields=fields)

    return df

def cashflow(condition, fields):
    _ts_code = None
    _ann_date = None
    _f_ann_date = None
    _start_date = None
    _end_date = None
    _period = None
    _report_type = None
    _comp_type = None
    _end_type = None
    _is_calc = None

    for key in condition:
        if key == 'ts_code':
            _ts_code = condition[key]
        elif key == 'ann_date':
            _ann_date = condition[key]
        elif key == 'f_ann_date':
            _f_ann_date = condition[key]
        elif key == 'start_date':
            _start_date = condition[key]
        elif key == 'end_date':
            _end_date = condition[key]
        elif key == 'period':
            _period = condition[key]
        elif key == 'report_type':
            _report_type = condition[key]
        elif key == 'comp_type':
            _comp_type = condition[key]
        elif key == 'end_type':
            _end_type = condition[key]
        elif key == 'is_calc':
            _is_calc = condition[key]
        else:
            continue

    if not _ts_code:
        Log.log("%sget_fundamentals函数当要获取cashflow现金流量表数据时,ts_code是必须参数,必须指定股票代码\n", context.dt)
        exceptional_handle("get_fundamentals函数当要获取cashflow现金流量表数据时,ts_code是必须参数,必须指定股票代码")

    df = pro.cashflow(ts_code=_ts_code, ann_date=_ann_date, f_ann_date=_f_ann_date, start_date=_start_date, end_date=_end_date,
                            period=_period, report_type=_report_type, comp_type=_comp_type, end_type=_end_type, is_calc=_is_calc,
                                fields=fields)

    return df

def forecast(condition, fields):
    _ts_code = None
    _ann_date = None
    _start_date = None
    _end_date = None
    _period = None
    _type = None

    for key in condition:
        if key == 'ts_code':
            _ts_code = condition[key]
        elif key == 'ann_date':
            _ann_date = condition[key]
        elif key == 'start_date':
            _start_date = condition[key]
        elif key == 'end_date':
            _end_date = condition[key]
        elif key == 'period':
            _period = condition[key]
        elif key == 'type':
            _type = condition[key]
        else:
            continue

    if not _ts_code and not _ann_date:
        Log.log("%sget_fundamentals函数当要获取forecast业绩预告表数据时,ann_date和ts_code至少输入一个参数\n", context.dt)
        exceptional_handle("get_fundamentals函数当要获取forecast业绩预告表数据时,ann_date和ts_code至少输入一个参数")

    df = pro.forecast(ts_code=_ts_code, ann_date=_ann_date, start_date=_start_date,
                            end_date=_end_date, period=_period, type=_type,
                                fields=fields)

    return df

def express(condition, fields):
    _ts_code = None
    _ann_date = None
    _start_date = None
    _end_date = None
    _period = None

    for key in condition:
        if key == 'ts_code':
            _ts_code = condition[key]
        elif key == 'ann_date':
            _ann_date = condition[key]
        elif key == 'start_date':
            _start_date = condition[key]
        elif key == 'end_date':
            _end_date = condition[key]
        elif key == 'period':
            _period = condition[key]
        else:
            continue

    if not _ts_code:
        Log.log("%sget_fundamentals函数当要获取express业绩快报表数据时,ts_code是必须参数,必须指定股票代码\n", context.dt)
        exceptional_handle("get_fundamentals函数当要获取express业绩快报表数据时,ts_code是必须参数,必须指定股票代码")

    df = pro.express(ts_code=_ts_code, ann_date=_ann_date, start_date=_start_date,
                        end_date=_end_date, period=_period, fields=fields)

    return df

def dividend(condition, fields):
    _ts_code = None
    _ann_date = None
    _record_date = None
    _ex_date = None
    _imp_ann_date = None

    for key in condition:
        if key == 'ts_code':
            _ts_code = condition[key]
        elif key == 'ann_date':
            _ann_date = condition[key]
        elif key == 'record_date':
            _record_date = condition[key]
        elif key == 'ex_date':
            _ex_date = condition[key]
        elif key == 'imp_ann_date':
            _imp_ann_date = condition[key]
        else:
            continue

    df = pro.dividend(ts_code=_ts_code, ann_date=_ann_date, record_date=_record_date,
                        ex_date=_ex_date, imp_ann_date=_imp_ann_date, fields=fields)

    return df

def fina_indicator(condition, fields):
    _ts_code = None
    _ann_date = None
    _start_date = None
    _end_date = None
    _period = None

    for key in condition:
        if key == 'ts_code':
            _ts_code = condition[key]
        elif key == 'ann_date':
            _ann_date = condition[key]
        elif key == 'start_date':
            _start_date = condition[key]
        elif key == 'end_date':
            _end_date = condition[key]
        elif key == 'period':
            _period = condition[key]
        else:
            continue

    if not _ts_code:
        Log.log("%sget_fundamentals函数当要获取fina_indicator财务指标数据表数据时,ts_code是必须参数,必须指定股票代码\n", context.dt)
        exceptional_handle("get_fundamentals函数当要获取fina_indicator财务指标数据表数据时,ts_code是必须参数,必须指定股票代码")

    df = pro.fina_indicator(ts_code=_ts_code, ann_date=_ann_date, start_date=_start_date,
                                end_date=_end_date, period=_period, fields=fields)

    return df

def fina_audit(condition, fields):
    _ts_code = None
    _ann_date = None
    _start_date = None
    _end_date = None
    _period = None

    for key in condition:
        if key == 'ts_code':
            _ts_code = condition[key]
        elif key == 'ann_date':
            _ann_date = condition[key]
        elif key == 'start_date':
            _start_date = condition[key]
        elif key == 'end_date':
            _end_date = condition[key]
        elif key == 'period':
            _period = condition[key]
        else:
            continue

    if not _ts_code:
        Log.log("%sget_fundamentals函数当要获取fina_audit财务审计意见表数据时,ts_code是必须参数,必须指定股票代码\n", context.dt)
        exceptional_handle("get_fundamentals函数当要获取fina_audit财务审计意见表数据时,ts_code是必须参数,必须指定股票代码")

    df = pro.fina_audit(ts_code=_ts_code, ann_date=_ann_date, start_date=_start_date,
                                end_date=_end_date, period=_period, fields=fields)

    return df

def fina_mainbz(condition, fields):
    _ts_code = None
    _period = None
    _start_date = None
    _end_date = None
    _type = None

    for key in condition:
        if key == 'ts_code':
            _ts_code = condition[key]
        elif key == 'type':
            _type = condition[key]
        elif key == 'start_date':
            _start_date = condition[key]
        elif key == 'end_date':
            _end_date = condition[key]
        elif key == 'period':
            _period = condition[key]
        else:
            continue

    if not _ts_code:
        Log.log("%sget_fundamentals函数当要获取fina_mainbz主营业务构成表数据时,ts_code是必须参数,必须指定股票代码\n", context.dt)
        exceptional_handle("get_fundamentals函数当要获取fina_mainbz主营业务构成表数据时,ts_code是必须参数,必须指定股票代码")

    df = pro.fina_mainbz(ts_code=_ts_code, period=_period, start_date=_start_date,
                                end_date=_end_date, type=_type, fields=fields)

    return df

def disclosure_date(condition, fields):
    _ts_code = None
    _pre_date = None
    _actual_date = None
    _end_date = None

    for key in condition:
        if key == 'ts_code':
            _ts_code = condition[key]
        elif key == 'pre_date':
            _pre_date = condition[key]
        elif key == 'actual_date':
            _actual_date = condition[key]
        elif key == 'end_date':
            _end_date = condition[key]
        else:
            continue

    df = pro.disclosure_date(ts_code=_ts_code, pre_date=_pre_date, actual_date=_actual_date,
                                    end_date=_end_date, fields=fields)

    return df

# -----------------------------------------------------------------------------------------
"""
table是财务表名称
condition是对应财务表得筛选参数 若输入限定范围之外得参数会过滤忽略掉 不影响函数执行
fields是选择你想要的财务表字段
"""
def get_fundamentals(table=None, condition=None, fields=None):

    # 财务表参数检验
    if table not in financial_table_list:
        Log.log("%sget_fundamentals函数未知财务表\n", context.dt)
        exceptional_handle("get_fundamentals函数未知财务表")

    # condition字典类型检验
    if type(condition) != type({}):
        Log.log("%sget_fundamentals函数的条件condition参数需是字典类型\n", context.dt)
        exceptional_handle("get_fundamentals函数的条件condition参数需是字典类型")

    # 判定财务表类型
    data = None
    if table == 'income':
        data = income(condition, fields)
    elif table == 'balancesheet':
        data = balancesheet(condition, fields)
    elif table == 'cashflow':
        data = cashflow(condition, fields)
    elif table == 'forecast':
        data = forecast(condition, fields)
    elif table == 'express':
        data = express(condition, fields)
    elif table == 'dividend':
        data = dividend(condition, fields)
    elif table == 'fina_indicator':
        data = fina_indicator(condition, fields)
    elif table == 'fina_audit':
        data = fina_audit(condition, fields)
    elif table == 'fina_mainbz':
        data = fina_mainbz(condition, fields)
    elif table == 'disclosure_date':
        data = disclosure_date(condition, fields)
    else:
        return

    return data

