# 判断fields
def check_fields(fields, range_):
    if type(fields) == type([]):
        for i in fields:
            if i not in range_:
                return False
        return True
    else:
        return False

# 判断申万行业代码
def check_industry_code(industry_code):
    if isinstance(industry_code, str):
        if len(industry_code) != 9:
            return False
        if '.SI' not in industry_code:
            return False
    else:
        return False
    return True

# 判断股票代码是否为ts接口股票格式
def check_ts_code(ts_code):
    if isinstance(ts_code, str):
        if len(ts_code) != 9:
            return False
        if '.SZ' not in ts_code and '.SH' not in ts_code and '.BJ' not in ts_code:
            return False
    else:
        return False
    return True


# 判断是否为单个月份/季度
def check_single(s):
    if isinstance(s, str):
        if len(s) != 6:
            return False
        else:
            return True
    else:
        return False
