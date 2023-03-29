"""
后台运行函数
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from frame.strategy import *
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from app01.views import *

START_DATE = sys.argv[1]
END_DATE = sys.argv[2]
CASH = sys.argv[3]
CASH = int(CASH)

context.set(CASH, START_DATE, END_DATE)


def run():
    # ***初始化工作***
    # plt_df是用来画图的一个Data
    # Frame
    plt_df = pd.DataFrame(index=context.date_range, columns=['value'])

    init_value = context.portfolio.starting_cash  # 策略开始前手里的资金
    if init_value == 0:
        Log.log("初始策略资金为0,请认真检查策略!\n")
        return
    initialize(context)  # 框架策略初始化函数
    last_price = {}  # 当今天停牌时，记录着上一个不停牌时的价格

    # ***核心工作***
    # ------------------------------在指定日期内循环遍历每一天------------------------------
    for dt in context.date_range:
        # context.dt = parse(dt)  # 时间作横坐标
        context.dt = dt
        PositionInfo.log("%s:\n", context.dt)
        handle_data(context)  # 框架策略执行函数
        value = context.portfolio.available_cash  # 账户总价值
        context.runtime = context.runtime + 1  # 累加运行天数

        # ----------------循环遍历总账户里的所有证券仓位--------------------
        # 当天闭市后，计算每天仓位里的证券所有价值
        for stock in context.portfolio.positions:
            today_data = get_today_data(stock)  # 获取这只证券今天价格
            if len(today_data) == 0:  # 如果停牌了，按上个不停牌日的价格算
                p = last_price[stock]
            else:
                p = today_data['open']  # 如果不停牌，按今天的开盘价算
                last_price[stock] = p
            context.portfolio.positions[stock].value = p * context.portfolio.positions[stock].total_amount  # 更新这只证券的价值
            value += context.portfolio.positions[stock].value
            # 仓位信息Info
            PositionInfo.log("%s(%s)  %s  %s  %s\n", context.portfolio.positions[stock].security_name, stock,
                             context.portfolio.positions[stock].total_amount, p, round(value, 2))
        context.portfolio.positions_value = value - context.portfolio.available_cash  # 这天的所有持仓总价值(不包括available_cash)
        # ------------------遍历总账户证券仓位结束------------------------
        # ---------------------循环遍历所有子账户------------------------
        for subp in range(len(context.portfolio.subPortfolio)):
            sub_total_value = context.portfolio.subPortfolio[subp].available_cash  # 这个子账户的总价值
            # ----------------循环遍历子账户里所有证券仓位--------------------
            # 当天闭市后，计算每天每个子账户仓位里的证券所有价值
            for stock in context.portfolio.subPortfolio[subp].positions:
                today_data = get_today_data(stock)  # 获取这只证券今天价格
                if len(today_data) == 0:  # 如果停牌了，按上个不停牌日的价格算
                    p = last_price[stock]
                else:
                    p = today_data['open']  # 如果不停牌，按今天的开盘价算
                    last_price[stock] = p
                context.portfolio.subPortfolio[subp].positions[stock].value = p * context.portfolio.subPortfolio[
                    subp].positions[stock].total_amount  # 更新这只证券的价值
                sub_total_value += context.portfolio.subPortfolio[subp].positions[stock].value
                # 仓位信息Info
                PositionInfo.log("%s(%s)  %s  %s  %s\n",
                                 context.portfolio.subPortfolio[subp].positions[stock].security_name, stock,
                                 context.portfolio.subPortfolio[subp].positions[stock].total_amount, p,
                                 round(context.portfolio.subPortfolio[subp].positions[stock].value))
            # 子账户仓位遍历完后 账户核算
            context.portfolio.subPortfolio[subp].positions_value = sub_total_value - context.portfolio.subPortfolio[
                subp].available_cash
            context.portfolio.subPortfolio[subp].total_value = sub_total_value
            context.portfolio.subPortfolio[subp].daily_pnl = sub_total_value - context.portfolio.subPortfolio[
                subp].pre_total_value  # 当日盈亏
            context.portfolio.subPortfolio[subp].daily_profit[context.dt] = context.portfolio.subPortfolio[
                subp].daily_pnl  # 每天盈亏金额情况
            if context.portfolio.subPortfolio[subp].pre_total_value != 0:
                context.portfolio.subPortfolio[subp].daily_profit_chg[context.dt] = round(
                    (context.portfolio.subPortfolio[subp].daily_pnl / context.portfolio.subPortfolio[
                        subp].pre_total_value), 4)  # 当天收益率
            context.portfolio.subPortfolio[subp].pre_total_value = sub_total_value  # 更新上一个交易日总账户价值为今天，为下一个交易日做准备
            if context.portfolio.subPortfolio[subp].starting_cash != 0:
                context.portfolio.subPortfolio[subp].returns = (sub_total_value - context.portfolio.subPortfolio[
                    subp].starting_cash) / context.portfolio.subPortfolio[subp].starting_cash
            value += sub_total_value  # 累加总价值
        # -----------------------------------子账户遍历结束-----------------------------------------------------

        plt_df.loc[dt, 'value'] = value  # 在横坐标dt这一天的账户总价值value

        # 判断今天相较上一个交易日是亏了还是赚了
        if value < context.portfolio.pre_total_value:
            context.loss_time = context.loss_time + 1
        elif value > context.portfolio.pre_total_value:
            context.profit_time = context.profit_time + 1

        # 总账户核算
        context.portfolio.returns = (value - init_value) / init_value
        context.portfolio.daily_pnl = value - context.portfolio.pre_total_value  # 当日盈亏
        context.portfolio.daily_profit[context.dt] = context.portfolio.daily_pnl  # 每天盈亏金额情况
        if context.portfolio.pre_total_value != 0:
            context.portfolio.daily_profit_chg[context.dt] = round(
                (context.portfolio.daily_pnl / context.portfolio.pre_total_value), 4)  # 当天收益率
        context.portfolio.pre_total_value = value  # 更新上一个交易日总账户价值为今天，为下一个交易日做准备
        context.portfolio.total_value = value  # 现在总账户价值

    # ---------------------------------指定日期每天遍历完毕---------------------------------

    # ***收尾工作***
    # 策略的收益率线
    plt_df['ratio'] = ((plt_df['value'] - init_value) / init_value) * 100

    # 基准线信息
    bm_df = attribute_history(count=context.total_dates, security=context.benchmark)
    bm_init = bm_df['open'][0]
    # plt_df里加上基准线
    plt_df['benckmark_ratio'] = ((bm_df['open'] - bm_init) / bm_init) * 100
    context.BTotal_Returns = round(plt_df['benckmark_ratio'][-1] / 100, 4)

    # 指标计算
    Total_Returns()
    Total_Annualized_Returns()
    Beta(bm_df['pct_chg'] / 100)
    Alpha()
    Algorithm_Volatility()
    Benchmark_Volatility(bm_df['pct_chg'] / 100)
    Sharpe()
    Downside_Risk()
    Sortino()
    Win(plt_df['ratio'], plt_df['benckmark_ratio'])
    Profit_loss_ratio()
    Max_Drawdown(plt_df['ratio'])
    Information_Ratio(bm_df['pct_chg'] / 100)

    # ----------------------plot画图----------------------

    # plt_df[['ratio', 'benckmark_ratio']].plot()
    #
    # def to_percent(temp, position):  # 纵坐标数值加上%符号
    #     return '%1.0f' % temp + '%'
    #
    # plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))

    # ----------------------plot画图----------------------

    # 输出交易数据
    print("%.2f%%" % (context.Total_Returns * 100))
    print("%.2f%%" % (context.Total_Annualized_Returns * 100))
    print("%.2f" % context.Alpha)
    print("%.2f" % context.Beta)
    print("%.2f" % context.Sharpe)
    print("%.2f" % context.Algorithm_Volatility)
    print("%.2f" % context.Benchmark_Volatility)
    print("%.2f" % context.Downside_Risk)
    print("%.2f" % context.Sortino)
    print("%.2f" % context.Information_Ratio)
    print("%.2f" % context.profit_time)
    print("%.2f" % context.loss_time)
    print("%.2f" % context.winning)
    print("%.2f" % context.winning_daily)
    print("%.2f" % context.profit_loss_ratio)
    print(context.Max_Drawdown_L)
    print(context.Max_Drawdown_R)
    print(plt_df.index.tolist())
    print(plt_df['ratio'].tolist())
    print(plt_df['benckmark_ratio'].tolist())

    # print('策略收益率: ', context.Total_Returns * 100, '%')
    # print('策略年化收益率: ', context.Total_Annualized_Returns * 100, '%')
    # print('阿尔法系数: ', context.Alpha)
    # print('贝塔系数: ', context.Beta)
    # print('夏普比率: ', context.Sharpe)
    # print('策略波动率: ', context.Algorithm_Volatility)
    # print('基准波动率: ', context.Benchmark_Volatility)
    # print('下行波动率: ', context.Downside_Risk)
    # print('索提诺比率: ', context.Sortino)
    # print('信息比率: ', context.Information_Ratio)
    # print('盈利次数: ', context.profit_time)
    # print('亏损次数: ', context.loss_time)
    # print('总胜率: ', context.winning)
    # print('日胜率: ', context.winning_daily)
    # print('盈亏比: ', context.profit_loss_ratio)
    # print('最大回撤区间: [', context.Max_Drawdown_L, ',', context.Max_Drawdown_R, ']')

    # 执行完毕，关闭文件
    # os.system("git checkout frame/strategy.py")     # 暂时的解决方案: 将strategy.py恢复初始状态
    TradeInfo.f.close()
    PositionInfo.f.close()
    Log.f.close()


# ----------------------------------------------------#
run()
