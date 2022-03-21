from frame import *

#
def run():
    plt_df = pd.DataFrame(index=pd.to_datetime(context.date_range), columns=['value'])
    init_value = context.cash
    initialize(context)
    last_price = {}
    for dt in context.date_range:
        context.dt = parse(dt)
        handle_data(context)
        value = context.cash
        for stock in context.positions:
            #考虑停牌情况
            today_data = get_today_data(stock)
            if len(today_data) == 0:
                p = last_price[stock]
            else:
                p = today_data['open']
                last_price[stock] = p
            value += p * context.positions[stock]
        plt_df.loc[dt, 'value'] = value
    plt_df['ratio'] = (plt_df['value'] - init_value) / init_value
    
    bm_df = attribute_daterange_history(context.benchmark, context.start_date, context.end_date)
    bm_init = bm_df['open'][0]
    plt_df['benckmark_ratio'] = (bm_df['open'] - bm_init) / bm_init
    
    plt_df[['ratio','benckmark_ratio']].plot()
    plt.show()

run()