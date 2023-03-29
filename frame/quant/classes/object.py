"""
类对象
"""

import numpy as np
import pandas as pd
import datetime
from dateutil.parser import parse
import tushare as ts
from quant.classes.log import *
#from sqlalchemy import create_engine

ts.set_token('1909646303eebb913370452a8030607853df092b7692698b32bf72c3')
pro = ts.pro_api()

pd.set_option('mode.chained_assignment', None)  # 不输出警告信息

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
        self.start_date = None      # 开始时间 datetime.datetime类型
        self.end_date = None        # 结束时间 datetime.datetime类型
        self.date_range = None      # 日期范围 numpy.ndarray类型
        self.total_date = 0         # 日期范围内一共有几天(不包括停牌日期)
        self.runtime = 0            # 当前已经运行几天 int类型
        self.dt = None              # 当天日期 datetime.datetime类型
        self.benchmark = None       # 基准 string类型

        self.stamp_duty = 0.001     # 缴纳印花税比率 默认千分之一
        self.commission = 0.0003    # 缴纳佣金(券商手续费)比率 默认万分之三
        self.transfer_fee = 0       # 过户费
        self.slippage = 0           # 滑点值
        self.slippage_type = 0      # 滑点值类型 0是固定 2是百分比 2是跳数
        self.slippage_FixedSec = {} # 指定证券对应固定滑点
        self.slippage_PerSec = {}   # 指定证券对应百分比滑点
        self.slippage_JumpSec = {}  # 指定证券对应跳数滑点
        self.isMainPor = True       # 当前是否为主账户
        self.subPor_index = None    # 如果不是主账户，当前子账号编号

        self.universe = []                   # 证券池 list类型
        self.portfolio = Portfolio()         # 总账户
        self.BTotal_Returns = 0              # 基准收益率
        self.BTotal_Annualized_Returns = 0   # 基准年化收益率
        self.Total_Returns = 0               # 策略收益率
        self.Total_Annualized_Returns = 0    # 策略年化收益率
        self.Alpha = 0                       # 阿尔法
        self.Beta = 0                        # 贝塔
        self.Sharpe = 0                      # 夏普比率
        self.Sortino = 0                     # 索提诺比率
        self.Information_Ratio = 0           # 信息比率
        self.Algorithm_Volatility = 0        # 策略波动率
        self.Benchmark_Volatility = 0        # 基准波动率
        self.Max_Drawdown_L = None           # 最大回撤左区间
        self.Max_Drawdown_R = None           # 最大回撤右区间
        self.Downside_Risk = 0               # 下行波动率
        self.winning = 0                     # 胜率
        self.winning_daily = 0               # 日胜率
        self.profit_loss_ratio = 0           # 盈亏比
        self.profit_time = 0                 # 盈利次数
        self.loss_time = 0                   # 亏损次数
        self.Rf = 0.04                       # 无风险利率

    def set(self, cash, start_date, end_date):
        self.start_date = parse(start_date)
        self.end_date = parse(end_date)
        # date_range是跳过停牌日期
        self.date_range = trade_cal[(trade_cal['is_open'] == 1) & \
                                    (trade_cal['cal_date'] >= start_date) & \
                                    (trade_cal['cal_date'] <= end_date)]['cal_date'].values[::-1]
        self.total_dates = len(self.date_range)

        # Portfolio 初始化
        self.portfolio.available_cash = cash
        self.portfolio.total_value = cash
        self.portfolio.starting_cash = cash
        self.portfolio.pre_total_value = cash




# 全局变量对象
class G:
    pass

# 总账户信息
class Portfolio:
    """
    available_cash: 可用资金, 可用来购买证券的资金
    locked_cash: 挂单锁住资金
    margin: 保证金，股票、基金保证金都为100%
    positions: 仓位
    total_value: 总的权益, 包括现金, 保证金(期货)或者仓位(股票)的总价值, 可用来计算收益
    returns: 总权益的累计收益；（当前总资产 + 今日出入金 - 昨日总资产） / 昨日总资产；
    starting_cash: 初始资金
    positions_value: 持仓价值
    frozen_cash	float	冻结资金，为子账户冻结资金加总
    total_returns	float	投资组合至今的累积收益率
    daily_returns	float	投资组合每日收益率
    daily_pnl	float	当日盈亏，子账户当日盈亏的加总
    market_value	float	投资组合当前的市场价值，为子账户市场价值的加总
    total_value	float	总权益，为子账户总权益加总
    units	float	份额。在没有出入金的情况下，策略的初始资金
    unit_net_value	float	单位净值
    transaction_cost	float	当日费用
    pnl	float	当前投资组合的累计盈亏
    annualized_returns	float	投资组合的年化收益率
    """
    def __init__(self):
        self.available_cash = 0     # 可取资金
        self.locked_cash = None
        self.margin = None
        self.positions = {}         # 证券仓位 key 是字符串表示哪支股票 : value是Position仓位对象
        self.total_value = 0        # 账户总价值 总账户的金额加上每个子账号的金额
        self.pre_total_value = 0    # 前一个交易日的总账户总价值
        self.returns = 0            # 总权益的累计收益；（当前总资产 + 今日出入金 - 昨日总资产） / 昨日总资产；
        self.starting_cash = 0      # 初始资金，就是开始策略时带上的资金，不会变
        self.positions_value = 0    # 总账户里所有仓位价值
        self.daily_pnl = 0          # 当日盈亏
        self.daily_profit = {}      # 每日收益，字典类型，存放某天的账户里收益金额情况 今天价值-昨天价值
        self.daily_profit_chg = {}  # 每日收益率，字典类型，存放某天的账户里收益率 今天收益/昨天价值
        self.subPortfolio = []      # 子账户，列表形式，值是子账户对象
        self.subP_next_index = 0    # 指向下一个未创建的子账户index

    # 给主账户增加资金
    def add_cash(self, cash):
        self.available_cash += cash
        self.total_value += cash

    # 转到某个子账户状态下
    def switch_to_subP(self, index):
        context.isMainPor = False
        context.subPor_index = index

    # 创建子账户
    def create_subP(self, money):
        if self.available_cash < money:
            Log.log("%s:总账户不够资金分配到子账户", context.dt)
            return
        subp = SubPortfolio(money)
        self.available_cash -= money
        self.total_value -= money
        self.subPortfolio.append(subp)
        self.subP_next_index += 1
        return self.subP_next_index - 1         # 返回创建子账户的编号

    # 删除子账户
    def del_subP(self, index):
        if len(self.subPortfolio[index].positions) != 0:
            Log.log("%s编号%s子账户还存在仓位，不能删除\n", context.dt, index)
            return
        self.available_cash += self.subPortfolio[index].available_cash  # 回流资金到主账户
        del self.subPortfolio[index]
        self.subP_next_index -= 1

    # 总账户资金流入到某子账户
    def transfer_cash(self, index, money):
        if self.available_cash < money:
            Log.log("%s:总账户不够资金分配到子账户", context.dt)
            return
        self.available_cash -= money
        self.total_value -= money
        self.subPortfolio[index].add_cash(money)

