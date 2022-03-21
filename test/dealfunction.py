from overall import *

#按股数下单(作为基础函数)
def _order(today_data, security, amount):
    p = today_data['open']

    if len(today_data) == 0:
        print("今天停牌")
        return

    if context.cash - amount * p < 0:
        amount = int(context.cash / p)
        print("现金不足,已调整为%d" % (amount))

    if amount % 100 != 0:
        if amount != -context.positions.get(security, 0):
            amount = int(amount / 100) * 100
            print("不是100的倍数,已调整为%d" % amount)

    if context.positions.get(security, 0) < -amount:
        amount = -context.positions.get(security, 0)
        print("卖出股票不能超出持仓数量,已调整为%d" % amount)
    
    context.positions[security] = context.positions.get(security, 0) + amount

    context.cash -= amount * p

    if context.positions[security] == 0:
         del context.positions[security]

#按股数下单
def order(security, amount):
    today_data = get_today_data(security)
    _order(today_data, security, amount)

#按目标股数下单
def order_target(security, amount):
    if amount < 0:
        print("数量不能为负,已调整成为0")
        amount = 0
    
    today_data = get_today_data(security)
    hold_amount = context.positions.get(security, 0)  #ToDo  T+1问题
    delta_amount = amount - hold_amount
    _order(today_data, security, delta_amount)

#按价值下单
def order_value(security, value):
    today_data = get_today_data(security)
    amount = int(value / today_data['open'])
    _order(today_data, security, amount)

#按目标价值下单
def order_target_value(security, value):
    today_data = get_today_data(security)
    if value < 0:
        print("价值不能为负,已调整为0")
        value = 0

    hold_value = context.positions.get(security, 0) * today_data['open']
    delta_value = value - hold_value
    order_value(security, delta_value)
