"""
交易函数
"""

from quant.stock.get_fun import *

# 按股数下单(作为基础函数)
def _order(today_data, security, amount):
    p = today_data['open']

    if len(today_data) == 0:
        print("今天停牌")
        return

    if context.portfolio.available_cash - amount * p < 0:
        amount = int(context.portfolio.available_cash / p)
        print("现金不足,已调整为%d" % (amount))

    if amount % 100 != 0:
        if amount != -context.portfolio.positions.get(security, Position()).total_amount:
            amount = int(amount / 100) * 100
            print("不是100的倍数,已调整为%d" % amount)

    if context.portfolio.positions.get(security, Position()).total_amount < -amount:
        amount = -context.portfolio.positions.get(security, Position()).total_amount
        print("卖出股票不能超出持仓数量,已调整为%d" % amount)

    postion = Position()
    postion.total_amount = context.portfolio.positions.get(security, Position()).total_amount + amount
    context.portfolio.positions[security] = postion

    context.portfolio.available_cash -= amount * p

    if context.portfolio.positions[security].total_amount == 0:
        del context.portfolio.positions[security]


# 按股数下单
def order(security, amount):
    today_data = get_today_data(security)
    _order(today_data, security, amount)


# 按目标股数下单
def order_target(security, amount):
    if amount < 0:
        print("数量不能为负,已调整成为0")
        amount = 0

    today_data = get_today_data(security)
    hold_amount = context.portfolio.positions.get(security, 0).total_amount  # ToDo  T+1问题
    delta_amount = amount - hold_amount
    _order(today_data, security, delta_amount)


# 按价值下单
def order_value(security, value):
    today_data = get_today_data(security)
    amount = int(value / today_data['open'])
    _order(today_data, security, amount)


# 按目标价值下单
def order_target_value(security, value):
    today_data = get_today_data(security)
    if value < 0:
        print("价值不能为负,已调整为0")
        value = 0

    hold_value = context.portfolio.positions.get(security, 0).total_amount * today_data['open']
    delta_value = value - hold_value
    order_value(security, delta_value)