# 子账户信息
class SubPortfolio:
    def __init__(self, cash):
        self.available_cash = cash      # 可取资金
        self.locked_cash = None
        self.margin = None
        self.positions = {}             # 证券仓位 key 是字符串表示哪支股票 : value是Position仓位对象
        self.starting_cash = cash       # 初始资金，就是开始策略时带上的资金，不会变
        self.total_value = cash         # 子账户总价值
        self.pre_total_value = cash     # 前一个交易日的子账户总价值
        self.returns = 0                # 总权益的累计收益；（当前总资产 + 今日出入金 - 昨日总资产） / 昨日总资产；
        self.positions_value = 0        # 所有仓位价值
        self.daily_pnl = 0              # 当日盈亏
        self.daily_profit = {}          # 每日收益，字典类型，存放某天的账户里收益金额情况 今天价值-昨天价值
        self.daily_profit_chg = {}      # 每日收益率，字典类型，存放某天的账户里收益率 今天收益/昨天价值

    # 子账户增加现金流，一般不在策略直接调用，由总账户类内部调用
    def add_cash(self, cash):
        self.available_cash += cash
        self.total_value += cash

    # 资金回流到总账户
    def backflow_cash(self, cash):
        if self.available_cash < cash:
            Log.log("%s:子账户资金不够回流到总账户", context.dt)
            return
        self.available_cash -= cash
        self.total_value -= cash
        context.portfolio.available_cash += cash
        context.portfolio.total_value += cash

    # 切换到总账户状态下
    def switch_to_mainP(self):
        context.isMainPor = True
        context.subPor_index = None

    # 转到另一个子账户状态
    def switch_to_subP(self, index):
        context.isMainPor = False
        context.subPor_index = index


# 持仓位标信息
class Position:
    """
    security: 标的代码
    price: 最新行情价格
    last_price: 上一个交易日价格
    acc_avg_cost 是累计的持仓成本，在清仓/减仓时也会更新，该持仓累积的收益都会用于计算成本（一开始acc_avg_cost为0，amount也为0），
                加仓：new_acc_avg_cost = (acc_avg_cost * amount + trade_value + commission) / (amount + trade_amount)；
                减仓：new_acc_avg_cost = (acc_avg_cost * amount - trade_value + commission) / (amount - trade_amount)
                说明：commission是本次买入或者卖出的手续费
    avg_cost 是当前持仓成本，只有在开仓/加仓时会更新： new_avg_cost = (posiont_value + trade_value + commission) / (position_amount + trade_amount)
            每次买入后会调整avg_cost, 卖出时avg_cost不变. 这个值也会被用来计算浮动盈亏.
    hold_cost: 当日持仓成本，计算方法：当日无收益：hold_cost = 前收价 （清算后），
               加仓：hold_cost = (hold_cost * amount + trade_value)/(amount + trade_amount)，
               减仓：hold_cost = (hold_cost * amount - trade_value)/(amount - trade_amount)；trade_value = trade_price * trade_amount
    last_update_time: 上次仓位更新时间，格式为 datetime.datetime
    total_amount: 总仓位, 但不包括挂单冻结仓位( 如果要获取当前持仓的仓位,需要将locked_amount和total_amount相加)
    value: 标的价值，计算方法是: price * total_amount * multiplier, 其中股票、基金的multiplier为1，期货为相应的合约乘数
    """

    def __init__(self):
        self.security_name = None       # 标的中文名
        self.security_code = None       # 标的代码
        self.price = None               # 标的最新行情价格
        self.last_price = None          # 上一个交易日价格
        self.acc_avg_cost = None
        self.avg_cost = None
        self.hold_cost = None
        self.last_update_time = None    # 上次仓位更新时间
        self.total_amount = 0           # 仓位证券总数量
        self.proportion = 0
        self.value = 0                  # 当前仓位总价值
        self.buy_pp = []                # 每次买入点价格 和buy_pn一一对应
        self.buy_pn = []                # 每次买入点数量 和buy_pp一一对应


# --------------------------------------------------------#
g = G()
context = Context()
TradeInfo = TradeInfo()
PositionInfo = PositionInfo()
Log = Log()
