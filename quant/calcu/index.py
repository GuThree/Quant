"""
指标计算函数
"""

from quant.stock.get_fun import *
import math

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

#策略收益
def Total_Returns(Pstart, Pend):
    context.Total_Returns = (Pend - Pstart) / Pstart


#策略年化收益
def Total_Annualized_Returns():
    math.pow((1 + context.Total_Returns), (250 / context.runtime)) - 1

