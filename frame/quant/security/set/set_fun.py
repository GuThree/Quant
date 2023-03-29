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

# 设置佣金
def set_commission(value):
    context.commission = value

# 设置印花税
def set_stamp_duty(value):
    context.stamp_duty = value

# 设置过户费
def set_transfer_fee(value):
    context.transfer_fee = value

# 设置固定滑点值
def set_FixedSlippage(var, security = None):
    if security:
        context.slippage_type = 0
        context.slippage_FixedSec[security] = var
    else:
        context.slippage_type = 0
        context.slippage = var

# 设置百分比滑点值
def set_PerSlippage(var, security = None):
    if var < 0 or var >= 1:
        Log.log("%s:百分比滑点取值范围是[0,1)\n", context.dt)
        return
    if security:
        context.slippage_type = 1
        context.slippage_PerSec[security] = var
    else:
        context.slippage_type = 1
        context.slippage = var

# 设置跳数滑点值
def set_JumpSlippage(var,  security = None):
    if security:
        context.slippage_type = 2
        context.slippage_JumpSec[security] = var
    else:
        context.slippage_type = 2
        context.slippage = var