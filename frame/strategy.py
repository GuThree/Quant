# 导入函数库
from quant import *

def initialize(context):
    # 输出内容到日志 Log.log()
    Log.log("初始化函数开始运行且全局只运行一次\n")
    # 设定沪深300作为基准
    set_benckmark('399300.SZ')
    # 设置滑点
    set_PerSlippage(0)

    # 持仓数量
    g.stocknum = 3
    # 交易日计时器
    g.days = 0
    # 调仓频率
    g.refresh_rate = 5

def check_stocks(context):
    list1 = daily_info(str(context.dt), field='total_mv', sort="ascend")['ts_code'][:10]
    list1 = list(list1.index)
    return  list1[:g.stocknum]

# 每日运行函数
def handle_data(context):
    if g.days % g.refresh_rate == 0:
        ## 获取持仓列表
        sell_list = list(context.portfolio.positions.keys())
        # 如果有持仓，则卖出
        if len(sell_list) > 0:
            for stock in sell_list:
                order_target(stock, 0)

        ## 分配资金
        if len(context.portfolio.positions) < g.stocknum:
            Num = g.stocknum - len(context.portfolio.positions)
            Cash = context.portfolio.available_cash / Num
        else:
            Cash = 0

        ## 选股
        stock_list = check_stocks(context)

        ## 买入股票
        for stock in stock_list:
            if len(context.portfolio.positions.keys()) < g.stocknum:
                order_value(stock, Cash)

        # 天计数加一
        g.days = 1
    else:
        g.days += 1