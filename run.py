"""
后台运行函数
"""

from frame import *
import matplotlib.pyplot as plt

CASH = 100000
START_DATE = '2016-01-23'
END_DATE = '2016-06-01'

context.set(CASH, START_DATE, END_DATE)

def run():
    plt_df = pd.DataFrame(index=pd.to_datetime(context.date_range), columns=['value'])
    init_value = context.portfolio.available_cash
    initialize(context)
    last_price = {}
    #在指定日期内循环遍历每一天
    for dt in context.date_range:
        context.dt = parse(dt)
        handle_data(context)
        value = context.portfolio.available_cash
        context.runtime = context.runtime + 1

        #循环遍历账户里的有的股票
        for stock in context.portfolio.positions:
            # 考虑停牌情况
            today_data = get_today_data(stock)
            if len(today_data) == 0:
                p = last_price[stock]
            else:
                p = today_data['open']
                last_price[stock] = p
            value += p * context.portfolio.positions[stock].total_amount
            context.portfolio.positions_value = value

        plt_df.loc[dt, 'value'] = value

    #收益率计算
    plt_df['ratio'] = (plt_df['value'] - init_value) / init_value

    bm_df = attribute_daterange_history(context.benchmark, context.start_date, context.end_date)
    bm_init = bm_df['open'][0]
    #基准收益率就算
    plt_df['benckmark_ratio'] = (bm_df['open'] - bm_init) / bm_init

    #画图
    plt_df[['ratio', 'benckmark_ratio']].plot()
    plt.show()


run()