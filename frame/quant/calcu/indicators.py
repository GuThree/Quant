"""
指标计算函数
"""

from quant.security.get import *

"""
    指标数据：
    Total Returns 策略收益
    Total Annualized Returns 策略年化收益
    Alpha 阿尔法
    Beta 贝塔
    Sharpe 夏普比率
    Sortino 索提诺比率
    Information Ratio 信息比率
    Algorithm Volatility 策略波动率
    Benchmark Volatility 基准波动率
    Max Drawdown 最大回撤
    Downside Risk 下行波动率
    胜率
    日胜率
    盈亏比
"""
def IPstand():
    pass


# 策略收益
def Total_Returns():
    context.Total_Returns = ((context.portfolio.total_value - context.portfolio.starting_cash) / context.portfolio.starting_cash)

# 策略年化收益 (要在Total_Returns之后调用)
def Total_Annualized_Returns():
    context.Total_Annualized_Returns = pow((1 + context.Total_Returns), (250 // context.runtime)) - 1

# 阿尔法 (要在Beta之后调用)
def Alpha():
    context.BTotal_Annualized_Returns = pow((1 + context.BTotal_Returns), (250 // context.runtime)) - 1
    context.Alpha = context.Total_Annualized_Returns - (context.Rf + context.Beta * (context.BTotal_Annualized_Returns - context.Rf))

# 贝塔
def Beta(bm_pct_chg):
    bm_pct_chg = bm_pct_chg[1:]
    bm_pct_chg = bm_pct_chg.reset_index(drop=True)
    s_pct_chg = pd.Series(context.portfolio.daily_profit_chg.values())
    s_pct_chg = s_pct_chg[1:]
    s_pct_chg = s_pct_chg.reset_index(drop=True)
    context.Beta = (np.cov(s_pct_chg, bm_pct_chg))[0][1] / np.var(bm_pct_chg)

# 夏普比率 (要在策略波动率之后算)
def Sharpe():
    context.Sharpe = (context.Total_Annualized_Returns - 0.04) / context.Algorithm_Volatility

# 策略波动率
def Algorithm_Volatility():
    s_pct_chg = pd.Series(context.portfolio.daily_profit_chg.values())
    s_pct_chg = s_pct_chg[1:]
    avg_r = s_pct_chg.mean()
    sum = 0
    for r in s_pct_chg:
        sum = sum + (r - avg_r)*(r - avg_r)
    context.Algorithm_Volatility = pow(250 * sum / (len(s_pct_chg) - 1), 0.5)

# 基准波动率
def Benchmark_Volatility(bm_pct_chg):
    bm_pct_chg = bm_pct_chg[1:]
    avg_r = bm_pct_chg.mean()
    sum = 0
    for r in bm_pct_chg:
        sum = sum + (r - avg_r) * (r - avg_r)
    context.Benchmark_Volatility = pow(250 * sum / (len(bm_pct_chg) - 1), 0.5)

# 下行波动率
def Downside_Risk():
    def f(rp, rpi):
        if rp < rpi:
            return 1
        else:
            return 0

    s_pct_chg = pd.Series(context.portfolio.daily_profit_chg.values())
    s_pct_chg = s_pct_chg[1:]
    s_pct_chg = s_pct_chg.reset_index(drop=True)
    sum = 0
    for i in range(len(s_pct_chg)):
        avg_r = s_pct_chg[:i+1].mean()
        sum = sum + ((s_pct_chg[i] - avg_r) * (s_pct_chg[i] - avg_r) * f(s_pct_chg[i], avg_r))
    context.Downside_Risk = pow(250 * sum / len(s_pct_chg), 0.5)

# 索提诺比率 (要在下行波动率之后算)
def Sortino():
    context.Sortino = (context.Total_Annualized_Returns - 0.04) / context.Downside_Risk

# 总胜率 和 日胜率
def Win(s_ratio, b_ratio):
    context.winning = context.profit_time / (context.profit_time + context.loss_time)

    win = 0
    for i in range(len(s_ratio)):
        if s_ratio[i] > b_ratio[i]:
            win = win + 1
    context.winning_daily = win / context.runtime

# 盈亏比
def Profit_loss_ratio():
    s_pct_chg = pd.Series(context.portfolio.daily_profit.values())
    profit_money = 0
    loss_money = 0
    for r in s_pct_chg:
        if r < 0:
            loss_money = loss_money + r
        elif r > 0:
            profit_money = profit_money + r
    loss_money = -1 * loss_money
    context.profit_loss_ratio = profit_money / loss_money

'''
    最大回撤：所有日期区间中回撤绝对值最大的，当有多个最大回撤相等时，只选一个，选择规则为：
    1.等值最大回撤对应的日期区间重叠时：选日期区间最狭窄的
    2.等值最大回撤对应的日期区间不重叠时：选日期区间最晚的
'''
def Max_Drawdown(ratio):
    min_ids = list(np.where(ratio == np.min(ratio)))
    max_ids = list(np.where(ratio == np.max(ratio)))
    mm = 9999999
    for i in max_ids:
        for j in min_ids:
            for ii in i:
                for jj in j:
                    if abs(ii - jj) < mm:
                        mm = ii -jj
                        mi = jj
                        ma = ii
    if ratio.index[mi] <= ratio.index[ma]:
        context.Max_Drawdown_L = ratio.index[mi]
        context.Max_Drawdown_R = ratio.index[ma]
    else:
        context.Max_Drawdown_L = ratio.index[ma]
        context.Max_Drawdown_R = ratio.index[mi]

# 信息比率 (要做策略年化收益率之后计算)
def Information_Ratio(bm_pct_chg):
    bm_pct_chg = bm_pct_chg[1:]
    bm_pct_chg = bm_pct_chg.reset_index(drop=True)
    s_pct_chg = pd.Series(context.portfolio.daily_profit_chg.values())
    s_pct_chg = s_pct_chg[1:]
    s_pct_chg = s_pct_chg.reset_index(drop=True)
    t = s_pct_chg - bm_pct_chg
    t = t * t
    sum = t.sum()
    context.Information_Ratio = (context.Total_Annualized_Returns - context.BTotal_Annualized_Returns) / pow(250 * sum / len(bm_pct_chg), 0.5)
