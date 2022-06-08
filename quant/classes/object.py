"""
类对象
"""

import numpy as np
import pandas as pd
import datetime
from dateutil.parser import parse
import tushare as ts
#from sqlalchemy import create_engine

ts.set_token('9e22c84922d0c39ef78ae4c9562c00dfa79775795f022c03e1432455')
pro = ts.pro_api()

# engine_ts = create_engine('mysql+pymysql://root:gsr3316806@127.0.0.1:3306/TushareDB?charset=utf8&use_unicode=1')
# sql = """SELECT * FROM trade_cal"""
# trade_cal = pd.read_sql_query(sql, engine_ts)

trade_cal = pro.trade_cal()

trade_cal = trade_cal[['cal_date', 'is_open']]
for i in range(len(trade_cal)):
    trade_cal['cal_date'][i] = parse(trade_cal['cal_date'][i]).strftime('%Y-%m-%d')


# 策略消息总览
class Context:
    def __init__(self):
        self.start_date = None      #开始时间
        self.end_date = None        #结束时间
        self.date_range = None      #日期范围
        self.runtime = 0            #已经运行几天
        self.dt = None              #当天日期
        self.benchmark = None       #基准

        self.universe = None        #股票池
        self.portfolio = Portfolio()    #总账户
        self.Total_Returns = 0   #策略收益
        self.Total_Annualized_Returns = 0    #策略年化收益
        self.Alpha = 0        #阿尔法
        self.Beta = 0         #贝塔
        self.Sharpe = 0       #夏普比率
        self.Sortino = 0      #索提诺比率
        self.Information_Ratio = 0      #信息比率
        self.Algorithm_Volatility = 0   #策略波动率
        self.Benchmark_Volatility = 0    #基准波动率
        self.Max_Drawdown = 0       #最大回撤
        self.Downside_Risk = 0      #下行波动率
        self.winning = 0            #胜率
        self.winning_daily = 0      #日胜率
        self.Profit_loss_ratio = 0      #盈亏比


    def set(self, cash, start_date, end_date):
        self.cash = cash
        self.start_date = start_date
        self.end_date = end_date
        self.date_range = trade_cal[(trade_cal['is_open'] == 1) & \
                                    (trade_cal['cal_date'] >= start_date) & \
                                    (trade_cal['cal_date'] <= end_date)]['cal_date'].values
        # Portfolio 初始化
        self.portfolio.available_cash = cash
        self.portfolio.transferable_cash = cash
        self.portfolio.total_value = cash
        self.portfolio.starting_cash = cash



# 全局变量对象
class G:
    pass

# 总账户信息
class Portfolio:
    """
    available_cash: 可用资金, 可用来购买证券的资金
    transferable_cash: 可取资金, 即可以提现的资金, 不包括今日卖出证券所得资金
    locked_cash: 挂单锁住资金
    margin: 保证金，股票、基金保证金都为100%
    positions: 仓位
    total_value: 总的权益, 包括现金, 保证金(期货)或者仓位(股票)的总价值, 可用来计算收益
    returns: 总权益的累计收益；（当前总资产 + 今日出入金 - 昨日总资产） / 昨日总资产；
    starting_cash: 初始资金, 现在等于 inout_cash
    positions_value: 持仓价值
    """
    """
    frozen_cash	float	冻结资金，为子账户冻结资金加总
    total_returns	float	投资组合至今的累积收益率
    daily_returns	float	投资组合每日收益率
    daily_pnl	float	当日盈亏，子账户当日盈亏的加总
    market_value	float	投资组合当前的市场价值，为子账户市场价值的加总
    total_value	float	总权益，为子账户总权益加总
    units	float	份额。在没有出入金的情况下，策略的初始资金
    unit_net_value	float	单位净值
    static_unit_net_value	float	静态单位权益
    transaction_cost	float	当日费用
    pnl	float	当前投资组合的累计盈亏
    start_date	datetime.datetime	策略投资组合的回测/实时模拟交易的开始日期
    annualized_returns	float	投资组合的年化收益率
    """

    def __init__(self):
        self.available_cash = 0
        self.transferable_cash = 0
        self.locked_cash = None
        self.margin = None
        self.positions = {}     #key 是字符串表示哪知股票， value是Position仓位对象
        self.total_value = None
        self.returns = None
        self.starting_cash = None
        self.positions_value = 0


