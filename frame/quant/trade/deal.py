"""
交易函数
"""
from quant.security.get import *

MP = "市价单"

# 按股数下单(作为基础函数)
def _order(today_data, security, amount):
    p = today_data['open']  # 以当日开盘价计算

    # 滑点左右价格
    if context.slippage_type == 0:
        if security in context.slippage_FixedSec:
            if amount > 0:
                p = p + context.slippage_FixedSec[security] / 2
            elif amount < 0:
                p = p - context.slippage_FixedSec[security] / 2
        else:
            if amount > 0:
                p = p + context.slippage / 2
            elif amount < 0:
                p = p - context.slippage / 2
    elif context.slippage_type == 1:
        if security in context.slippage_PerSec:
            if amount > 0:
                p = p * (1 + context.slippage_PerSec[security])
            elif amount < 0:
                p = p * (1 - context.slippage_PerSec[security])
        else:
            if amount > 0:
                p = p * (1 + context.slippage)
            elif amount < 0:
                p = p * (1 - context.slippage)
    elif context.slippage_type == 2:
        if security in context.slippage_JumpSec:
            if amount > 0:
                p = p + 0.01 * context.slippage_JumpSec[security]
            elif amount < 0:
                p = p - 0.01 * context.slippage_JumpSec[security]
        else:
            if amount > 0:
                p = p + 0.01 * context.slippage
            elif amount < 0:
                p = p - 0.01 * context.slippage
    else:
        Log.log("%s:未知滑点类型\n", context.dt)

    # 判断购买类型
    buyorsell = 'None'
    if amount < 0:
        buyorsell = '卖'
    elif amount > 0:
        buyorsell = '买'

    # 前置判断
    if context.isMainPor:
        if len(today_data) == 0:
            Log.log("%s:[%s]这天停牌\n", context.dt, security)
            return

        if context.portfolio.available_cash - amount * p < 0:
            amount = int(context.portfolio.available_cash / p)
            Log.log("%s:[%s]总账户现金不足,数量已调整为%s\n", context.dt, security, amount)

        if amount % 100 != 0:
            if amount != -context.portfolio.positions.get(security, Position()).total_amount:
                amount = int(amount / 100) * 100
                Log.log("%s:[%s]交易股数不是100的倍数,数量已调整为%s\n", context.dt, security,amount)

        if context.portfolio.positions.get(security, Position()).total_amount < -amount:
            amount = -context.portfolio.positions.get(security, Position()).total_amount
            Log.log("%s:[%s]卖出股票不能超出持仓数量,数量已调整为%s\n", context.dt, security,amount)
    else:
        if len(today_data) == 0:
            Log.log("%s:[%s]这天停牌\n", context.dt, security)
            return

        if context.portfolio.subPortfolio[context.subPor_index].available_cash - amount * p < 0:
            amount = int(context.portfolio.subPortfolio[context.subPor_index].available_cash / p)
            Log.log("%s:[%s]该子账户现金不足,数量已调整为%s\n", context.dt, security, amount)

        if amount % 100 != 0:
            if amount != -context.portfolio.subPortfolio[context.subPor_index].positions.get(security, Position()).total_amount:
                amount = int(amount / 100) * 100
                Log.log("%s:[%s]交易股数不是100的倍数,数量已调整为%s\n", context.dt, security, amount)

        if context.portfolio.subPortfolio[context.subPor_index].positions.get(security, Position()).total_amount < -amount:
            amount = -context.portfolio.subPortfolio[context.subPor_index].positions.get(security, Position()).total_amount
            Log.log("%s:[%s]卖出股票不能超出持仓数量,数量已调整为%s\n", context.dt, security, amount)

    # 手续费计算
    charge = 0
    if amount > 0:
        charge = amount * p * context.commission
        if charge < 5:
            charge = 5
    elif amount < 0:
        charge = -amount * p * context.stamp_duty
    charge = round(charge, 2)

    # 更新仓位消息(未完成)
    if context.isMainPor:
        postion = context.portfolio.positions.get(security, Position())
    else:
        postion = context.portfolio.subPortfolio[context.subPor_index].positions.get(security, Position())
    postion.total_amount = postion.total_amount + amount
    postion.price = p
    name = get_sbasic(code=security, fields=['name'])   # 证券的中文名
    if len(name.index) != 0:
        postion.security_name = name['name'][0]
    else:
        postion.security_name = "未找到相关消息"
    postion.security_code = security
    if amount > 0:
        postion.buy_pp.append(p)
        postion.buy_pn.append(amount)

    # 平仓盈亏计算
    profit = 0
    if amount < 0:
        tn = -amount
        cnt = 0
        rest = 0
        for n in postion.buy_pn:
            tn -= n
            ++cnt
            if tn <= 0:
                rest = tn + n
                break
        for i in range(cnt-1):
            profit += (postion.price - postion.buy_pp[i]) * postion.buy_pn[i]
        profit += (postion.price - postion.buy_pp[cnt-1]) * rest
        postion.buy_pn[cnt-1] -= rest
        del postion.buy_pn[0:cnt-1]
        del postion.buy_pp[0:cnt-1]
        profit = round(profit, 2)

    # 更新仓位收尾消息(未完成)
    postion.last_price = p
    postion.last_update_time = context.dt
    if context.isMainPor:
        context.portfolio.positions[security] = postion
    else:
        context.portfolio.subPortfolio[context.subPor_index].positions[security] = postion

    # 如果这个证券数量为0则删
    if context.isMainPor:
        if context.portfolio.positions[security].total_amount == 0:
            del context.portfolio.positions[security]
    else:
        if context.portfolio.subPortfolio[context.subPor_index].positions[security].total_amount == 0:
            del context.portfolio.subPortfolio[context.subPor_index].positions[security]

    # 更新账户总金额
    if context.isMainPor:
        context.portfolio.available_cash -= amount * p  # 盈亏
        context.portfolio.available_cash -= charge      # 扣印花税或佣金
        context.portfolio.available_cash -= context.transfer_fee  # 扣过户费
    else:
        context.portfolio.subPortfolio[context.subPor_index].available_cash -= amount * p  # 盈亏
        context.portfolio.subPortfolio[context.subPor_index].available_cash -= charge  # 扣印花税或佣金
        context.portfolio.subPortfolio[context.subPor_index].available_cash -= context.transfer_fee  # 扣过户费

    # 交易日志填写
    TradeInfo.log("%s  %s  %s  %s  %s  %s  %s  %s  %s  %s\n", context.dt, security, postion.security_name, buyorsell, MP, amount, p, round(amount*p, 2), profit, charge)

#---------------------------------------------------------------
# 按股数下单
def order(security, amount):
    today_data = get_today_data(security)
    _order(today_data, security, amount)


# 按目标股数下单
def order_target(security, amount):
    if amount < 0:
        Log.log("%s:[%s]交易数量不能为负,已调整成为0\n", context.dt, security)
        amount = 0

    today_data = get_today_data(security)
    if context.isMainPor:
        hold_amount = context.portfolio.positions.get(security, 0).total_amount
    else:
        hold_amount = context.portfolio.subPortfolio[context.subPor_index].positions.get(security, 0).total_amount
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
        Log.log("%s:[%s]目标价值不能为负,已调整为0\n", context.dt, security)
        value = 0

    if context.isMainPor:
        hold_value = context.portfolio.positions.get(security, 0).total_amount * today_data['open']
    else:
        hold_value = context.portfolio.subPortfolio[context.subPor_index].positions.get(security, 0).total_amount * today_data['open']
    delta_value = value - hold_value
    order_value(security, delta_value)
