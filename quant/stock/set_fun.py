"""
策略设置函数
"""

from quant.classes.object import *

# 设置基准
def set_benckmark(security):
    context.benchmark = security

#设置股票池
def set_universe(security_list):
    context.universe = security_list