# 子账户信息
class SubPortfolio:
    """
    inout_cash: 累计出入金, 比如初始资金 1000, 后来转移出去 100, 则这个值是 1000 - 100
    available_cash: 可用资金, 可用来购买证券的资金
    transferable_cash: 可取资金, 即可以提现的资金, 不包括今日卖出证券所得资金
    locked_cash: 挂单锁住资金
    *type: 账户所属类型
    long_positions: 多单的仓位, 一个 dict, key 是标的代码, value 是 [Position]对象
    short_positions: 空单的仓位, 一个 dict, key 是标的代码, value 是 [Position]对象
    *positions_value: 持仓价值
    total_value: 总资产, 包括现金, 保证金(期货)或者仓位(股票)的总价值, 可用来计算收益
    *total_liability: 总负债, 等于融资负债、融券负债、利息总负债的总和
    *net_value: 净资产, 等于总资产减去总负债
    *cash_liability: 融资负债
    *sec_liability: 融券负债
    *interest: 利息总负债
    *maintenance_margin_rate: 维持担保比例
    *available_margin: 融资融券可用保证金
    *margin: 保证金，股票、基金保证金都为100%；融资融券保证金为0期货保证金会实时更新,总是等于当前期货价值乘以保证金比率,当保证金不足时,强制平仓.平仓顺序是:亏损多的(相对于开仓均价)先平仓
    """

    def __init__(self):
        self.inout_cash = None
        self.available_cash = None
        self.transferable_cash = None
        self.locked_cash = None
        self.type = None
        self.long_positions = None
        self.short_positions = None
        self.positions_value = None
        self.total_value = None
        self.total_liability = None
        self.net_value = None
        self.cash_liability = None
        self.sec_liability = None
        self.interest = None
        self.maintenance_margin_rate = None
        self.available_margin = None
        self.margin = None

# 持仓位标信息
class Position:
    """
    security: 标的代码
    price: 最新行情价格
    acc_avg_cost 是累计的持仓成本，在清仓/减仓时也会更新，该持仓累积的收益都会用于计算成本（一开始acc_avg_cost为0，amount也为0），
                加仓：new_acc_avg_cost = (acc_avg_cost * amount + trade_value + commission) / (amount + trade_amount)；
                减仓：new_acc_avg_cost = (acc_avg_cost * amount - trade_value + commission) / (amount - trade_amount)
                说明：commission是本次买入或者卖出的手续费
    avg_cost 是当前持仓成本，只有在开仓/加仓时会更新： new_avg_cost = (posiont_value + trade_value + commission) / (position_amount + trade_amount)
            每次买入后会调整avg_cost, 卖出时avg_cost不变. 这个值也会被用来计算浮动盈亏.
    hold_cost: 当日持仓成本，计算方法：当日无收益：hold_cost = 前收价 （清算后），
               加仓：hold_cost = (hold_cost * amount + trade_value)/(amount + trade_amount)，
               减仓：hold_cost = (hold_cost * amount - trade_value)/(amount - trade_amount)；trade_value = trade_price * trade_amount
    init_time: 建仓时间，格式为 datetime.datetime
    transact_time: 最后交易时间，格式为 datetime.datetime
    total_amount: 总仓位, 但不包括挂单冻结仓位( 如果要获取当前持仓的仓位,需要将locked_amount和total_amount相加)
    closeable_amount: 可卖出的仓位 / 场外基金持有份额
    today_amount: 今天开的仓位
    value: 标的价值，计算方法是: price * total_amount * multiplier, 其中股票、基金的multiplier为1，期货为相应的合约乘数
    side: 多/空，'long' or 'short'
    """

    def __init__(self):
        self.security = None
        self.price = None
        self.acc_avg_cost = None
        self.avg_cost = None
        self.hold_cost = None
        self.init_time = None
        self.transact_time = None
        self.total_amount = 0
        self.closeable_amount = None
        self.today_amount = None
        self.value = 0
        self.side = None
        self.pindex = None


# --------------------------------------------------------#
g = G()
context = Context()
