"""
策略实现框架
"""
from quant import *

def initialize(context):
    set_benckmark('000001.SZ')
    g.p1 = 5
    g.p2 = 60
    g.security = '000006.SZ'

def handle_data(context):
    hist = attribute_history(g.security, g.p2)
    ma5 = hist['close'][-g.p1].mean()
    ma60 = hist['close'].mean()

    if ma5 > ma60 and g.security not in context.portfolio.positions:
        order_value(g.security, context.portfolio.available_cash)
    elif ma5 < ma60 and g.security in context.portfolio.positions:
        order_target(g.security, 0)