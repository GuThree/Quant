"""
宏观经济数据
"""

from quant.security.check_fun import *
from quant.classes.exception import *

get_cnCPI_range_list = ['month', 'nt_val', 'nt_yoy', 'nt_mom', 'nt_accu', 'town_val', 'town_yoy',
              'town_mom', 'town_accu', 'cnt_val', 'cnt_yoy', 'cnt_mom', 'cnt_accu']
get_cnGDP_range_list = ['quarter', 'gdp', 'gdp_yoy', 'pi', 'pi_yoy', 'si', 'si_yoy', 'ti', 'ti_yoy']

# 居民消费价格指数
"""
 获取CPI居民消费价格数据，包括全国、城市和农村的数据
 1.获取单个月份或多个月份的数据-输入字符串，格式为YYYY-MM，多个字符串用逗号隔开
 2.获取一个时间段内的所有数据-输入开始月份和截止月份，格式为YYYY-MM
"""
def get_cnCPI(m=None,start_m=None,end_m=None,fields=None):

    if m is not None:
        if start_m or end_m is not None:
            Log.log("%sget_cnCPI函数输入了无关变量\n", context.dt)
            exceptional_handle("get_cnCPI函数输入了无关变量")
        if check_single(m):
            try:  # 判断输入的日期格式是否为'%Y-%m'
                datetime.datetime.strptime(m, '%Y-%m')
            except ValueError:
                raise ValueError("开始日期输入有误,日期格式应改为‘%Y-%m’")
            m = datetime.datetime.strptime(m, '%Y-%m').strftime('%Y%m')
            if check_fields(fields,get_cnCPI_range_list):
                df = pro.cn_cpi(m=m)
                df = df[fields]
                return df
            df = pro.cn_cpi(m=m)
            return df
        else:
            m_list1 = m.split(',')
            m_list2 = []
            for mon in m_list1:
                try:  # 判断输入的日期格式是否为'%Y-%m'
                    datetime.datetime.strptime(mon, '%Y-%m')
                except ValueError:
                    raise ValueError("开始日期输入有误,日期格式应改为‘%Y-%m’")
                temp = datetime.datetime.strptime(mon, '%Y-%m').strftime('%Y%m')
                m_list2.append(temp)
            m = ','.join(m_list2)

            if fields is not None:
                if check_fields(fields, get_cnCPI_range_list):
                    df = pro.cn_cpi(m=m)
                    df = df[fields]
                    return df
                else:
                    Log.log("%sget_cnCPI函数fields不在范围或格式有误\n", context.dt)
                    exceptional_handle("get_cnCPI函数fields内容不在范围或格式有误")
            else:
                df = pro.cn_cpi(m=m)
                return df

    if start_m and end_m is not None:
        try:  # 判断输入的日期格式是否为'%Y-%m'
            datetime.datetime.strptime(start_m, '%Y-%m')
            datetime.datetime.strptime(end_m, '%Y-%m')
        except ValueError:
            raise ValueError("开始日期输入有误,日期格式应改为‘%Y-%m’")
        start_m = datetime.datetime.strptime(start_m, '%Y-%m').strftime('%Y%m')
        end_m = datetime.datetime.strptime(end_m, '%Y-%m').strftime('%Y%m')

        if fields is not None:
            if check_fields(fields, get_cnCPI_range_list):
                df = pro.cn_cpi(start_m=start_m, end_m=end_m)
                df = df[fields]
                return df
            else:
                Log.log("%sget_cnCPI函数fields不在范围或格式有误\n", context.dt)
                exceptional_handle("get_cnCPI函数fields内容不在范围或格式有误")
        else:
            df = pro.cn_cpi(start_m=start_m, end_m=end_m)
            return df
    else:
        if start_m or end_m is not None:
            Log.log("%sget_cnCPI函数缺少开始月份或结束月份\n", context.dt)
            exceptional_handle("get_cnCPI函数缺少开始月份或结束月份")

    if fields is not None:
        if check_fields(fields, get_cnCPI_range_list):
            df = pro.cn_cpi()
            df = df[fields]
            return df
        else:
            Log.log("%sget_cnCPI函数fields不在范围或格式有误\n", context.dt)
            exceptional_handle("get_cnCPI函数fields内容不在范围或格式有误")
    else:
        df = pro.cn_cpi()
        return df

# GDP数据
"""
 1.获取单个季度或多个季度的数据-输入字符串，格式为YYYYQX，多个字符串用逗号隔开
 2.获取一个时间段内的所有数据-输入开始季度和截止季度，格式为YYYYQX
"""
def get_cnGDP(q=None, start_q=None, end_q=None, fields=None):

    if q is not None:
        if start_q or end_q is not None:
            Log.log("%sget_cnGDP函数输入了无关变量\n", context.dt)
            exceptional_handle("get_cnGDP函数输入了无关变量")
        if check_single(q):
            if fields is not None:
                if check_fields(fields,get_cnGDP_range_list):
                    df = pro.cn_gdp(q=q)
                    df = df[fields]
                    return df
                else:
                    Log.log("%sget_cnGDP函数fields不在范围或格式有误\n", context.dt)
                    exceptional_handle("get_cnGDP函数fields内容不在范围或格式有误")
            else:
                df = pro.cn_gdp(q=q)
                return df
        else:
            q_list1 = q.split(',')
            q_list2 = []
            for qua in q_list1:
                if len(qua) != 6:
                    Log.log("%sget_cnGDP函数输入的季度中格式有误\n", context.dt)
                    exceptional_handle("get_cnGDP函数输入的季度中格式有误")
                q_list2.append(qua)
            q = ','.join(q_list2)
            if fields is not None:
                if check_fields(fields, get_cnGDP_range_list):
                    df = pro.cn_gdp(q=q)
                    df = df[fields]
                    return df
                else:
                    Log.log("%sget_cnGDP函数fields不在范围或格式有误\n", context.dt)
                    exceptional_handle("get_cnGDP函数fields内容不在范围或格式有误")
            else:
                df = pro.cn_gdp(q=q)
                return df

    if start_q and end_q is not None:
        if len(start_q) != 6 or len(end_q) != 6:
            Log.log("%sget_cnGDP函数输入的格式有误\n", context.dt)
            exceptional_handle("get_cnGDP函数输入的格式有误")
        if fields is not None:
            if check_fields(fields, get_cnGDP_range_list):
                df = pro.cn_gdp(start_q=start_q, end_q=end_q)
                df = df[fields]
                return df
            else:
                Log.log("%sget_cnGDP函数fields不在范围或格式有误\n", context.dt)
                exceptional_handle("get_cnGDP函数fields内容不在范围或格式有误")
        else:
            df = pro.cn_gdp(start_q=start_q, end_q=end_q)
            return df
    else:
        if start_q or end_q is not None:
            Log.log("%sget_cnGDP函数缺少开始月份或结束月份\n", context.dt)
            exceptional_handle("get_cnGDP函数缺少开始月份或结束月份")

    if fields is not None:
        if check_fields(fields, get_cnGDP_range_list):
            df = pro.cn_gdp()
            df = df[fields]
            return df
        else:
            Log.log("%sget_cnGDP函数fields不在范围或格式有误\n", context.dt)
            exceptional_handle("get_cnGDP函数fields内容不在范围或格式有误")
    else:
        df = pro.cn_gdp()
        return df
